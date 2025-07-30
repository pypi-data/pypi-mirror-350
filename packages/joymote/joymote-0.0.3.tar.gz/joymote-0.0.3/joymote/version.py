import importlib.metadata
import os
import re
import subprocess


def get_version() -> str:
    try:
        # Try to get the version from the installed package metadata
        return importlib.metadata.version("joymote")
    except importlib.metadata.PackageNotFoundError:
        try:
            # Try to get the version from the git commit hash
            git_dir = os.path.dirname(__file__)
            git_describe = subprocess.check_output(
                ["git", "describe", "--tags", "--long", "--always"],
                cwd=git_dir,
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()

            # Remove starting "v"
            git_describe = re.sub(r"^v", r"", git_describe)
            # Add "r" before the number of revisions
            git_describe = re.sub(r"([^-]*-g)", r"r\1", git_describe)

            return f"{git_describe}"
        except Exception:
            return "unknown"


if __name__ == "__main__":
    print(get_version())
