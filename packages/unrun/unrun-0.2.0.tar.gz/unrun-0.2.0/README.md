# UnRun

A simple CLI tool to run commands from a YAML file.

## Installation

```bash
pip install unrun
```

## Usage & Features

Create an `unrun.yaml` file in your project root:

```yaml
hello: echo "Hello, world!"
foo:
    bar: echo "This is foo bar"
baz:
    - echo "This is baz item 1"
    - echo "This is baz item 2"
```

### Single Command

You can run a single command by specifying its key:

```bash
unrun hello
```

Output:

```
Hello, world!
```

### Nested Command
You can run nested commands by specifying the full path:

```bash
unrun foo.bar
```

Output:

```
This is foo bar
```

### List Command
To run all commands under a key that contains a list, you can simply specify the key:

```bash
unrun baz
```

Output:

```
This is baz item 1
This is baz item 2
```

### Arguments

- `key`: The key of the command to run.
- `--file`: Specify a custom YAML file (default is `unrun.yaml`).
- `extra`: Additional arguments to pass after each command.

## License

[MIT License](https://github.com/howcasperwhat/unrun/blob/main/LICENSE)