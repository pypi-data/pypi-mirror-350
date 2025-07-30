"""This script sets up the package version based on the latest git tag
or commit hash."""

import logging
import pathlib
import re

import git  # type: ignore[import-not-found]
import setuptools  # type: ignore[import-untyped]

VERSION_FILE = "src/nombres_vers_lettres/_version.py"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# def get_long_description() -> str:
#     """Get the long description from the README file.

#     Returns:
#         str: The content of the README file.
#     """
#     readme_path = pathlib.Path(__file__).parent / "README.md"

#     if not readme_path.exists():
#         return ""

#     with readme_path.open(encoding="utf-8") as readme_file:
#         return readme_file.read()


def get_version() -> str:
    """Get the package version from the latest git tag or commit hash.

    Returns:
        str: The version string, which is the latest git tag or commit hash.
    """
    if pathlib.Path(VERSION_FILE).exists():
        logger.info("Using version from %s", VERSION_FILE)
        with open(VERSION_FILE, encoding="utf-8") as version_file:
            return (
                version_file.read()
                .strip()
                .replace('__version__ = "', "")
                .replace('"', "")
            )

    def _write_version_file(version: str) -> str:
        """Write the version to the _version.py file."""
        with open(VERSION_FILE, "w", encoding="utf-8") as version_file:
            version_file.write(f'__version__ = "{version}"\n')

        logger.info("Wrote version %s to %s", version, VERSION_FILE)
        return version

    # Attempt to get the version from the latest git tag
    try:
        repo = git.Repo(search_parent_directories=True)
        tag = repo.git.describe(tags=True, always=True)
        logger.info("Found git tag: %s", tag)

    except git.InvalidGitRepositoryError:
        logger.warning("Not in a git repository, falling back to commit hash.")
        # Fallback version if not in a git repository
        return _write_version_file("0.0.0")

        # Example of tag: v1.0.2-3-gabcdef0
    # Convert to: 1.0.2.post3+gabcdef0
    match = re.match(r"v?(\d+\.\d+\.\d+)(?:-(\d+)-g([0-9a-f]+))?", tag)
    if match:
        base_version = match.group(1)
        commits_since_tag = match.group(2)
        commit_hash = match.group(3)

        if commits_since_tag and commit_hash:
            logger.info(
                "Version with commits since tag: %s, commit hash: %s",
                commits_since_tag,
                commit_hash,
            )
            return _write_version_file(
                f"{base_version}.post{commits_since_tag}+g{commit_hash}"
            )
        logger.info("Base version from tag: %s", base_version)
        return _write_version_file(base_version)

    logger.warning("Unexpected tag format: %s", tag)
    # Fallback version if tag format is unexpected
    return _write_version_file("0.0.0")


setuptools.setup(
    version=get_version(),
    # long_description=get_long_description(),
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
)
