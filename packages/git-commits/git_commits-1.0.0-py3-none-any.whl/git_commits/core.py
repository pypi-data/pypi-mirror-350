"""
Core functionality for listing Git commits.
"""

import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

import git
import pytz
import dateparser

from .utils import get_timezone


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


def _parse_date_string(date_str: str, timezone: pytz.timezone = pytz.UTC) -> datetime:
    """
    Parse a date string into a timezone-aware datetime object using dateparser.

    Args:
        date_str: Date string to parse (e.g., "2023-01-01", "yesterday", "2 weeks ago")
        timezone: Timezone to interpret the date in (defaults to UTC)

    Returns:
        Timezone-aware datetime object
    """

    timezone_str = timezone.zone

    # Use dateparser to parse the date string
    dt = dateparser.parse(
        date_str, settings={"TIMEZONE": timezone_str, "RETURN_AS_TIMEZONE_AWARE": True}
    )
    if dt is None:
        raise ValueError(f"Unable to parse date string '{date_str}'")

    # Ensure the datetime is timezone-aware and in the correct timezone
    if dt.tzinfo is None:
        dt = timezone.localize(dt)
    else:
        dt = dt.astimezone(timezone)
    return dt


def list_git_commits(
    repo_path: str,
    author: Optional[str] = None,
    since: Optional[Union[str, datetime]] = None,
    until: Optional[Union[str, datetime]] = None,
    timezone: str = "UTC",
    all_branches: bool = False,
) -> List[GitCommit]:
    """
    List Git commits from a specified local repository with filtering options.

    Args:
        repo_path: The absolute or relative path to the local Git repository
        author: Filter commits by author's name or email (case-insensitive partial matching)
        since: Filter commits authored after this date (datetime object or string)
        until: Filter commits authored before this date (datetime object or string)
        timezone: Timezone string for interpreting string dates (e.g., "UTC", "America/New_York")
        all_branches: If True, search commits across all branches (including remote-tracking)

    Returns:
        List of GitCommit objects representing the filtered commits
    """
    try:
        # Validate and open the repository
        if not os.path.exists(repo_path):
            print(f"Error: Repository path '{repo_path}' does not exist.")
            return []

        repo = git.Repo(repo_path)

        # Validate that it's a Git repository
        if repo.bare:
            print(f"Error: '{repo_path}' is a bare repository.")
            return []

    except git.exc.InvalidGitRepositoryError:
        print(f"Error: '{repo_path}' is not a valid Git repository.")
        return []
    except Exception as e:
        print(f"Error: Unable to open repository at '{repo_path}': {e}")
        return []

    try:
        # Get timezone
        timezone_obj = get_timezone(timezone)

        # Prepare date filters
        since_datetime = None
        until_datetime = None

        if since is not None:
            if isinstance(since, str):
                since_datetime = _parse_date_string(since, timezone_obj)
            elif isinstance(since, datetime):
                since_datetime = since
                if since_datetime.tzinfo is None:
                    raise ValueError("datetime objects must be timezone-aware")
            else:
                raise ValueError("'since' must be a string or datetime object")

        if until is not None:
            if isinstance(until, str):
                until_datetime = _parse_date_string(until, timezone_obj)
            elif isinstance(until, datetime):
                until_datetime = until
                if until_datetime.tzinfo is None:
                    raise ValueError("datetime objects must be timezone-aware")
            else:
                raise ValueError("'until' must be a string or datetime object")

        # Get commits from appropriate branches
        if all_branches:
            # Get commits from all branches (including remote-tracking branches)
            commits = list(repo.iter_commits(all=True))
        else:
            # Get commits from current branch only
            commits = list(repo.iter_commits())

        # Filter commits
        filtered_commits = []

        for commit in commits:
            # Convert commit authored datetime to timezone-aware datetime
            commit_datetime = datetime.fromtimestamp(
                commit.authored_date, tz=timezone_obj
            )

            # Apply author filter
            if author is not None:
                author_lower = author.lower()
                if (
                    author_lower not in commit.author.name.lower()
                    and author_lower not in commit.author.email.lower()
                ):
                    continue

            # Apply since filter
            if since_datetime is not None and commit_datetime < since_datetime:
                continue

            # Apply until filter
            if until_datetime is not None and commit_datetime > until_datetime:
                continue

            # Get all branches containing this commit
            try:
                branches_output = repo.git.branch("--contains", commit.hexsha, "--all")
                branches = [
                    b.strip().lstrip("* ").replace("remotes/", "")
                    for b in branches_output.split("\n")
                    if b.strip()
                ]
            except Exception:
                branches = []

            # Create GitCommit object
            git_commit = GitCommit(
                sha=commit.hexsha,
                short_sha=commit.hexsha[:7],
                author_name=commit.author.name,
                author_email=commit.author.email,
                authored_datetime=commit_datetime,
                message=commit.message.strip(),
                branches=branches,
            )

            filtered_commits.append(git_commit)

        return filtered_commits

    except Exception as e:
        print(f"Error: An error occurred while processing commits: {e}")
        return []
