#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import pathlib
import typing

import rich
import rich.progress
import rich.prompt
import rich.table
import typer

from pendingai import config
from pendingai.commands.generator.controller import GeneratorController
from pendingai.commands.generator.models import Model
from pendingai.context import Context

console = rich.console.Console(theme=config.RICH_CONSOLE_THEME, soft_wrap=True)

app = typer.Typer(
    name="generator",
    help=(
        "Generative solutions for novel molecule identification and "
        "similarity searches for supplementing synthetic screening of "
        "targeted structures. For more information refer to the "
        "documentation with <pendingai docs>."
    ),
    short_help="Generative solutions for novel molecule identification.",
    no_args_is_help=True,
    add_completion=False,
    pretty_exceptions_show_locals=False,
    rich_markup_mode=None,
    context_settings={"max_content_width": config.CONSOLE_WIDTH},
)


# region command: models -----------------------------------------------


@app.command(
    "models",
    help=(
        "List molecule generator models available for use."
        "\n\nUnique models IDs are required for specifying which model "
        "to use when sampling. If no models are available please "
        "contact support."
    ),
    short_help="List molecule generator models.",
)
def retrieve_models(
    context: Context,
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
    Retrieve a list of molecule generator models stored in the
    database and output with relevant information for the user.

    Args:
        context (Context): App runtime context.
        render_json (bool, optional): Output results as json.

    Raises:
        typer.Exit: No molecule generator models were returned.
    """
    # request generator models from the api client
    controller = GeneratorController(context)
    items: list[tuple[Model, str]] = controller.retrieve_models()

    # capture the edge case where no engines exist from the response by
    # the api client; give a non-zero exit status.
    if len(items) == 0:
        console.print("[warn]! No generator models available.")
        raise typer.Exit(1)

    # output the generator model data either as json data if the
    # --json flag is given, else as a table output.
    if render_json:
        console.print_json(
            data=[x[0].model_dump(mode="json") | {"status": x[1]} for x in items]
        )
    else:
        table = rich.table.Table(
            rich.table.Column("ID"),
            rich.table.Column("Name"),
            rich.table.Column("Version", style="dim"),
            rich.table.Column("Status"),
            box=rich.table.box.SQUARE,
        )
        items.sort(key=lambda x: x[1], reverse=True)
        for model, status in items:
            table.add_row(
                model.id,
                model.name if model.name else "[dim i]unknown",
                model.version if model.version else "[dim i]unknown",
                status.title(),
            )
        console.print(table)


# region command: sample -----------------------------------------------


def _generate_sample_output_file() -> pathlib.Path:
    fix: str = "pendingai_generator_sample"
    cwd: pathlib.Path = pathlib.Path.cwd()
    count: int = sum([1 for x in cwd.iterdir() if x.name.startswith(fix)])
    return cwd / f"{fix}_{count + 1:>03d}.smi"


@app.command(
    "sample",
    help=(
        "Sample molecule SMILES from a generator model and output "
        "results to a file. Specify a model id to perform sampling "
        "against a particular molecule generator model."
    ),
    short_help="Sample molecules from a generator model.",
)
def sample(
    context: Context,
    output_file: typing.Annotated[
        pathlib.Path,
        typer.Option(
            "-o",
            "--output-file",
            default_factory=_generate_sample_output_file,
            show_default=False,
            help=(
                "Output SMILES filepath to store sampled molecules. "
                "Defaults to 'pendingai_generator_sample_XXX.smi' in "
                "the current working directory."
            ),
            writable=True,
            dir_okay=False,
            file_okay=True,
            resolve_path=True,
        ),
    ],
    samples: typing.Annotated[
        int,
        typer.Option(
            "-n",
            "--num-samples",
            help="Number of samples to generate. Defaults to 500.",
            show_choices=False,
            show_default=False,
            metavar="INTEGER",
            min=1,
            max=1_000_000,
        ),
    ] = 500,
    append_flag: typing.Annotated[
        bool,
        typer.Option(
            "-a",
            "--append",
            help=(
                "Flag to append generated molecules to an existing "
                "file and skip the prompt for overwriting files."
            ),
            is_flag=True,
        ),
    ] = False,
    model_id: typing.Annotated[
        str | None,
        typer.Option(
            "--model",
            help=(
                "A specified model id used for the sampling process. "
                "Otherwise sample via any available generator model."
            ),
        ),
    ] = None,
) -> None:
    # sample molecules either randomly or from a selected model until a
    # given number of unique samples are produced overall by iteratively
    # requesting molecules from the api layer
    controller = GeneratorController(context)

    # validate output file and append flags to correctly prepare where
    # sampled molecules are written with an output io wrapper flag
    output_file_flag: str = "w"
    prompt: str = f"[warn]? Would you like to overwrite the file: {output_file.name}"
    if output_file.exists() and append_flag:
        console.print(f"[warn]! Appending results to file: {output_file.name}")
        output_file_flag = "a"
    elif output_file.exists() and not rich.prompt.Confirm.ask(prompt, console=console):
        console.print(f"[warn]! See --append for appending to file: {output_file.name}")
        raise typer.Exit(0)
    writer: typing.Any = output_file.open(output_file_flag)

    # build progress bar to track sampling progress, note that file
    # content is being written on each iteration and does not need to
    # wait until the iteration loop is complete
    progress: rich.progress.Progress = rich.progress.Progress(
        rich.progress.SpinnerColumn(finished_text=""),
        *rich.progress.Progress.get_default_columns(),
        rich.progress.TimeElapsedColumn(),
        transient=True,
    )

    # perform sampling until the requested number of samples is finished
    # and uniquely written to file in minibatches
    limit: int = 500
    all_samples: set[str] = set()
    with progress:
        task: rich.progress.TaskID = progress.add_task("Sampling...", total=samples)
        while not progress.finished:
            result: list[str] = controller.generate_sample(model_id, limit)
            sample: set[str] = set(result) - all_samples
            output: list[str] = [x + "\n" for x in sample][: samples - len(all_samples)]
            all_samples = all_samples.union(output)
            writer.writelines(output)
            progress.update(task, advance=len(sample))

    console.print(f"[success]Sampled {len(all_samples)} molecules: {output_file.name}")
