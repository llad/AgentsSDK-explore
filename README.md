# AgentsSDK-explore
Explore the agents SDK capabilities

## Running with Docker Compose

1. Build and start the services:

   ```bash
   docker compose up --build
   ```

   This command starts two containers:

   - `server`: exposes the Streamable HTTP MCP server on port `8000`.
   - `app`: runs `main.py`, which connects to the server and demonstrates the sample interactions.

2. To stop the containers, press `Ctrl+C` and run:

   ```bash
   docker compose down
   ```

### Environment variables

The application can be configured with the following variables:

| Variable | Description | Default |
| --- | --- | --- |
| `MCP_SERVER_URL` | URL of the MCP server used by `main.py`. | `http://localhost:8000/mcp` |
| `START_LOCAL_SERVER` | Set to `0`/`false` to skip starting a local server subprocess. | `1` |
| `LOCAL_SERVER_COMMAND` | Custom command to start the local server (overrides the default `uv run server.py`). | *(unset)* |
