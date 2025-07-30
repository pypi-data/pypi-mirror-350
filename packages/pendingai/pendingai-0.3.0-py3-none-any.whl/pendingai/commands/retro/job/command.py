#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import enum
import json
import os
import pathlib
import typing
from datetime import datetime

import rich
import rich.progress
import rich.prompt
import rich.table
import typer

from pendingai import config
from pendingai.commands.retro.controller import RetroController
from pendingai.commands.retro.job.controller import RetroJobController
from pendingai.commands.retro.job.models import JobPage
from pendingai.context import Context
from pendingai.utils import formatters, regex_patterns

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)

app = typer.Typer(
    name="job",
    help=(
        "Operations working on individual retrosynthesis jobs referred to by "
        "their id."
        "\n\nMost commands operate on single jobs only. <result> and <depict> "
        "are capable of processing multiple jobs."
    ),
    short_help="Operations working on individual retrosynthesis jobs.",
    add_completion=False,
    pretty_exceptions_show_locals=False,
    rich_markup_mode=None,
)

# region callbacks -----------------------------------------------------


def _validate_page_size(page_size: int | None) -> int | None:
    """
    Page size options require an enumeration, to avoid this we do a
    quick lookup in the range [5, 25] with step size 5 to check it is a
    valid interval value.

    Args:
        page_size (int, optional): Page size option.

    Raises:
        typer.BadParameter: Page size value is not a valid interval.

    Returns:
        int: Page size option.
    """
    if page_size and page_size not in range(5, 26, 5):
        raise typer.BadParameter("Must be an interval of 5.")
    return page_size


def _eng_callback(context: Context, engine: str | None) -> str | None:
    """
    Check an optional retrosynthesis engine id is available and exists
    in the database.

    Args:
        context (Context): App runtime context.
        engine (str, optional): Retrosynthesis engine id.

    Raises:
        typer.BadParameter: Retrosynthesis engine id does not exist or
            is not currently available.

    Returns:
        str: Retrosynthesis engine id.
    """
    if engine:
        if len(engine) < 11:
            raise typer.BadParameter("Retrosynthesis engine not available.")
        ctrl = RetroController(context)
        engine_ids: list[str] = [x.id for x in ctrl.retrieve_retrosynthesis_engines()]
        matched_ids: list[str] = [x for x in engine_ids if x.startswith(engine)]
        if len(matched_ids) == 0:
            raise typer.BadParameter("Retrosynthesis engine not available.")
        elif len(matched_ids) > 1:
            raise typer.BadParameter("ID matches more than 1 engine, use a longer ID.")
        engine = matched_ids[0]
    return engine


def _lib_callback(context: Context, libraries: list[str] | None) -> list[str] | None:
    """
    Check an optional collection of building block libraries are
    available and exist in the database.

    Args:
        context (Context): App runtime context.
        libraries (list[str], optional): Building block library ids.

    Raises:
        typer.BadParameter: Building block library ids do not exist; if
            at least one is not found.

    Returns:
        list[str]: Building block library ids.
    """
    if libraries:
        ctrl = RetroController(context)
        for i in libraries:
            if i not in [x.id for x in ctrl.retrieve_building_block_libraries()]:
                raise typer.BadParameter(f"Building block library not found: {i}.")
    return libraries


def _job_id_callback(job_id: str | None) -> str | None:
    """
    Validate a retrosynthesis job id follows the required regex.

    Args:
        job_id (str, optional): Retrosynthesis job id.

    Raises:
        typer.BadParameter: Job id does not follow the required regex.

    Returns:
        str: Retrosynthesis job id.
    """
    if job_id is not None and regex_patterns.JOB_ID_PATTERN.match(job_id) is None:
        raise typer.BadParameter(f"Invalid job ID format: {job_id}")
    return job_id


def _job_ids_file_callback(job_ids_file: pathlib.Path | None) -> pathlib.Path | None:
    """
    Validate an optional input filepath containing line-delimited job
    ids and has all entries following the required regex.

    Args:
        job_ids_file (pathlib.Path, optional): Input filepath.

    Raises:
        typer.BadParameter: A job ID does not follow the required regex.

    Returns:
        pathlib.Path: Input filepath.
    """
    if job_ids_file:
        for i, job_id in enumerate(job_ids_file.open("r").readlines(), 1):
            job_id = job_id.strip()
            if regex_patterns.JOB_ID_PATTERN.match(job_id) is None:
                raise typer.BadParameter(f"Invalid job ID format: {job_id} (line {i})")
    return job_ids_file


def _output_dir_callback(output_dir: pathlib.Path) -> pathlib.Path:
    """
    Given an output directory optional parameter, if the path does not
    yet exist then confirm with the user and give standard out feedback.

    Args:
        output_dir (pathlib.Path): Output directory to check exists.

    Returns:
        pathlib.Path: Output directory that exists.
    """
    if not output_dir.exists():
        prompt: str = f"[warn]! Do you want to create the directory: {output_dir}?"
        if rich.prompt.Confirm.ask(prompt, console=console):
            output_dir.mkdir(parents=True)
            console.print(f"[success]✓ Directory created successfully: {output_dir}")
        else:
            raise typer.Exit(1)
    return output_dir


def _default_output_file(suffix: str = ".json") -> pathlib.Path:
    """
    Callable default generator for an output filename for an option.
    Provides an isoformat datetime file name with given suffix in the
    current working directory of the user.

    Args:
        suffix (str, optional): File suffix. Defaults to ".json".

    Returns:
        pathlib.Path: Generated output filename.
    """
    p: pathlib.Path = pathlib.Path.cwd() / datetime.now().isoformat(timespec="seconds")
    return p.with_suffix(suffix)


# region command: submit -----------------------------------------------


@app.command(
    "submit",
    help=(
        "Submit a job to a retrosynthesis engine.\n\n"
        "NOTE: Jobs including their results will be automatically deleted "
        "30 days after completion.\n\n"
        "Building block libraries are repeatable:\n\n"
        "\t<pendingai retro job submit SMILES --library lib1 --library lib2>"
    ),
    short_help="Submit a job to a retrosynthesis engine.",
    no_args_is_help=True,
)
def submit_job(
    context: Context,
    smiles: typing.Annotated[
        str,
        typer.Argument(
            help="Query molecule smiles.",
            metavar="SMILES",
        ),
    ],
    retrosynthesis_engine: typing.Annotated[
        str | None,
        typer.Option(
            "--engine",
            help="Retrosynthesis engine id. Defaults to primary engine.",
            callback=_eng_callback,
        ),
    ] = None,
    building_block_libraries: typing.Annotated[
        list[str] | None,
        typer.Option(
            "--library",
            help="Building block library ids. Defaults to all available libraries.",
            callback=_lib_callback,
        ),
    ] = [],
    number_of_routes: typing.Annotated[
        int,
        typer.Option(
            "--num-routes",
            help="Maximum number of retrosynthetic routes to generate. Defaults to 20.",
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=50,
        ),
    ] = 20,
    processing_time: typing.Annotated[
        int,
        typer.Option(
            "--time-limit",
            help="Maximum processing time in seconds. Defaults to 300.",
            show_default=False,
            metavar="INTEGER",
            min=60,
            max=600,
        ),
    ] = 300,
    reaction_limit: typing.Annotated[
        int,
        typer.Option(
            "--reaction-limit",
            help=(
                "Maximum number of times a specific reaction can "
                "appear in generated retrosynthetic routes. Defaults "
                "to 3."
            ),
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=20,
        ),
    ] = 3,
    building_block_limit: typing.Annotated[
        int,
        typer.Option(
            "--block-limit",
            help=(
                "Maximum number of times a building block can appear "
                "in a single retrosynthetic route. Default to 3."
            ),
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=20,
        ),
    ] = 3,
    render_json: typing.Annotated[
        bool,
        typer.Option(
            "--json",
            help="Render output as JSON.",
            is_flag=True,
        ),
    ] = False,
) -> str:
    """
    Submit a single retrosynthesis job and retrieve the newly created
    job id returned by the api layer.

    Args:
        context (Context): App runtime context.
        smiles (str): Smiles query molecule.
        retrosynthesis_engine (str, optional): Retrosynthesis engine
            id. Defaults to primary engine.
        building_block_libraries (list[str], optional): Building block
            library ids. Defaults to all available libraries.
        number_of_routes (int, optional): Maximum number of
            retrosynthetic routes to generate. Defaults to 20.
        processing_time (int, optional): Maximum processing time in
            seconds. Defaults to 300.
        reaction_limit (int, optional): Maximum number of times a
            specific reaction can appear in generated retrosynthetic
            routes. Defaults to 3.
        building_block_limit (int, optional): Maximum number of times a
            building block can appear in a single retrosynthetic route.
            Default to 3.
        render_json (bool, optional): Render output as json.

    Returns:
        str: Retrosynthesis job id.
    """
    controller = RetroJobController(context)

    # update user with feedback if default engine and libraries are used
    # and since typer does not allow nullable lists, also coerce libs to
    # none if it is empty.
    if retrosynthesis_engine is None and not render_json:
        console.print("[success]✓ Added default retrosynthesis engine.")
    if building_block_libraries == []:
        building_block_libraries = None
    if building_block_libraries is None and not render_json:
        console.print("[success]✓ Added default building block libraries.")

    # create the job and extract the job id to return to the user in
    # the console either as json or human readable text.
    job_id: str = controller.create_job(
        smiles,
        retrosynthesis_engine,
        building_block_libraries,
        number_of_routes,
        processing_time,
        reaction_limit,
        building_block_limit,
    )

    if render_json:
        console.print_json(data={"jobId": job_id})
    else:
        console.print(f"[success]✓ Retrosynthesis job submitted with ID: {job_id}")
    return job_id


# region command: status -----------------------------------------------


@app.command(
    "status",
    help="Get the status of a retrosynthesis job.",
    short_help="Get the status of a retrosynthesis job.",
    no_args_is_help=True,
)
def retrieve_job_status(
    context: Context,
    job_id: typing.Annotated[
        str,
        typer.Argument(
            help="Retrosynthesis job ID to retrieve the status for.",
            callback=_job_id_callback,
            metavar="JOB_ID",
        ),
    ],
    render_json: typing.Annotated[
        bool,
        typer.Option(
            "--json",
            help="Render output as JSON.",
            is_flag=True,
        ),
    ] = False,
) -> str:
    """
    Retrieve the status of a retrosynthesis job by id and provide the
    feedback in a readable format to the user.

    Args:
        context (Context): App runtime context.
        job_id (str): Retrosynthesis job id to retrieve the status of.
        render_json (bool, optional): Render output as json.

    Raises:
        typer.Exit: Retrosynthesis job id was not found.

    Returns:
        str: Retrosynthesis job status.
    """
    controller = RetroJobController(context)
    status: str = controller.retrieve_job_status(job_id)

    if render_json:
        console.print_json(data={"status": status})
    else:
        if status == "completed":
            console.print(f"[success]✓ Retrosynthesis job is complete: {job_id}")
        elif status == "failed":
            console.print(f"[red]! Retrosynthesis job failed: {job_id}")
        elif status == "processing":
            console.print(f"[warn]! Retrosynthesis job is in progress: {job_id}")
        else:
            console.print(f"[warn]! Preparing retrosynthesis job: {job_id}")

    return status


# region command: result -----------------------------------------------


@app.command(
    "result",
    help=(
        "Retrieve results for one or more retrosynthesis jobs by ID. The command "
        "is slower than batch-based screening and retrieves results individually. "
        "Results are written to file as JSON.\n\n"
        "NOTE: Provide either a single [JOB_ID] or --input-file argument."
    ),
    short_help="Retrieve results for one or more retrosynthesis jobs.",
    no_args_is_help=True,
)
def retrieve_job_results(
    context: Context,
    output_file: typing.Annotated[
        pathlib.Path,
        typer.Option(
            "--output-file",
            "-o",
            default_factory=_default_output_file,
            show_default=False,
            help=(
                "Specified JSON output file for writing results to. Defaults to "
                "an ISO-8601 formatted filename in the working directory."
            ),
            writable=True,
            dir_okay=False,
            file_okay=True,
            resolve_path=True,
        ),
    ],
    job_id: typing.Annotated[
        str | None,
        typer.Argument(
            help="Single retrosynthesis job ID to retrieve the status for.",
            callback=_job_id_callback,
            metavar="[JOB_ID]",
        ),
    ] = None,
    input_file: typing.Annotated[
        pathlib.Path | None,
        typer.Option(
            "--input-file",
            "-i",
            help="Input file of line-delimited job IDs to retrieve results for.",
            callback=_job_ids_file_callback,
            dir_okay=False,
            file_okay=True,
            exists=True,
            resolve_path=True,
        ),
    ] = None,
) -> None:
    """
    Retrieve results for one or more retrosynthesis jobs by the id. The
    jobs cannot distinguish between missing or incomplete; provide user
    feedback on if a job cannot retrieve results. Write results as json
    to an output file.

    Args:
        context (Context): App runtime context.
        output_file (pathlib.Path, optional): Output path for writing
            json job results to.
        job_id (str, optional): Single job id to retrieve results for.
        input_file (pathlib.Path, optional): Input file path containing
            line-delimited job ids to retrieve results for.

    Raises:
        typer.Exit: File overwrite is not granted, returns zero status.
        typer.BadParameter: Either both or neither the `job_id` and
            `input_file` parameters are provided.
    """
    controller = RetroJobController(context)

    # xor on the input file and job id parameters to enforce only either
    # a mini-batch operation or a single job lookup to get results.
    if (job_id and input_file) or (not job_id and not input_file):
        raise typer.BadParameter('Provide one of "--input-file" or "[JOB_ID]".')

    # confirm the operation if the output path already exists and is ok
    # with overwriting the filepath.
    if output_file.exists():
        prompt: str = f"[warn]! Do you want to overwrite the file: {output_file}?"
        if not rich.prompt.Confirm.ask(prompt, console=console):
            raise typer.Exit(0)

    # prepare all job ids from the mini-batch or single argument input as
    # a list of job ids to build a progress bar for retrieving results.
    ids: list[str] = [job_id] if job_id else []
    if input_file:
        ids = list(set([x.strip() for x in input_file.open().readlines()]))
        console.print(f"[success][not b]✓ Found {len(ids)} unique job id(s).")

    # iterate over each job id and collect the id and optional result as
    # a tuple pair; provide feedback on any results that were missing
    # or possibly incomplete.
    results: list[tuple[str, dict | None]] = []
    with rich.progress.Progress(transient=True) as progress:
        for x in progress.track(ids, description="Retrieving results"):
            result: dict | None = controller.retrieve_job_result(x)
            results.append((x, result))
    for x in [job_id for job_id, result in results if result is None]:
        console.print(f"[not b][warn]! Retrosynthesis job not found or incomplete: {x}")

    # output a final completion summary of collected jobs that were
    # completed with results and write json to the output file.
    if len(completed := [x for _, x in results if x is not None]) > 0:
        console.print(f"[success][not b]✓ Found {len(completed)} completed job(s).")
        json.dump(completed, output_file.open("w"), indent=2)
        filesize: str = formatters.format_filesize(os.path.getsize(output_file))
        console.print(f"[success][not b]✓ Results saved to {output_file} ({filesize})")
    else:
        console.print("[warn]! Found 0 completed job(s).")


# region command: list -------------------------------------------------


# status enum is required when specifying valid options for a string
# typer option parameter.
class Status(str, enum.Enum):
    """Status enumeration."""

    COMPLETED = "completed"
    FAILED = "failed"
    SUBMITTED = "submitted"
    PROCESSING = "processing"


@app.command(
    "list",
    help=(
        "Retrieve a page of retrosynthesis jobs. Displays select search "
        "parameters and a binary synthesizability flag. Use <pendingai "
        "retro job result> to retrieve retrosynthetic routes of completed jobs."
    ),
    short_help="Retrieve a page of retrosynthesis jobs.",
)
def retrieve_job_list(
    context: Context,
    page: typing.Annotated[
        int,
        typer.Option(
            "--page",
            help="Page number being fetched.",
            show_choices=False,
            show_default=False,
            metavar="INTEGER",
            min=1,
        ),
    ] = 1,
    page_size: typing.Annotated[
        int,
        typer.Option(
            "--page-size",
            help="Number of results per page.",
            callback=_validate_page_size,
            show_default=False,
            metavar="INTEGER",
            min=5,
            max=25,
        ),
    ] = 10,
    filter_status: typing.Annotated[
        Status | None,
        typer.Option(
            "--status",
            help="Optional filter for matching status.",
        ),
    ] = None,
    render_json: typing.Annotated[
        bool,
        typer.Option(
            "--json",
            help="Render output as JSON.",
            is_flag=True,
        ),
    ] = False,
) -> None:
    """
    Retrieve a paginated collection of retrosynthesis jobs for a set of
    optional filter conditions and page lookup parameters.

    Args:
        page (int, optional): Page number being fetched.
        page_size (int, optional): Page size for the response.
        filter_status (str, optional): Status to filter jobs by.
        render_json (bool, optional): Render output as json.

    Raises:
        typer.Exit: Exceeded page limit of results or no results were
            given in the page response from the api layer.
    """
    controller = RetroJobController(context)
    status: str | None = filter_status.value if filter_status else None
    page_data: JobPage = controller.retrieve_jobs(page, page_size, status)

    # capture the case where the page limit has been exceeded by --page
    # or if the page data contains no job results; exit both with non-
    # zero exit status.
    if len(page_data.data) == 0:
        console.print("[yellow]! No results found with the given filter.")
        raise typer.Exit(1)

    if render_json:
        console.print_json(data=[x.model_dump(mode="json") for x in page_data.data])

    else:
        # instantiate the table of results to display to the user; add
        # all columns and global column formatting; avoid adding width
        # constraints to impact when smaller screens are used.
        table = rich.table.Table(
            rich.table.Column("ID"),
            rich.table.Column("Created"),
            rich.table.Column("Molecule", max_width=50),
            rich.table.Column("Status"),
            rich.table.Column("Synthesizable", justify="right"),
            box=rich.table.box.SQUARE,
            caption=f"Page {page} of {'many' if page_data.has_more else page}",
        )

        for result in page_data.data:
            # map the status value into a colour; map synthesis outcome
            # depending on whether the job is complete and add colour.
            synthesizable: str = (
                "[green]Yes"
                if len(result.routes) > 0
                else ("[red]No" if result.status == "completed" else "[dim i]n/a")
            )
            result.status = {
                "completed": "[reverse green]",
                "failed": "[reverse red]",
                "processing": "[reverse yellow]",
                "submitted": "[reverse]",
            }[result.status] + result.status.title()
            table.add_row(
                result.id,
                formatters.localize_datetime(result.created).isoformat(" ", "seconds"),
                result.query,
                result.status,
                synthesizable,
            )

        console.print(table)


# region command: delete ----------------------------------------------


@app.command(
    "delete",
    help="Delete a retrosynthesis job.",
    short_help="Delete a retrosynthesis job.",
    no_args_is_help=True,
)
def delete_job(
    context: Context,
    job_id: typing.Annotated[
        str,
        typer.Argument(
            help="Retrosynthesis job ID to delete.",
            callback=_job_id_callback,
            metavar="JOB_ID",
        ),
    ],
    render_json: typing.Annotated[
        bool,
        typer.Option(
            "--json",
            help="Render output as JSON.",
            is_flag=True,
        ),
    ] = False,
) -> None:
    """
    Delete a retrosynthesis job by id and provide the feedback in a
    readable format to the user; capture when the job id does not exist
    or if the delete command fails.

    Args:
        context (Context): App runtime context.
        job_id (str): Retrosynthesis job id to delete.
        render_json (bool, optional): Render output as json.

    Raises:
        typer.Exit: Retrosynthesis job id was not found.
    """
    controller = RetroJobController(context)
    success: bool = controller.delete_job(job_id)

    if render_json:
        console.print_json(data={"success": success})
    else:
        if not success:
            console.print(f"[red]! Failed to delete retrosynthesis job: {job_id}")
            raise typer.Exit(1)
        console.print(f"[success]✓ Retrosynthesis job deleted successfully: {job_id}")


# region command: depict -----------------------------------------------


@app.command(
    "depict",
    help=(
        "Generate depictions of retrosynthetic routes for jobs. "
        "Specify either a [JOB_ID] or --input-file containing job IDs. "
        "PDFs are saved as 'job_<id>.pdf' in the current directory "
        "unless an output path is provided."
        "\n\n"
        "NOTE: Experimental feature. Feedback welcome at 'support@pending.ai'."
    ),
    short_help="Get route depictions for one or more retrosynthesis jobs.",
    no_args_is_help=True,
)
def depict_retrosynthesis_results(
    context: Context,
    job_id: typing.Annotated[
        str | None,
        typer.Argument(
            help="Specify a single job ID to generate route depictions.",
            callback=_job_id_callback,
            metavar="[JOB_ID]",
        ),
    ] = None,
    job_ids_file: typing.Annotated[
        pathlib.Path | None,
        typer.Option(
            "--input-file",
            "-i",
            help="Path to a file containing multiple job IDs (one per line) to process.",
            callback=_job_ids_file_callback,
            resolve_path=True,
            file_okay=True,
            dir_okay=False,
            exists=True,
        ),
    ] = None,
    output_directory: typing.Annotated[
        pathlib.Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory where generated files with depictions will be saved.",
            callback=_output_dir_callback,
            show_default=False,
            file_okay=False,
            dir_okay=True,
        ),
    ] = pathlib.Path.cwd(),
    force_overwrite: typing.Annotated[
        bool,
        typer.Option(
            "--force",
            help="Overwrite existing output files without confirmation.",
            is_flag=True,
        ),
    ] = False,
) -> None:
    """
    Request pdfs for a collection of job ids for any retrosynthetic
    routes and write to a local output directory with standard output
    feedback for the user.

    Args:
        context (Context): App runtime context.
        job_id (str, optional): A single command-line job id.
        job_ids_file (pathlib.Path, optional): File with job ids.
        output_directory (pathlib.Path, optional): Results directory.
        force_overwrite (bool, optional): Force overwrite existing pdfs.

    Raises:
        typer.BadParameter: Either both or neither a job id or job id
            file are given as input.
    """
    controller = RetroJobController(context)

    # xor on the input file and job id parameters to enforce only either
    # a mini-batch operation or a single job lookup to get pdfs.
    if (job_id and job_ids_file) or (not job_id and not job_ids_file):
        raise typer.BadParameter('Provide one of "--input-file" or "[JOB_ID]".')

    # prepare all job ids from the mini-batch or single argument input as
    # a list of job ids to iterate over for retrieving pdfs.
    ids: list[str] = [job_id] if job_id else []
    if job_ids_file:
        ids = list(set([x.strip() for x in job_ids_file.open().readlines()]))
        console.print(f"[success][not b]✓ Found {len(ids)} unique job id(s).")

    # iterate over each job id and write the pdf to the specified id
    # filepath; check if wanting to overwrite a file and skip if not.
    for x in ids:
        path: pathlib.Path = output_directory / f"job_{x}.pdf"
        prompt: str = f"[warn]! Do you want to overwrite: {path}?"
        if path.exists():
            if not (force_overwrite or rich.prompt.Confirm.ask(prompt, console=console)):
                console.print(f"[warn]! Skipping PDF generation for job: {x}")
                continue
        controller.retrieve_job_pdf(x, path)
