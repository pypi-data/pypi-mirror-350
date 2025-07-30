import os
from pathlib import Path


def download_example_yaml(output_path: str | None = None) -> str | bool:
    """
    Downloads the example YAML file containing CV data.

    Args:
        output_path (str, optional): Path where to save the example YAML.
                                    If None, returns the YAML content as a string.

    Returns:
        str or bool: YAML content if output_path is None,
                     otherwise True if file was saved successfully.
    """
    # Get the path to the example YAML file
    current_dir = Path(__file__).parent
    example_path = current_dir / "example.yaml"

    try:
        # Read the example YAML content
        with open(example_path) as f:
            example_yaml = f.read()

        if output_path is None:
            return example_yaml

        # Ensure directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Write content to file
        with open(output_path, "w") as f:
            f.write(example_yaml)
        return True
    except Exception as e:
        print(f"Error handling example YAML: {e}")
        return False


def main() -> None:
    """CLI entry point to download the example YAML."""
    import argparse

    parser = argparse.ArgumentParser(description="Download example CV YAML file")
    parser.add_argument(
        "--output",
        "-o",
        default="example.yaml",
        help="Output file path (default: example.yaml)",
    )

    args = parser.parse_args()

    if download_example_yaml(args.output):
        print(f"Example YAML saved to {args.output}")
    else:
        print("Failed to save example YAML")


if __name__ == "__main__":
    main()
