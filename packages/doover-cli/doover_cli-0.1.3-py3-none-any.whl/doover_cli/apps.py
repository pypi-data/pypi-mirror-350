import json
import os
import pathlib
import re
import shutil
import socket
import subprocess

from urllib.parse import urlencode
from pathlib import Path
from enum import Enum
from typing_extensions import Annotated

import requests
import typer

from .utils.apps import get_app_directory, call_with_uv

CHANNEL_VIEWER = "https://my.d.doover.com/channels/dda"
TEMPLATE_REPO = "https://api.github.com/repos/getdoover/app-template/tarball/main"
AUTH_TOKEN = "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"

VALID_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9-_]+$")
IP_PATTERN = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
HOSTNAME_PATTERN = re.compile(r"(?P<host>[a-zA-Z0-9-_]?)-?(?P<serial>[0-9a-zA-Z]{6})")

app = typer.Typer(no_args_is_help=True)


class AppType(Enum):
    DEVICE = "device"
    INTEGRATION = "integration"


class SimulatorType(Enum):
    MODBUS = "modbus"
    PLATFORM = "platform"
    MIXED = "mixed"
    CHANNELS = "channels"


def extract_archive(archive_path: pathlib.Path):
    """Extract an archive (tar, gz, zip) to a temporary directory and return the path to the extracted directory.

    Accounts for archives which rename the directory e.g. Github archives.
    """
    # this supports either tar, gz or zip files.
    extract_path = archive_path
    while extract_path.suffix in {".tar", ".gz", ".zip"}:
        extract_path = extract_path.with_suffix("")

    shutil.unpack_archive(archive_path, extract_path)
    if len(os.listdir(extract_path)) == 1:
        # get the inner folder
        extract_path = next(extract_path.iterdir())

    return extract_path


@app.command()
def create(
    name: Annotated[str, typer.Option(prompt="What is the name of your app?")],
    description: Annotated[
        str,
        typer.Option(
            prompt="Description (tell me a little about your app - what does it do?)"
        ),
    ],
    type_: Annotated[AppType, typer.Option(prompt=True)] = AppType.DEVICE.value,
    simulator: Annotated[
        SimulatorType, typer.Option(prompt=True)
    ] = SimulatorType.MIXED.value,
    cicd: Annotated[
        bool,
        typer.Option(prompt="Do you want to enable CI/CD?", confirmation_prompt=True),
    ] = True,
):
    """Create an application with a walk-through wizard.

    This will create a new directory with the name of your app, and populate it with a template application.
    """
    name_as_path = name.lower().replace(" ", "-").replace("_", "-")
    if not VALID_NAME_PATTERN.match(name_as_path):
        raise ValueError(
            f"Invalid app name: {name}. Only alphanumeric characters, dashes, and underscores are allowed."
        )

    path = Path(name_as_path)
    if path.exists():
        typer.confirm("Path already exists. Do you want to overwrite it?", abort=True)
        shutil.rmtree(path)

    name_as_pascal_case = "".join(word.capitalize() for word in name_as_path.split("-"))
    name_as_snake_case = "_".join(name_as_path.split("-"))

    print("Fetching template repository...")
    data = requests.get(
        TEMPLATE_REPO, headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
    )
    if data.status_code != 200:
        raise Exception(f"Failed to fetch template repository: {data.status_code}")

    tmp_path = Path("/tmp/app-template.tar.gz")
    tmp_path.write_bytes(data.content)
    # Extract the tarball
    extracted_path = extract_archive(tmp_path)
    shutil.move(extracted_path, path)

    print("Renaming template files...")
    for file in path.rglob("*.py"):
        file: pathlib.Path
        try:
            contents: str = file.read_text()
        except FileNotFoundError:
            print(f"Something strange happened while correcting {file.name}")
            continue

        replacements = [
            ("SampleConfig", f"{name_as_pascal_case}Config"),
            ("SampleApplication", f"{name_as_pascal_case}Application"),
            ("SampleUI", f"{name_as_pascal_case}UI"),
            ("SampleState", f"{name_as_pascal_case}State"),
            ("sample_application", name_as_snake_case),
        ]

        for old, new in replacements:
            contents = contents.replace(old, new)

        file.write_text(contents)

    # write config
    print("Updating config...")
    config_path = path / "application" / "app_config.py"
    subprocess.run(["python", str(config_path)])

    content = json.loads((path / "doover_config.json").read_text())
    del content["sample_application"]
    content[str(name_as_snake_case)].update(
        {
            "name": name,
            "description": description,
            "type": type_.value,
            "simulator": simulator.value,
        }
    )
    config_path.write_text(json.dumps(content))

    if cicd is False:
        print("Disabling CI/CD workflows")
        shutil.move(
            path / ".github" / "workflows", path / ".github" / "workflows_disabled"
        )

    print("Done!")


@app.command()
def run(
    remote: str = typer.Argument(None),
    docker_args: list[str] = typer.Argument(None),
    port: int = 2375,
):
    """Runs an application. This assumes you have a docker-compose file in the `simulator` directory."""
    root_fp = get_app_directory()

    print(f"Running application from {root_fp}")
    if not (root_fp / "simulators" / "docker-compose.yml").exists():
        raise FileNotFoundError(
            "docker-compose.yml not found. Please ensure there is a docker-compose.yml file in the simulators directory."
        )

    if Path("/usr/bin/docker").exists():
        docker_path = "/usr/bin/docker"
    elif Path("/usr/local/bin/docker").exists():
        docker_path = "/usr/local/bin/docker"
    else:
        raise RuntimeError(
            "Couldn't find docker installation. Make sure it is installed, in your PATH and try again."
        )

    if remote:
        match = HOSTNAME_PATTERN.match(remote)
        if match:
            remote = f"{match.group('host') or 'doovit'}-{match.group('serial')}.local"

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((remote, port))
        except ConnectionRefusedError:
            typer.confirm(
                "Connection refused. Do you want me to try and disable the firewall?",
                default=True,
                abort=True,
            )

            try:
                from paramiko import SSHClient
            except ImportError:
                raise ImportError(
                    "paramiko not found. Please install it with pip install paramiko"
                )

            username = typer.prompt(
                f"Please enter the username for {remote}:", default="doovit"
            )
            password = typer.prompt(
                "Please enter the password (skip for SSH keys):",
                default="doovit",
                hide_input=True,
            )

            client = SSHClient()
            client.load_system_host_keys()
            client.connect(remote, username=username, password=password)
            stdin, stdout, stderr = client.exec_command("dd dfw down")
            print(stdout.read().decode())
            print(stderr.read().decode())

        host_args = (f"--host={remote}:{port}",)
    else:
        host_args = ()

    if docker_args:
        # feel free to add more
        compose_flags = (
            "abort-on-container-exit",
            "abort-on-container-failure",
            "no-recreate",
            "remove-orphans",
            "force-recreate",
            "timeout",
            "detatch",
            "pull",
            "quiet-pull",
        )
        docker_args = [
            f"--{arg}" if arg in compose_flags else arg for arg in docker_args
        ]
    else:
        docker_args = []

    # docker compose -f docker-compose.pump-aquamonix.yml up --build --abort-on-container-exit
    os.execl(
        docker_path,
        "docker",
        *host_args,
        "compose",
        "-f",
        str(root_fp / "simulators" / "docker-compose.yml"),
        "up",
        "--build",
        *docker_args,
    )


@app.command()
def deploy():
    """Deploy an application."""
    pass


@app.command()
def channels(host: str = "localhost", port: int = 49100):
    """Open the channel viewer in your browser."""
    import webbrowser

    url = CHANNEL_VIEWER + "?" + urlencode({"local_url": f"http://{host}:{port}"})
    webbrowser.open(url)


@app.command()
def test():
    """Run tests on the application. This uses pytest and requires uv to be installed."""
    call_with_uv("pytest")


@app.command()
def lint(
    fix: Annotated[
        bool,
        typer.Option(help="The --fix option passed to ruff to fix linting failure."),
    ] = False,
):
    """Run linter on the application. This uses ruff and requires uv to be installed."""
    args = ["ruff", "check"]
    if fix:
        args.append("--fix")

    call_with_uv(*args)
