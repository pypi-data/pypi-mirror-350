import glob
import logging
from pathlib import Path

from exasol_script_languages_container_ci.lib.github_release_asset_uploader import (
    GithubReleaseAssetUploader,
)


class AssetUploader:

    def __init__(self, release_asset_uploader: GithubReleaseAssetUploader):
        self._release_asset_uploader = release_asset_uploader

    def upload_assets(
        self,
        repo_id: str,
        release_id: int,
        content_type: str,
        artifact_path: str,
        file_suffix: str,
        label_prefix: str,
    ):
        release_artifacts = glob.glob(f"{artifact_path}/*{file_suffix}")
        for release_artifact in release_artifacts:
            artifact_file_name = Path(release_artifact).name
            if artifact_file_name.endswith(file_suffix):
                artifact_file_name = artifact_file_name[: -len(file_suffix)]
            else:
                logging.error(
                    f"Artifact file: {artifact_file_name} does not end with {file_suffix}. "
                    f"Using {artifact_file_name} as label."
                )
            self._release_asset_uploader.upload(
                archive_path=release_artifact,
                label=f"{label_prefix} {artifact_file_name}",
                repo_id=repo_id,
                release_id=release_id,
                content_type=content_type,
            )
