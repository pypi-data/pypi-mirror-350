from typer import Typer

from cmitai.cli.commands import app as cli_app

app = Typer()
app.add_typer(cli_app, name="generate")

if __name__ == "__main__":
    app()
