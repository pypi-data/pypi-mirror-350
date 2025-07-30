import tempfile
from pathlib import Path
from typing import Annotated, Literal

import pandas as pd
from fastmcp import Context, FastMCP
from fmpy import extract
from fmpy import simulate_fmu as fmpy_simulate_fmu
from pydantic import Field

mcp: FastMCP = FastMCP(
    name="mcp-fmu",
    instructions="""
        This tool provides functionality to simulate FMU files and retrieve model descriptions.
        Call `get_model_description` to retrieve the model description of an FMU file which includes
        information such as model name, description, fmi version, fmu type, and scalar variable information categorized by causality and variability.
        Call `simulate_fmu` to run a simulation of an FMU file. You can specify the start time, stop time, step size, and other parameters for the simulation.
    """,
    on_duplicate_prompts="error",
    on_duplicate_tools="error",
    tags={"fmu", "simulation"},
)


@mcp.tool(
    name="get_model_description",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
    },
)
async def get_model_description(
    filename: Annotated[Path, Field(description="Path to the local FMU file")],
) -> str:
    """
    Get the model description information of the FMU.

    Parameters
    ----------
    filename : Path
        The path to the FMU file.

    Returns
    -------
    str
        The model description information of the FMU.

    Raises
    ------
    FileNotFoundError
        If the file does not exist or is not a file.
    ValueError
        If the file is not an FMU file.
    """
    if not filename.exists():
        raise FileNotFoundError(f"File {filename} does not exist.")

    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} is not a file.")

    if not filename.suffix == ".fmu":
        raise ValueError(f"File {filename} is not an FMU file.")

    with tempfile.TemporaryDirectory() as tmp:
        extract(filename.absolute(), tmp)
        with open(Path(tmp) / "modelDescription.xml", "r") as f:
            md = f.read()

    return md


@mcp.tool(
    name="simulate_fmu",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True,
    },
)
async def simulate_fmu(
    filename: Annotated[Path, Field(description="Path to the local FMU file")],
    ctx: Context,
    output_filename: Annotated[
        Path | None,
        Field(description="Path for the generated result output file"),
    ] = None,
    start_time: Annotated[
        float, Field(description="Start time of the simulation in seconds", ge=0.0)
    ] = 0.0,
    stop_time: Annotated[
        float,
        Field(
            default=1.0, description="Stop time of the simulation in seconds", gt=0.0
        ),
    ] = 1.0,
    step_size: Annotated[
        float,
        Field(
            default=0.01, description="Step size of the simulation in seconds", gt=0.0
        ),
    ] = 0.01,
    output_interval: Annotated[
        float,
        Field(
            description="Output intervals of the simulation in seconds, it is used to determine the time points at which the output is recorded",
        ),
    ] = 0.01,
    solver: Annotated[
        Literal["CVode", "Euler"],
        Field(description="Solver to use for model exchange type FMUs"),
    ] = "CVode",
    relative_tolerance: Annotated[
        float | str | None,
        Field(description="Relative tolerance of the simulation"),
    ] = None,
    record_events: Annotated[
        bool,
        Field(description="Whether to record events during the simulation"),
    ] = True,
    fmi_type: Annotated[
        str | None,
        Field(description="FMI type to use for the simulation"),
    ] = None,
    start_values: Annotated[
        dict, Field(description="Start values for the simulation")
    ] = {},
    apply_default_start_values: Annotated[
        bool, Field(description="Whether to apply default start values")
    ] = True,
    output_variables: Annotated[
        list[str] | None,
        Field(description="Outputs to record during the simulation"),
    ] = None,
    debug_logging: bool = False,
) -> dict:
    """
    Run an FMU simulation.

    Parameters
    ----------
    filename : Path
        The path to the FMU file.
    output_filename : Path | None, optional
        The path to the output file, by default None
        - If None, the output is saved as a CSV file
        - If a path, the output is saved as a CSV file defined by the path
    start_time : float, optional
        The start time of the simulation, by default 0.0
    stop_time : float, optional
        The stop time of the simulation, by default 1.0
    step_size : float, optional
        The step size of the simulation, by default 0.01
    output_interval : float, optional
        The output interval of the simulation, by default 0.01
    solver : str, optional
        solver to use for model exchange ('Euler' or 'CVode'), by default "CVode"
    relative_tolerance : float | str | None, optional
        The relative tolerance of the simulation, by default None
    record_events : bool, optional
        Whether to record events during the simulation, by default True
    fmi_type : str | None, optional
        The FMI type to use for the simulation, by default None
    start_values : dict, optional
        The start values for the simulation, by default {}
    apply_default_start_values : bool, optional
        Whether to apply default start values, by default False
    output_variables : list[str] | None, optional
        The outputs to record during the simulation, by default None
        - If None, all outputs are recorded.
        - If a list, only the specified outputs are recorded.
    debug_logging : bool, optional
        Whether to enable debug logging, by default False

    Returns
    -------
    dict
        The results of the simulation.

    Raises
    ------
    FileNotFoundError
        If the file does not exist or is not a file.
    ValueError
        If the file is not an FMU file.
    """
    await ctx.info(f"Simulating fmu: {filename}")

    if not filename.exists():
        raise FileNotFoundError(f"File {filename} does not exist.")

    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} is not a file.")

    if not filename.suffix == ".fmu":
        raise ValueError(f"File {filename} is not an FMU file.")

    with tempfile.TemporaryDirectory() as tmp:
        extract(str(filename), tmp)

        result = fmpy_simulate_fmu(
            tmp,
            start_time=start_time,
            stop_time=stop_time,
            step_size=step_size,
            output_interval=output_interval,
            solver=solver,
            relative_tolerance=relative_tolerance,  # type: ignore
            record_events=record_events,
            fmi_type=fmi_type,  # type: ignore
            start_values=start_values,
            apply_default_start_values=apply_default_start_values,
            output=output_variables,  # type: ignore
            debug_logging=debug_logging,
        )

        df = pd.DataFrame(result)

        if output_filename is None:
            output_filename = filename.with_suffix(".csv")

        df.to_csv(output_filename, index=False)

    return {
        "result": "success" if result is not None else "failure",
        "output_file": str(output_filename),
    }


@mcp.prompt(
    name="simulate_fmu_prompt",
    description="Creates a request to simulate an FMU file",
)
async def simulate_fmu_prompt(
    filename: Annotated[Path, Field(description="Path to the local FMU file")],
) -> str:
    return rf"""
        Generate a short summary of the FMU file {filename} using the `get_model_description` tool with at least the following information
            - model name and description
            - fmi version
            - fmu type
            - scalar variable information categorized by causality and variability
        If the fmu contains any fixed parameters, then generate a list of all fixed parameters and their start values to let the user know about them.
        If the fmu contains any input variables, then generate a list of all input variables and their start values to let the user know about them.
        Get default experiment settings from the model description and use them as the default values for the fmu simulation.
        If the fmu is only a ModelExchange type FMU, then CVode solver should be used as default solver.
        Simulate the fmu {filename} using the `simulate_fmu` tool, and the `output_filename` should be set to the same path as the fmu file but with a `.csv` extension.
    """


if __name__ == "__main__":
    mcp.run()
