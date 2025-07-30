from typing import Iterable, List, Optional

from benchling_api_client.v2.stable.api.datasets import (
    archive_datasets as api_client_archive_datasets,
    create_dataset,
    get_dataset,
    list_datasets,
    unarchive_datasets,
    update_dataset,
)
from benchling_api_client.v2.stable.models.dataset import Dataset
from benchling_api_client.v2.stable.models.dataset_create import DatasetCreate
from benchling_api_client.v2.stable.models.dataset_update import DatasetUpdate
from benchling_api_client.v2.stable.models.datasets_archival_change import DatasetsArchivalChange
from benchling_api_client.v2.stable.models.datasets_archive import DatasetsArchive
from benchling_api_client.v2.stable.models.datasets_archive_reason import DatasetsArchiveReason
from benchling_api_client.v2.stable.models.datasets_paginated_list import DatasetsPaginatedList
from benchling_api_client.v2.stable.models.datasets_unarchive import DatasetsUnarchive
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset
from benchling_sdk.services.v2.base_service import BaseService


class DatasetService(BaseService):
    """
    Datasets.

    Similar to Data frames, datasets in Benchling represent tabular data that is not schematized. Datasets are
    saved to folders within Benchling with additional metadata, making them accessible and searchable within
    Benchling. Each dataset actually contains a data frame, and a data frame is required to create a dataset.

    See https://benchling.com/api/v2/reference#/Datasets
    """

    @api_method
    def get_by_id(self, dataset_id: str) -> Dataset:
        """
        Get a dataset.

        See https://benchling.com/api/v2/reference#/Datasets/getDataset
        """
        response = get_dataset.sync_detailed(client=self.client, dataset_id=dataset_id)
        return model_from_detailed(response)

    @api_method
    def archive_datasets(
        self, dataset_ids: Iterable[str], reason: DatasetsArchiveReason
    ) -> DatasetsArchivalChange:
        """
        Archive Datasets.

        See https://benchling.com/api/reference#/Datasets/archiveDatasets
        """
        archive_request = DatasetsArchive(reason=reason, dataset_ids=list(dataset_ids))
        response = api_client_archive_datasets.sync_detailed(
            client=self.client,
            json_body=archive_request,
        )
        return model_from_detailed(response)

    @api_method
    def create(self, dataset: DatasetCreate) -> Dataset:
        """
        Create a dataset.

        See https://benchling.com/api/v2/reference#/Datasets/createDataset
        """
        response = create_dataset.sync_detailed(client=self.client, json_body=dataset)
        return model_from_detailed(response)

    @api_method
    def _datasets_page(
        self,
        ids: Optional[str] = None,
        display_ids: Optional[str] = None,
        returning: Optional[str] = None,
    ) -> Response[DatasetsPaginatedList]:
        response = list_datasets.sync_detailed(
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
    ) -> PageIterator[Dataset]:
        """
        List Datasets.

        See https://benchling.com/api/v2/reference#/Datasets/listDatasets
        """

        def api_call(next_token: NextToken) -> Response[DatasetsPaginatedList]:
            return self._datasets_page(ids=ids, display_ids=display_ids, returning=returning)

        def results_extractor(body: DatasetsPaginatedList) -> Optional[List[Dataset]]:
            return body.datasets

        return PageIterator(api_call, results_extractor)

    @api_method
    def unarchive(self, dataset_ids: Iterable[str]) -> DatasetsArchivalChange:
        """
        Unarchive one or more Datasets.

        See https://benchling.com/api/reference#/Datasets/unarchiveDatasets
        """
        unarchive_request = DatasetsUnarchive(dataset_ids=list(dataset_ids))
        response = unarchive_datasets.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def update(self, dataset_id: str, dataset: DatasetUpdate) -> Dataset:
        """
        Update a Dataset.

        See https://benchling.com/api/reference#/Datasets/updateDataset
        """
        response = update_dataset.sync_detailed(client=self.client, dataset_id=dataset_id, json_body=dataset)
        return model_from_detailed(response)
