"""
A Python library for listing Git commits from local repositories.
"""

from .core import list_git_commits, GitCommit

__version__ = "0.1.0"
__all__ = ["list_git_commits", "GitCommit"]
