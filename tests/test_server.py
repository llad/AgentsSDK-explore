import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

requests_stub = types.ModuleType("requests")
requests_stub.get = lambda *args, **kwargs: None
sys.modules.setdefault("requests", requests_stub)

fastmcp_module = types.ModuleType("mcp.server.fastmcp")


class _FastMCP:
    def __init__(self, *_, **__):
        pass

    def tool(self):
        def decorator(func):
            return func

        return decorator

    def run(self, *_, **__):
        return None


fastmcp_module.FastMCP = _FastMCP

mcp_server_module = types.ModuleType("mcp.server")
mcp_server_module.fastmcp = fastmcp_module
mcp_module = types.ModuleType("mcp")
mcp_module.server = mcp_server_module

sys.modules.setdefault("mcp", mcp_module)
sys.modules.setdefault("mcp.server", mcp_server_module)
sys.modules.setdefault("mcp.server.fastmcp", fastmcp_module)

from server import add


def test_add_returns_sum():
    assert add(2, 3) == 5
