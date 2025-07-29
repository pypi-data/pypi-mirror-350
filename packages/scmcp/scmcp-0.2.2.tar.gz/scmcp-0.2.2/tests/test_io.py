import asyncio
import pytest
from fastmcp import Client
import anndata
from pathlib import Path
from scmcp.server import sc_mcp, setup


asyncio.run(setup())

@pytest.mark.asyncio 
async def test_read_and_write():
    test_dir = Path(__file__).parent / "data/hg19"
    outfile = Path(__file__).parent / "data/test.h5ad"
    async with Client(sc_mcp) as client:
        tools = await client.list_tools()
        result = await client.call_tool("sc_io_read", {"request":{"filename": test_dir}})
        assert "AnnData" in result[0].text

        result = await client.call_tool("sc_io_write", {"request":{"filename": outfile}})
        assert outfile.exists()
        outfile.unlink()
