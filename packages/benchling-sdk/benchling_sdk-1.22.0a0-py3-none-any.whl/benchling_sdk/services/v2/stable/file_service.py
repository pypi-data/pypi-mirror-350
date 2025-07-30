from typing import Iterable, List, Optional

from benchling_api_client.v2.stable.api.files import (
    archive_files as api_client_archive_files,
    create_file,
    get_file,
    list_files,
    patch_file,
    unarchive_files,
)
from benchling_api_client.v2.stable.models.file import File
from benchling_api_client.v2.stable.models.file_create import FileCreate
from benchling_api_client.v2.stable.models.file_update import FileUpdate
from benchling_api_client.v2.stable.models.files_archival_change import FilesArchivalChange
from benchling_api_client.v2.stable.models.files_archive import FilesArchive
from benchling_api_client.v2.stable.models.files_archive_reason import FilesArchiveReason
from benchling_api_client.v2.stable.models.files_paginated_list import FilesPaginatedList
from benchling_api_client.v2.stable.models.files_unarchive import FilesUnarchive
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset
from benchling_sdk.services.v2.base_service import BaseService


class FileService(BaseService):
    """
    Files.

    Files are Benchling objects that represent files and their metadata. Compared to Blobs, which are used by
    most Benchling products for attachments, Files are primarily used in the Analysis and Connect product.

    See https://benchling.com/api/v2/reference#/Files
    """

    @api_method
    def archive_files(
        self, file_ids: Iterable[str], reason: FilesArchiveReason
    ) -> FilesArchivalChange:
        """
        Archive Files.

        See https://benchling.com/api/reference#/Files/archiveFiles
        """
        archive_request = FilesArchive(reason=reason, file_ids=list(file_ids))
        response = api_client_archive_files.sync_detailed(
            client=self.client,
            json_body=archive_request,
        )
        return model_from_detailed(response)

    @api_method
    def create(self, file: FileCreate) -> File:
        """
        Create a file.

        See https://benchling.com/api/v2/reference#/Files/createFile
        """
        response = create_file.sync_detailed(client=self.client, json_body=file)
        return model_from_detailed(response)

    @api_method
    def get_by_id(self, file_id: str) -> File:
        """
        Get a file.

        See https://benchling.com/api/v2/reference#/Files/getFile
        """
        response = get_file.sync_detailed(client=self.client, file_id=file_id)
        return model_from_detailed(response)

    @api_method
    def _files_page(
        self,
        ids: Optional[str] = None,
        display_ids: Optional[str] = None,
        returning: Optional[str] = None,
    ) -> Response[FilesPaginatedList]:
        response = list_files.sync_detailed(
            client=self.client,
            ids=none_as_unset(ids),
            display_ids=none_as_unset(display_ids),
            returning=none_as_unset(returning),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list(
        self,
        *,
        ids: Optional[str] = None,
        display_ids: Optional[str] = None,
        returning: Optional[str] = None,
    ) -> PageIterator[File]:
        """
        List Files.

        See https://benchling.com/api/v2/reference#/Files/listFiles
        """

        def api_call(next_token: NextToken) -> Response[FilesPaginatedList]:
            return self._files_page(ids=ids, display_ids=display_ids, returning=returning)

        def results_extractor(body: FilesPaginatedList) -> Optional[List[File]]:
            return body.files

        return PageIterator(api_call, results_extractor)

    @api_method
    def update(self, file_id: str, file: FileUpdate) -> File:
        """
        Update a File.

        See https://benchling.com/api/reference#/Files/updateFile
        """
        response = patch_file.sync_detailed(client=self.client, file_id=file_id, json_body=file)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, file_ids: Iterable[str]) -> FilesArchivalChange:
        """
        Unarchive one or more Files.

        See https://benchling.com/api/reference#/Files/unarchiveFiles
        """
        unarchive_request = FilesUnarchive(file_ids=list(file_ids))
        response = unarchive_files.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)
