"""Teams validator module"""

from collections import Counter
from typing import Dict, List, Tuple, Union

from opendapi.defs import DATASTORES_SUFFIX, OPENDAPI_SPEC_URL, OpenDAPIEntity
from opendapi.validators.base import BaseValidator, ValidationError
from opendapi.validators.defs import FileSet, MergeKeyCompositeIDParams
from opendapi.weakref import weak_lru_cache


class DatastoresValidator(BaseValidator):
    """
    Validator class for datastores files
    """

    SUFFIX = DATASTORES_SUFFIX
    SPEC_VERSION = "0-0-1"
    ENTITY = OpenDAPIEntity.DATASTORES

    # Paths & keys to use for uniqueness check within a list of dicts when merging
    MERGE_UNIQUE_LOOKUP_KEYS: List[
        Tuple[
            List[Union[str, int, MergeKeyCompositeIDParams.IgnoreListIndexType]],
            MergeKeyCompositeIDParams,
        ]
    ] = [(["datastores"], MergeKeyCompositeIDParams(required=[["urn"]]))]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @weak_lru_cache()
    def _get_file_state_datastore_urn_counts(self, fileset: FileSet) -> Counter:
        """Collect all the datastores urns"""
        return Counter(
            (
                dt.get("urn")
                for content in self.get_file_state(fileset).values()
                for dt in content.get("datastores", [])
            )
        )

    def _validate_datastore_urns_globally_unique(
        self, file: str, content: dict, fileset: FileSet
    ):
        """Validate if the datastore urns are globally unique"""
        datastore_urn_counts = self._get_file_state_datastore_urn_counts(fileset)
        non_unique_datastore_urns = {
            datastore["urn"]
            for datastore in content.get("datastores", [])
            if datastore_urn_counts[datastore["urn"]] > 1
        }
        if non_unique_datastore_urns:
            raise ValidationError(
                f"Non-globally-unique datastore urns in file '{file}': {non_unique_datastore_urns}"
            )

    def validate_content(self, file: str, content: Dict, fileset: FileSet):
        """Validate the content of the files"""
        super().validate_content(file, content, fileset)
        self._validate_datastore_urns_globally_unique(file, content, fileset)

    def _get_base_generated_files(self) -> Dict[str, Dict]:
        """Set Autoupdate templates in {file_path: content} format"""
        return {
            f"{self.base_destination_dir}/{self.config.org_name_snakecase}.datastores.yaml": {
                "schema": OPENDAPI_SPEC_URL.format(
                    version=self.SPEC_VERSION, entity="datastores"
                ),
                "datastores": [],
            }
        }
