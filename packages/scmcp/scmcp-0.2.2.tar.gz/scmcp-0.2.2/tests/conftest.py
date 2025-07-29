
import pytest

@pytest.fixture
def mcp_config():
    return {
        "mcpServers": {
            "scmcp": {
                "command": "scmcp",
                "args": ["run"]
            }
        }
    }