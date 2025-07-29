import asyncio
import pytest
from fastmcp import Client
import anndata
from pathlib import Path
from scmcp.server import sc_mcp, setup

asyncio.run(setup())


@pytest.mark.asyncio 
async def test_create_kernel():
    """Test kernel creation with different kernel types."""
    test_dir = Path(__file__).parent / "data/pbmc68k_reduced.h5ad"
    
    async with Client(sc_mcp) as client:
        # First read the data
        result = await client.call_tool("sc_io_read", {"request": {"filename": test_dir}})
        assert "AnnData" in result[0].text

        # Test connectivity kernel
        result = await client.call_tool("cr_kernel_create_kernel", {
            "request": {
                "kernel": "connectivity",
                "n_neighbors": 30
            }
        })
        assert "connectivity" in result[0].text

        # Compute transition matrix
        result = await client.call_tool("cr_kernel_compute_transition_matrix", {
            "request": {
                "kernel": "connectivity",
                "threshold_scheme": "hard",
                "weight_connectivities": 0.2,
                "weight_self_loops": 0.1
            }
        })
        assert "connectivity" in result[0].text



