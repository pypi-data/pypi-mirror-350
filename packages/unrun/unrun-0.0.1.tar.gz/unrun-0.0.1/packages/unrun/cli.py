import yaml
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run commands from unrun.yaml")
    parser.add_argument("key", help="The key of the command to run from unrun.yaml")
    args = parser.parse_args()

    try:
        with open("unrun.yaml", "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: unrun.yaml not found in the current directory.")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing unrun.yaml: {e}")
        return

    if args.key in config:
        command = config[args.key]
        print(f"Running command: {command}")
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print(f"Error: Key '{args.key}' not found in unrun.yaml")

if __name__ == "__main__":
    main()
