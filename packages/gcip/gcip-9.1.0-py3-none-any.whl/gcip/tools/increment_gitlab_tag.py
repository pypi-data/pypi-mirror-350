import argparse
import os
from typing import Tuple

import gitlab  # type: ignore
import semver  # type: ignore
from gitlab.v4.objects import Project  # type: ignore


# Function to get the latest tag from the repository
def get_latest_tag(project: Project) -> str:
    tags = project.tags.list(order_by="version", sort="desc")
    if tags:
        return str(list(tags)[0].name)
    else:
        return "0.0.0"


# Function to increment the version
def increment_version(version: str, increment_type: str) -> semver.VersionInfo:
    if increment_type == "major":
        return semver.VersionInfo.parse(version).bump_major()
    elif increment_type == "minor":
        return semver.VersionInfo.parse(version).bump_minor()
    elif increment_type == "patch":
        return semver.VersionInfo.parse(version).bump_patch()
    else:
        raise ValueError(
            "Invalid increment type. Choose from 'major', 'minor', 'patch'."
        )


# Function to handle optional 'v' prefix
def handle_version_prefix(version: str) -> Tuple[str, str]:
    prefix = ""
    if version.startswith("v") or version.startswith("V"):
        prefix = version[0]
        version = version[1:]
    return prefix, version


# Main function
def main(
    *,
    gitlab_projects: str,
    private_token_env: str,
    use_job_token: bool = False,
    job_token_env: str = "CI_JOB_TOKEN",
    increment_type: str,
    gitlab_host: str,
    tag_message: str = "",
) -> None:
    private_token: str | None = None
    job_token: str | None = None

    private_token = os.environ[private_token_env]
    job_token = os.environ[job_token_env]

    # Create a GitLab instances
    gl_private_token = gitlab.Gitlab(gitlab_host, private_token=private_token)
    if use_job_token:
        gl_job_token = gitlab.Gitlab(gitlab_host, job_token=job_token)

    # Split project list into individual projects
    projects = [p.strip() for p in gitlab_projects.split(",")]

    for project in projects:
        # Get the project instance
        project_private_token = gl_private_token.projects.get(project, lazy=True)

        # Get the latest tag
        latest_tag = get_latest_tag(project_private_token)
        print(f"Project: {project}")
        print(f"Latest tag: {latest_tag}")

        # Handle optional 'v' prefix
        latest_tag_prefix, latest_tag_version = handle_version_prefix(latest_tag)

        # Increment the version
        new_version = increment_version(latest_tag_version, increment_type)

        # Combine prefix with new version
        new_tag = f"{latest_tag_prefix}{new_version}"
        print(f"New version: {new_tag}")

        if use_job_token:
            print("Creating Release...")
            project_job_token = gl_job_token.projects.get(project, lazy=True)
            # Create a new release with job token
            project_job_token.releases.create(
                {
                    "tag_name": new_tag,
                    "ref": "main",
                }
            )
        else:
            print("Creating Tag...")
            # Create a new tag with optional message
            project_private_token.tags.create(
                {
                    "tag_name": new_tag,
                    "ref": "main",
                    "message": tag_message if tag_message else "",
                }
            )
        print("Success.")
        print("-" * 20)

    if not use_job_token and tag_message:
        print(f"Tag message: {tag_message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Increment SemVer tag in GitLab repository."
    )
    parser.add_argument(
        "--gitlab-projects",
        type=str,
        required=True,
        help="Comma-separated list of GitLab project IDs or paths (namespace/project).",
    )
    parser.add_argument(
        "--increment-type",
        type=str,
        required=True,
        choices=["major", "minor", "patch"],
        help="The part of the version to increment.",
    )
    parser.add_argument(
        "--private-token-env",
        type=str,
        required=True,
        help="Environment variable for GitLab private token. Used to query existing tags.",
    )
    parser.add_argument(
        "--use-job-token",
        action="store_true",
        help="If to use the job token for creating tags via releases, the only way to create tags on behalf the pipeline triggerer.",
    )
    parser.add_argument(
        "--job-token-env",
        type=str,
        default="CI_JOB_TOKEN",
        help="Environment variable for GitLab job token. Typically 'CI_JOB_TOKEN'. Used to create releases/tags.",
    )
    parser.add_argument(
        "--gitlab-host",
        type=str,
        default="https://gitlab.com",
        help="The GitLab host URL.",
    )
    parser.add_argument(
        "--tag-message",
        type=str,
        default="",
        help="Optional message to include in the tag. Does not work with '--use-job-token'.",
    )

    args = parser.parse_args()
    main(
        gitlab_projects=args.gitlab_projects,
        private_token_env=args.private_token_env,
        use_job_token=args.use_job_token,
        job_token_env=args.job_token_env,
        increment_type=args.increment_type,
        gitlab_host=args.gitlab_host,
        tag_message=args.tag_message,
    )
