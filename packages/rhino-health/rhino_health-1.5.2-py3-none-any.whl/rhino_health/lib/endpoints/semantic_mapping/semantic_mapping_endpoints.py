"""
@autoapi False
"""
from typing import Union

from rhino_health.lib.endpoints.endpoint import Endpoint
from rhino_health.lib.endpoints.semantic_mapping.semantic_mapping_dataclass import (
    SemanticMappingApproveList,
    SemanticMappingCreateInput,
    SemanticMappingDataclass,
    Vocabulary,
    VocabularyInput,
    VocabularySearch,
)
from rhino_health.lib.utils import rhino_error_wrapper

BUFFER_TIME_IN_SEC = 300


class SemanticMappingEndpoints(Endpoint):
    """
    @autoapi False

    Endpoints to interact with semantic mappings
    """

    @property
    def semantic_mapping_dataclass(self):
        """
        @autoapi False
        :return:
        """
        return SemanticMappingDataclass

    @rhino_error_wrapper
    def vocabulary_search(self, vocabulary_uid: str, vocabulary_search_params: VocabularySearch):
        return self.session.post(
            f"/vocabularies/{vocabulary_uid}/search/",
            vocabulary_search_params.dict(by_alias=True),
            adapter_kwargs={"data_as_json": True},
        )

    @rhino_error_wrapper
    def create_semantic_mapping(self, semantic_mapping_create_input: SemanticMappingCreateInput):
        data = semantic_mapping_create_input.dict(by_alias=True)
        result = self.session.post(
            "/semantic_mappings",
            data=data,
            adapter_kwargs={"data_as_json": True},
        )
        return result.to_dataclass(self.semantic_mapping_dataclass)

    @rhino_error_wrapper
    def get_semantic_mapping(self, semantic_mapping_or_uid: Union[str, SemanticMappingDataclass]):
        result = self.session.get(
            f"/semantic_mappings/{semantic_mapping_or_uid if isinstance(semantic_mapping_or_uid, str) else semantic_mapping_or_uid.uid}"
        )
        return result.to_dataclass(self.semantic_mapping_dataclass)

    @rhino_error_wrapper
    def get_semantic_mapping_data(
        self, semantic_mapping_or_uid: Union[str, SemanticMappingDataclass]
    ):
        result = self.session.get(
            f"/semantic_mappings/{semantic_mapping_or_uid if isinstance(semantic_mapping_or_uid, str) else semantic_mapping_or_uid.uid}/data"
        )
        return result  # TODO: Convert to dataclass.

    @rhino_error_wrapper
    def approve_mappings(self, semantic_mapping_uid: str, mapping_data: SemanticMappingApproveList):
        data = mapping_data.dict(by_alias=True)
        result = self.session.post(
            f"/semantic_mappings/{semantic_mapping_uid}/approve_mappings",
            data=data,
            adapter_kwargs={"data_as_json": True},
        )
        return result  # TODO: Convert to dataclass

    def create_vocabulary(self, vocabulary_input: VocabularyInput):
        data = vocabulary_input.dict(by_alias=True)
        result = self.session.post(
            "/vocabularies/",
            data=data,
            adapter_kwargs={"data_as_json": True},
        )
        return result.to_dataclass(Vocabulary)

    def get_vocabulary(self, vocabulary_or_uid: Union[str, Vocabulary]):
        result = self.session.get(
            f"/vocabularies/{vocabulary_or_uid if isinstance(vocabulary_or_uid, str) else vocabulary_or_uid.uid}",
        )
        return result.to_dataclass(Vocabulary)
