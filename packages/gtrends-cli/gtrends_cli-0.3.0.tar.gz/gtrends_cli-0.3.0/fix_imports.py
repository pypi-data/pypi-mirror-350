#!/usr/bin/env python3
import os
import re


def fix_imports(directory):
    """Recursively fix imports in all Python files in the given directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()

                # Replace 'from src.' with 'from '
                modified_content = re.sub(r"from src\.", "from ", content)

                # Write back only if changes were made
                if modified_content != content:
                    print(f"Fixing imports in {file_path}")
                    with open(file_path, "w") as f:
                        f.write(modified_content)


if __name__ == "__main__":
    fix_imports("src")
    print("Import fixes completed.")
