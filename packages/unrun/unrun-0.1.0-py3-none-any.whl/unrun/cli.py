import os, yaml, argparse, subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax


def error(message: str, console: Console, title: str = "Error"):
    console.print(
        Panel(
            Text(message, style="bold red"),
            title=Text(title, style="bold red")
        )
    )


def load(file: str, console: Console) -> dict:
    try:
        with open(file, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        error(
            f"`{file}` not found in the current directory.",
            console
        )
        return None
    except yaml.YAMLError as e:
        error(
            f"Error parsing {file}: {e}",
            console
        )
        return None


def parse(key: str, object: dict, console: Console) -> str:
    keys = key.split(".")
    command = object
    for k in keys:
        if isinstance(command, dict) and k in command:
            command = command[k]
        else:
            error(
                f"Key '{k}' not found in the object.",
                console=console
            )
            return None
    if isinstance(command, str):
        return command
    elif isinstance(command, list):
        return " && ".join(command)
    else:
        error(
            f"Value for key '{key}' is not a string or list.",
            console=console
        )
        return None


def main():
    console = Console()
    parser = argparse.ArgumentParser(
        description="Run commands from `unrun.yaml`"
    )
    parser.add_argument("key", help="The key of the command to run from unrun.yaml")
    args = parser.parse_args()

    config = load("unrun.yaml", console)
    if config is None:
        return

    command = parse(args.key, config, console)
    if command is None:
        return

    console.print(
        Panel(
            Syntax(
                command, "bash",
                theme="monokai",
                line_numbers=False
            ),
            title=Text(f"Running command for key '{args.key}'", style="bold blue")
        )
    )

    try:
        # Prepare environment for the subprocess
        # This helps with Unicode encoding issues on Windows,
        # especially when tools like 'twine' use 'rich' for output.
        process_env = os.environ.copy()
        process_env["PYTHONIOENCODING"] = "utf-8"
        process_env["PYTHONUTF8"] = "1"

        process = subprocess.Popen(
            command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",  # Ensure the parent process decodes output as UTF-8
            errors="replace",  # How to handle decoding errors if any (though unlikely for rich)
            env=process_env    # Pass the modified environment to the subprocess
        )
        stdout, stderr = process.communicate()

        if stdout:
            console.print(Text("Output:", style="bold green"))
            console.print(stdout.strip())
        if stderr:
            console.print(Text("Error:", style="bold red"))
            console.print(stderr.strip())
        if not stdout and not stderr:
            console.print(
                Text("No output or error from the command.", style="bold green")
            )

    except Exception as e:
        error(
            f"An unexpected error occurred: {e}",
            console,
            title="Unexpected Error"
        )


if __name__ == "__main__":
    main()
