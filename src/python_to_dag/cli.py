import click
import sys
import os
from pathlib import Path
from .parser import PipelineParser
from .generator import PipelineGenerator


@click.group()
def cli():
    """Python to DAG Conversion Tool."""
    pass


@cli.command()
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True),
    help="Path to pipeline definition file (YAML).",
)
@click.option(
    "--out",
    "-o",
    default="dags",
    type=click.Path(),
    help="Output directory for generated DAGs.",
)
def build(input, out):
    """Convert pipeline definition to Airflow DAG."""
    try:
        # 1. Parse
        click.echo(f"Parsing: {input}")
        parser = PipelineParser()
        pipeline_ir = parser.parse_file(input)

        # 2. Validate (Implicit in parsing)
        # TODO: Add specific validator step (P2-1)

        # 3. Generate
        out_dir = Path(out)
        out_path = out_dir / f"{pipeline_ir.pipeline_id}.py"
        click.echo(f"Generating: {out_path}")

        generator = PipelineGenerator()
        generator.generate(pipeline_ir, str(out_path))

        click.echo(click.style("Build Success!", fg="green"))

    except Exception as e:
        click.echo(click.style(f"Build Failed: {e}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--input",
    "-i",
    required=True,
    type=click.Path(exists=True),
    help="Path to pipeline definition file (YAML).",
)
def validate(input):
    """Validate pipeline definition without generating code."""
    try:
        click.echo(f"Validating: {input}")
        parser = PipelineParser()
        # Parsing triggers Pydantic validation
        pipeline_ir = parser.parse_file(input)

        click.echo(
            click.style(f"Validation Success: {pipeline_ir.pipeline_id}", fg="green")
        )

    except Exception as e:
        click.echo(click.style(f"Validation Failed: {e}", fg="red"), err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
