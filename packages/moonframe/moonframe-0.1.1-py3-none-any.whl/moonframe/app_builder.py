from moonframe.application import create_flask_app, create_flask_app_dict
from flask import Flask
from pathlib import Path
import json


def build_app_scatter(filepath: str, delimiter: str = ";") -> Flask:
    """Build a Flask app for the scatter plot.
    Take a CSV file as input.

    Args:
        filepath (str): Path to the CSV input file.
        delimiter (str, optional): Separator used in the CSV file. Defaults to ";".

    Returns:
        Flask: Flask app. Serve with "moonframe.serve_app()"
    """
    return create_flask_app("scatter.html", filepath=filepath, delimiter=delimiter)


def build_app_treeshow(filepath: str, repo_path=str) -> Flask:
    """Build a Flask app to explore repository with a circular packing graph.
    Made for Marauders map tree-show : `mmap tree-showjs`
    Take a JSON file as input.

    Args:
        filepath (str): Path to the .json.
        repo_path (str): Path to the repository. Defaults to str.

    Returns:
        Flask: Flask app. Serve with "moonframe.serve_app()"
    """
    repo = Path(repo_path)
    return create_flask_app(
        "nobvisualjs.html",
        filepath=filepath,
        repository=True,
        repo_name=repo.name,
        repo_path=repo.parent,
    )


def build_app_nobvisual(data: dict, title: str, legend: dict = None) -> Flask:
    """Build a Flask app to explore files with a circular packing graph.
    Made for nobvisual.

    Take as input a nested structure with id, text, color, datum and children key. like this :
    [
        {
            "id": "0",
            "text": "my root",
            "color": "red",
            "children": [
                {
                    "id": "01",
                    "text": "children1",
                    "color": "green",
                    "children": [],
                    "datum": 1.0,
                },
                {
                    "id": "02",
                    "text": "children2",
                    "color": "green",
                    "children": [],
                    "datum": 1.0,
                }
            "datum": 1.0
        }
    ]

    Args:
        data (dict) : Input dict from nobvisual.
        title (str): Title of the graph.
        legend (dict): Custom legend.

    Returns:
        Flask: Flask app. Serve with "moonframe.serve_app()"
    """
    return create_flask_app_dict(
        "nobvisualjs.html",
        data=data,
        repository=False,
        title=title,
        legend=json.dumps(legend),
    )
