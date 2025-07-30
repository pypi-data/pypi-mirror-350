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


def parse_command(key: str, extra: str, object: dict, console: Console):
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
        return f"{command} {extra}" if extra else command
    elif isinstance(command, list):
        return " && ".join([
            f"{cmd} {extra}"
            if extra else cmd
            for cmd in command
        ])
    else:
        error(
            f"Value for key '{key}' is not a string or list.",
            console=console
        )
        return None


def parse_filename(file) -> str:
    filename = file if file else os.getenv("UNRUN_FILE")
    if not filename:
        f = os.path.expanduser("~/unrun.config.yaml")
        if os.path.exists(f):
            with open(f, "r") as file:
                try:
                    config = yaml.safe_load(file)
                    filename = config.get("file", "unrun.yaml")
                except yaml.YAMLError:
                    filename = "unrun.yaml"
        else:
            filename = "unrun.yaml"
    if not filename.endswith(".yaml"):
        filename += ".yaml"
    return filename


def parse_extra(extra: list, unknown: list) -> str:
    result = []
    if extra and unknown:
        result = extra + unknown
    elif extra:
        result = extra
    elif unknown:
        result = unknown
    return " ".join(result)


def main():
    console = Console()
    parser = argparse.ArgumentParser(
        description="Run commands from `.yaml` files using unrun.",
        epilog="Example: unrun my_command",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("key", help="The key of the command to run from `.yaml`")
    parser.add_argument("--file", "-f", default=None, help="Path to the `.yaml`")
    parser.add_argument("extra", nargs="*", help="Extra arguments to pass to the command")
    args, unknown = parser.parse_known_args()

    key, file = args.key, args.file
    extra = parse_extra(args.extra, unknown)

    filename = parse_filename(file)

    config = load(filename, console)
    if config is None:
        return

    command = parse_command(key, extra, config, console)
    if command is None:
        return

    console.print(
        Panel(
            Syntax(command, "bash", word_wrap=True),
            title=Text(f"Running command for key '{args.key}'", style="bold blue"),
        )
    )

    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        error(
            f"An unexpected error occurred: {e}",
            console,
            title="Unexpected Error"
        )


if __name__ == "__main__":
    main()
