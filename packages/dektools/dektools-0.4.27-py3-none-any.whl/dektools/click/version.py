import sys
import typer

app = typer.Typer(add_completion=False)


@app.command()
def extract(version):
    from ..version import version_extract
    sys.stdout.write(version_extract(version))
