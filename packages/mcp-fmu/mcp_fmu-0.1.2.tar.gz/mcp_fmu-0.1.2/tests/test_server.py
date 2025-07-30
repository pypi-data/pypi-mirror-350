import pathlib
import zipfile
import httpx

import pytest
from fastmcp import Client


from mcp_fmu.server import mcp

REFERENCE_FMUS_URL = "https://github.com/modelica/Reference-FMUs/releases/download/v0.0.38/Reference-FMUs-0.0.38.zip"


def download_reference_fmu(name: str, tmpdir: pathlib.Path) -> pathlib.Path:
    # Download the reference FMU zip file to a temporary directory
    response = httpx.get(REFERENCE_FMUS_URL, follow_redirects=True)
    response.raise_for_status()  # Ensure the request was successful

    zip_path = tmpdir / "Reference-FMUs.zip"
    with open(zip_path, "wb") as f:
        f.write(response.content)

    # Extract the zip file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(tmpdir)

    # Return the path to the extracted FMU files
    return (tmpdir / name).absolute()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "reference_fmu", ["2.0/BouncingBall.fmu", "3.0/BouncingBall.fmu"]
)
async def test_get_model_description(reference_fmu, tmpdir):
    filename = download_reference_fmu(reference_fmu, pathlib.Path(tmpdir))
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_model_description",
            {"filename": str(filename)},
        )
        assert isinstance(result[0].text, str)  # type: ignore


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "reference_fmu", ["2.0/BouncingBall.fmu", "3.0/BouncingBall.fmu"]
)
async def test_simulate_fmu(reference_fmu, tmpdir):
    filename = download_reference_fmu(reference_fmu, pathlib.Path(tmpdir))
    async with Client(mcp) as client:
        result = await client.call_tool(
            "simulate_fmu",
            {
                "filename": str(filename),
                "output_filename": None,
                "start_time": 0.0,
                "stop_time": 1.0,
                "step_size": 0.01,
            },
        )
        assert isinstance(result[0].text, str)  # type: ignore
