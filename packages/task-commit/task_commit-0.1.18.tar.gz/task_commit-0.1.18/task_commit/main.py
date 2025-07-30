import io
import sys

from .core import git_commit

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    """
    Main function that calls the git_commit function to perform the commit.
    """

    git_commit()
