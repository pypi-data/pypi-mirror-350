from flask import Flask, render_template, send_from_directory
import webbrowser
import waitress
from pathlib import Path
import json


def create_flask_app(html: str, filepath: str, **kwargs) -> Flask:
    """
    Create a Flask app that takes a file as input.

    To get the path of the file, use `/data` in your html file.

    You can pass as many variables as you want with the **kwargs arg. For example :

    ```
    app = create_flask_app(html="index.html", filepath="test.csv", arg1=0)
    ```

    You can get `arg1` in Javascript with :

    ```
    const arg1 = "{{ arg1 }}"
    ```

    Args:
        html (str): html filename.
        filepath (str): Path to the file.

    Returns:
        Flask : Flask app
    """
    app = Flask("moonframe")

    @app.route("/")
    def index():
        return render_template(html, **kwargs)

    @app.route("/data")
    def get_data():
        file = Path(filepath).resolve()
        return send_from_directory(file.parent, file.name)

    return app


def create_flask_app_dict(html: str, data: dict, **kwargs) -> Flask:
    """
    Create a Flask app that takes a dict as input.

    Get your dict in HTML with:
    ```
    <script>
        const data = JSON.parse('{{ data | safe }}')
    </script>
    ```
    You can pass as many variables as you want with the **kwargs arg. For example :

    ```
    app = create_flask_app(html="index.html", filepath="test.csv", arg1=0)
    ```

    You can get `arg1` in Javascript with :

    ```
    const arg1 = "{{ arg1 }}"
    ```

    Args:
        html (str): html filename.
        data (dict): Input dict.

    Returns:
        Flask : Flask app
    """
    app = Flask("moonframe")

    @app.route("/")
    def index():
        return render_template(html, data=json.dumps(data), **kwargs)

    return app


def serve_app(app: Flask, port: str = "5000") -> None:  # pragma: no cover
    """Serve any Flask app with waitress (production server)

    Args:
        app (Flask): Flask app.
        port (str): Port.
    """
    webbrowser.open(f"http://127.0.0.1:{port}")
    waitress.serve(app, port=port)
