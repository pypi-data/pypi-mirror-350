"""
@autoapi False

INTERNAL USE ONLY!
"""

from typing import Union

from rhino_health.lib.endpoints.code_object.code_object_dataclass import CodeObjectRunResponse
from rhino_health.lib.endpoints.endpoint import Endpoint
from rhino_health.lib.endpoints.syntactic_mapping.syntactic_mapping_dataclass import (
    SyntacticMapping,
    SyntacticMappingCreateInput,
    SyntacticMappingRun,
)
from rhino_health.lib.utils import rhino_error_wrapper

BUFFER_TIME_IN_SEC = 300


class SyntacticMappingEndpoints(Endpoint):
    """
    @autoapi False

    Endpoints to interact with syntactic mappings
    """

    @property
    def syntactic_mapping_dataclass(self):
        """
        @autoapi False
        :return:
        """
        return SyntacticMapping

    @rhino_error_wrapper
    def create_syntactic_mapping(self, syntactic_mapping_input: SyntacticMappingCreateInput):
        data = syntactic_mapping_input.dict(by_alias=True)
        result = self.session.post(
            "/syntactic_mappings",
            data=data,
            adapter_kwargs={"data_as_json": True},
        )
        return result.to_dataclass(self.syntactic_mapping_dataclass)

    @rhino_error_wrapper
    def get_syntactic_mapping(self, syntactic_mapping_or_uid: Union[str, SyntacticMapping]):
        result = self.session.get(
            f"/syntactic_mappings/{syntactic_mapping_or_uid if isinstance(syntactic_mapping_or_uid, str) else syntactic_mapping_or_uid.uid}"
        )
        return result.to_dataclass(self.syntactic_mapping_dataclass)

    def run_data_harmonization(
        self,
        syntactic_mapping_or_uid: Union[str, SyntacticMapping],
        run_params: SyntacticMappingRun,
    ):
        syntactic_mapping = (
            self.get_syntactic_mapping(syntactic_mapping_or_uid)
            if isinstance(syntactic_mapping_or_uid, str)
            else syntactic_mapping_or_uid
        )
        data = run_params.dict(by_alias=True)
        result = self.session.post(
            f"/code_objects/{syntactic_mapping.code_object_uids[0]}/run_data_harmonization",
            data=data,
            adapter_kwargs={"data_as_json": True},
        )
        return result.to_dataclass(CodeObjectRunResponse)  # TODO: Is this the right response
