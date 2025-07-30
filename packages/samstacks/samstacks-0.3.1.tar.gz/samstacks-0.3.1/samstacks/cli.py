"""
Command-line interface for samstacks.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

import click

from . import __version__
from .core import Pipeline
from .exceptions import SamStacksError
from . import ui  # Import the new ui module

from rich.logging import RichHandler


def setup_logging(debug: bool, quiet: bool) -> None:
    """Configure logging based on verbosity flags."""
    samstacks_level = logging.INFO
    boto_level = logging.WARNING

    if quiet:
        samstacks_level = logging.ERROR
        boto_level = logging.ERROR
        ui.set_verbose_mode(False)  # Ensure ui module also respects quiet
    elif debug:
        samstacks_level = logging.DEBUG
        boto_level = logging.DEBUG
        ui.set_verbose_mode(True)
    else:
        ui.set_verbose_mode(False)

    logging.getLogger("samstacks").setLevel(samstacks_level)
    logging.getLogger("boto3").setLevel(boto_level)
    logging.getLogger("botocore").setLevel(boto_level)
    logging.getLogger("urllib3").setLevel(boto_level)

    # Minimal RichHandler config; primary output via ui module
    logging.basicConfig(
        level=samstacks_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                show_path=debug,
                show_level=debug,
                show_time=debug,
                markup=True,
            )
        ],
    )


@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
@click.option(
    "--debug", "-d", is_flag=True, help="Enable debug logging and verbose output."
)  # Added -d short flag
@click.option("--quiet", is_flag=True, help="Suppress all output except errors.")
@click.pass_context
def cli(ctx: click.Context, debug: bool, quiet: bool) -> None:
    """Deploy a pipeline of AWS SAM stacks using a YAML manifest."""  # Simplified description
    ctx.ensure_object(dict)
    # Store debug/quiet state for potential use in other commands or core logic if needed directly
    # However, ui.VERBOSE_MODE and logger levels should be the primary drivers of verbosity.
    ctx.obj["debug"] = debug
    ctx.obj["quiet"] = quiet
    setup_logging(debug, quiet)

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())  # Click's default help is fine
        ctx.exit()


@cli.command()
@click.argument("manifest_file", type=click.Path(exists=True, path_type=Path))
@click.option("--region", help="AWS region (overrides manifest settings)")
@click.option("--profile", help="AWS profile (overrides manifest settings)")
@click.option(
    "--input",
    "-i",
    "inputs_kv",  # Store in a variable named 'inputs_kv'
    multiple=True,
    type=str,
    help="Provide input values for pipeline inputs defined in `pipeline_settings.inputs`. "
    "Format: name=value. Can be used multiple times (e.g., -i name1=value1 -i name2=value2). "
    "Note: Values containing '=' will only split on the first occurrence.",
)
@click.option(
    "--auto-delete-failed",
    is_flag=True,
    help="Proactively delete ROLLBACK_COMPLETE stacks and old 'No updates' changesets.",
)
@click.pass_context
def deploy(
    ctx: click.Context,
    manifest_file: Path,
    region: Optional[str],
    profile: Optional[str],
    inputs_kv: tuple[
        str, ...
    ],  # Changed from list to tuple as per click's multiple=True
    auto_delete_failed: bool,
) -> None:
    """Deploy stacks defined in the manifest file."""
    is_debug = ctx.obj.get("debug", False)
    parsed_inputs: dict[str, str] = {}
    for item in inputs_kv:
        if "=" not in item:
            raise click.BadParameter(f"Input '{item}' must be in 'name=value' format.")

        name, value = item.split("=", 1)
        if not name.strip():
            raise click.BadParameter(
                f"Input '{item}' must be in 'name=value' format, and 'name' cannot be empty."
            )

        if not value.strip():
            raise click.BadParameter(
                f"Input '{item}' has an empty value. Use 'name=value' format with a non-empty value, or omit the input to use defaults."
            )

        parsed_inputs[name] = value

    try:
        # Pass parsed_inputs to Pipeline.from_file to provide user-defined inputs.
        pipeline = Pipeline.from_file(
            manifest_file, cli_inputs=parsed_inputs
        )  # parsed_inputs is now finalized as part of the pipeline execution path.

        if region:
            pipeline.set_global_region(region)
        if profile:
            pipeline.set_global_profile(profile)

        pipeline.deploy(auto_delete_failed=auto_delete_failed)

        ui.success("Pipeline deployment completed successfully!")

    except SamStacksError as e:
        ui.error("Pipeline error", details=str(e), exc_info=e if is_debug else None)
        sys.exit(1)
    except Exception as e:
        ui.error(
            "Unexpected pipeline error",
            details=str(e),
            exc_info=e if is_debug else None,
        )
        sys.exit(1)


@cli.command()
@click.argument("manifest_file", type=click.Path(exists=True, path_type=Path))
@click.pass_context
def validate(ctx: click.Context, manifest_file: Path) -> None:
    """Validate the manifest file syntax and structure."""
    is_debug = ctx.obj.get("debug", False)
    try:
        pipeline = Pipeline.from_file(manifest_file)
        pipeline.validate()
        ui.success("Manifest file is valid!")

    except SamStacksError as e:
        ui.error("Validation error", details=str(e), exc_info=e if is_debug else None)
        sys.exit(1)
    except Exception as e:
        ui.error(
            "Unexpected validation error",
            details=str(e),
            exc_info=e if is_debug else None,
        )
        sys.exit(1)


def main() -> None:
    """Entry point for the CLI."""
    cli()
