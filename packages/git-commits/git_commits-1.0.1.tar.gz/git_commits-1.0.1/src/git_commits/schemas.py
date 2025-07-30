from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class GitCommit:
    """Represents a Git commit with relevant information."""

    sha: str
    short_sha: str
    author_name: str
    author_email: str
    authored_datetime: datetime
    message: str
    branches: List[str]


@dataclass
class RepoAuthor:
    """Represents a Git repository author with relevant information."""

    name: str
    email: str
