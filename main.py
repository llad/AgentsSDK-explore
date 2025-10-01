import asyncio
import os
import shlex
import shutil
import subprocess
import time
from typing import Any

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStreamableHttp
from agents.model_settings import ModelSettings


def _should_start_local_server() -> bool:
    value = os.environ.get("START_LOCAL_SERVER")
    if value is None:
        return True

    return value.strip().lower() not in {"0", "false", "no"}


def _get_server_url() -> str:
    return os.environ.get("MCP_SERVER_URL", "http://localhost:8000/mcp")


def _get_local_server_command(server_file: str) -> list[str]:
    command = os.environ.get("LOCAL_SERVER_COMMAND")
    if command:
        return shlex.split(command)

    return ["uv", "run", server_file]


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="Use the tools to answer the questions.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    # Use the `add` tool to add two numbers
    message = "Add these numbers: 7 and 22."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_weather` tool
    message = "What's the weather in Tokyo?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_secret_word` tool
    message = "What's the secret word?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    server_url = _get_server_url()
    async with MCPServerStreamableHttp(
        name="Streamable HTTP Python Server",
        params={
            "url": server_url,
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Streamable HTTP Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)


if __name__ == "__main__":
    start_local_server = _should_start_local_server()
    if start_local_server and not shutil.which("uv") and not os.environ.get("LOCAL_SERVER_COMMAND"):
        raise RuntimeError(
            "uv is not installed. Please install it: https://docs.astral.sh/uv/getting-started/installation/"
        )

    # We'll run the Streamable HTTP server in a subprocess. Usually this would be a remote server, but for this
    # demo, we'll run it locally at http://localhost:8000/mcp unless configured otherwise.
    process: subprocess.Popen[Any] | None = None
    try:
        if start_local_server:
            this_dir = os.path.dirname(os.path.abspath(__file__))
            server_file = os.path.join(this_dir, "server.py")
            command = _get_local_server_command(server_file)

            print(f"Starting Streamable HTTP server at {_get_server_url()} ...")

            process = subprocess.Popen(command)
            # Give it 3 seconds to start
            time.sleep(3)

            print("Streamable HTTP server started. Running example...\n\n")
        else:
            print(
                "Using external Streamable HTTP server at "
                f"{_get_server_url()}. Skipping local server startup.\n"
            )

        asyncio.run(main())
    except Exception as e:
        print(f"Error running example: {e}")
        exit(1)
    finally:
        if process:
            process.terminate()
