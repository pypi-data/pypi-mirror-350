import logging
from pathlib import Path

from github import Github, GithubException


class GithubReleaseAssetUploader:
    """
    Implements upload to a Github Release.
    See https://docs.github.com/en/rest/releases/assets#upload-a-release-asset for details.
    The access token needs to be stored in the environment variable GITHUB_TOKEN
    """

    def __init__(self, token):
        self._token = token

    def upload(
        self,
        archive_path: str,
        label: str,
        repo_id: str,
        release_id: int,
        content_type: str,
    ):
        gh = Github(self._token)
        gh_repo = gh.get_repo(repo_id)
        release = gh_repo.get_release(release_id)
        # Check GH limitation
        # https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases#storage-and-bandwidth-quotas
        if Path(archive_path).stat().st_size >= 2 * (2**30):
            logging.error("File larger than 2GB. Skipping it...")
        else:
            try:
                release.upload_asset(
                    path=archive_path, label=label, content_type=content_type
                )
            except GithubException as ex:
                logging.error(
                    f"Upload of asset {archive_path} to release {release_id} failed: {ex}"
                )
                raise ex
