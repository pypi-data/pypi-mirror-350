import time
import webbrowser
from argparse import ArgumentParser
from pathlib import Path
from threading import Thread

import marimo
from fastapi import FastAPI

# Create a marimo asgi app
server = (
    marimo.create_asgi_app()
    .with_app(path="", root=str(Path(__file__).with_name("index.py")))
    .with_app(path="/orbitals", root=str(Path(__file__).with_name("orbitals.py")))
    .with_app(path="/tddft", root=str(Path(__file__).with_name("tddft.py")))
    .with_app(path="/soc_tddft", root=str(Path(__file__).with_name("soc_tddft.py")))
)

# Create a FastAPI app
app = FastAPI()

app.mount("/", server.build())


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("output_file", type=str, default="")
    return parser.parse_args()


def open_in_browser():
    # Give the server a second (or two) to start
    time.sleep(2)
    webbrowser.open("http://localhost:8000")


def serve_app():
    import uvicorn

    _args = parse_args()

    # Start browser in a different thread to not block the server
    Thread(target=open_in_browser).start()
    uvicorn.run(app, host="localhost", port=8000)


# Run the server
if __name__ == "__main__":
    serve_app()
