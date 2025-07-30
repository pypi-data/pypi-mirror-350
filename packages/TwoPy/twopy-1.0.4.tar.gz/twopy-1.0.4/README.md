# Install
```shell
pip install TwoPy==version
```


## Example
```python
import argparse
import os
from TwoPy import PythonProjectBuilder

def main():
    parser = argparse.ArgumentParser(description="TwoPy")
    parser.add_argument(
        "project_path",
        nargs='?',
        default="src"
    )
    parser.add_argument("--rename", nargs='*')
    parser.add_argument("--move", nargs='*')
    parser.add_argument("--output", default="project.zip")
    parser.add_argument("--encrypt", action='store_false')
    parser.add_argument("--encrypted_output", default="project.enc")

    args = parser.parse_args()

    if not os.path.exists(args.project_path):
        print(f"Error: Project path '{args.project_path}' not found!")
        return

    builder = PythonProjectBuilder(args.project_path)

    rename_map = {}
    if args.rename:
        for pair in args.rename:
            if "=" in pair:
                old, new = pair.split("=", 1)
                rename_map[old] = new
            else:
                print(f"Invalid rename format: {pair}")

    move_map = {}
    if args.move:
        for pair in args.move:
            if "=" in pair:
                item, new_path = pair.split("=", 1)
                move_map[item] = new_path
            else:
                print(f"Invalid move format: {pair}")

    builder.adapt_structure(rename_map=rename_map, move_map=move_map)
    builder.compress(args.output)

    if args.encrypt:
        key = builder.encrypt(args.output, args.encrypted_output)
        print(f"Decryption key: {key.decode()}")

    builder.cleanup()

if __name__ == "__main__":
    main()
```



### ChangeLog

> [!NOTE] 1.0.0
> - First version