import os
import sys

import typer

app = typer.Typer(name="scratch")

os.environ['SKIPPY'] = 'skip'

import check_import  # noqa

print(f"{sys.argv = }")


@app.command()
def start():

    print(f"{sys.argv = }")
    print(f"{os.getenv('SKIPPY') = }")


@app.command()
def end():

    print("Endgame...")


if __name__ == '__main__':
    app()
