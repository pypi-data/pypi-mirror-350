import logging
import re
from tempfile import TemporaryDirectory
from typing import Tuple

from exasol_script_languages_container_ci.lib.asset_uploader import AssetUploader
from exasol_script_languages_container_ci.lib.ci_export import CIExport


def _parse_repo_url(source_repo_url: str) -> str:
    """
    source_repo_url is expected to have the following format: `https://github.com/exasol/script-languages-repo`
    where `exasol/script-languages-repo` is the repository for which the release will be created.
    This method returns the repository id.
    """
    res = re.search(r"^https://github.com/([a-zA-Z0-9\-_/]+)$", source_repo_url)
    if res is None:
        raise ValueError(
            f"Parameter source_repo_url={source_repo_url} does not match the following regex: "
            rf"^https://github.com/([a-zA-Z0-9\-_/]+)$"
        )
    return res.groups()[0]


class ReleaseUploader:

    def __init__(self, asset_uploader: AssetUploader, ci_export: CIExport = CIExport()):
        self._ci_export = ci_export
        self._asset_uploader = asset_uploader

    def release_upload(
        self, flavor_path: Tuple[str, ...], source_repo_url: str, release_id: int
    ) -> None:
        """
        Exports the container into tar.gz(s) and uploads to the repository / release.
        release_key is expected to have the following format: "{key}:{value}" where {key} can be:
        * "Tag"
        * "Id"
        source_repo_url is expected to have the following format: `https://github.com/exasol/script-languages-repo`
        """
        repo_id = _parse_repo_url(source_repo_url)
        with TemporaryDirectory() as temp_dir:
            logging.info(f"Running command 'export' with parameters: {locals()}")
            self._ci_export.export(flavor_path=flavor_path, export_path=temp_dir)
            self._asset_uploader.upload_assets(
                repo_id=repo_id,
                release_id=release_id,
                content_type="application/gzip",
                artifact_path=temp_dir,
                file_suffix=".tar.gz",
                label_prefix="Flavor",
            )
            self._asset_uploader.upload_assets(
                repo_id=repo_id,
                release_id=release_id,
                content_type="text/plain",
                artifact_path=temp_dir,
                file_suffix=".tar.gz.sha512sum",
                label_prefix="Checksum",
            )
