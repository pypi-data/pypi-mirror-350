import sys
import typer

app = typer.Typer(add_completion=False)


@app.command()
def auth(url, username, password=None):
    from ..web.url import Url
    sys.stdout.write(Url.new(url).replace(username=username, password=password).value)
