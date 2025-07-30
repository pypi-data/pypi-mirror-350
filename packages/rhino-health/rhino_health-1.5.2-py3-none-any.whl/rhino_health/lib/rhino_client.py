import sys

from rhino_health.lib.constants import ApiEnvironment
from rhino_health.lib.endpoints.code_object.code_object_endpoints import (
    CodeObjectEndpoints,
    LTSCodeObjectEndpoints,
)
from rhino_health.lib.endpoints.code_run.code_run_endpoints import (
    CodeRunEndpoints,
    LTSCodeRunEndpoints,
)
from rhino_health.lib.endpoints.data_schema.data_schema_endpoints import (
    DataSchemaEndpoints,
    LTSDataSchemaEndpoints,
)
from rhino_health.lib.endpoints.dataset.dataset_endpoints import (
    DatasetEndpoints,
    LTSDatasetEndpoints,
)
from rhino_health.lib.endpoints.federated_dataset.federated_dataset_endpoints import (
    FederatedDatasetEndpoints,
)
from rhino_health.lib.endpoints.project.project_endpoints import (
    LTSProjectEndpoints,
    ProjectEndpoints,
)
from rhino_health.lib.endpoints.sql_query.sql_query_endpoints import SQLQueryEndpoints
from rhino_health.lib.endpoints.user.user_endpoints import LTSUserEndpoints, UserEndpoints
from rhino_health.lib.endpoints.workgroup.workgroup_endpoints import (
    LTSWorkgroupEndpoints,
    WorkgroupEndpoints,
)
from rhino_health.lib.utils import alias, rhino_error_wrapper, setup_traceback, url_for

__api__ = ["RhinoClient"]


class EndpointTypes:
    """
    Constants for different endpoint types. This is how we group and separate different endpoints
    """

    PROJECT = "project"
    DATASET = "dataset"
    DATA_SCHEMA = "data_schema"
    FEDERATED_DATASET = "federated_dataset"
    CODE_OBJECT = "code_object"
    CODE_RUN = "code_run"
    WORKGROUP = "workgroup"
    SQL_QUERY = "sql_query"
    USER = "user"


class SDKVersion:
    """
    Used internally for future backwards compatibility
    """

    STABLE = "1.0"
    PREVIEW = "2.0"


VERSION_TO_CLOUD_API = {SDKVersion.STABLE: "v2", SDKVersion.PREVIEW: "v2"}
"""
@autoapi False
"""

VERSION_TO_ENDPOINTS = {
    SDKVersion.STABLE: {
        EndpointTypes.CODE_OBJECT: LTSCodeObjectEndpoints,
        EndpointTypes.DATASET: LTSDatasetEndpoints,
        EndpointTypes.DATA_SCHEMA: LTSDataSchemaEndpoints,
        EndpointTypes.FEDERATED_DATASET: FederatedDatasetEndpoints,
        EndpointTypes.CODE_RUN: LTSCodeRunEndpoints,
        EndpointTypes.PROJECT: LTSProjectEndpoints,
        EndpointTypes.SQL_QUERY: SQLQueryEndpoints,
        EndpointTypes.USER: LTSUserEndpoints,
        EndpointTypes.WORKGROUP: LTSWorkgroupEndpoints,
    },
    SDKVersion.PREVIEW: {
        EndpointTypes.CODE_OBJECT: CodeObjectEndpoints,
        EndpointTypes.DATASET: DatasetEndpoints,
        EndpointTypes.DATA_SCHEMA: DataSchemaEndpoints,
        EndpointTypes.FEDERATED_DATASET: FederatedDatasetEndpoints,
        EndpointTypes.CODE_RUN: CodeRunEndpoints,
        EndpointTypes.PROJECT: ProjectEndpoints,
        EndpointTypes.SQL_QUERY: SQLQueryEndpoints,
        EndpointTypes.USER: UserEndpoints,
        EndpointTypes.WORKGROUP: WorkgroupEndpoints,
    },
}
"""
@autoapi False
"""


class RhinoClient:
    """
    Allows access to various endpoints directly from the RhinoSession

    Attributes
    ----------
    code_object: Access endpoints at the code_object level
    code_run: Access endpoints at the code_run level
    dataset: Access endpoints at the dataset level
    data_schema: Access endpoints at the data_schema level
    federated_dataset: Access endpoints for federated_datasets
    project: Access endpoints at the project level
    sql_query: Access endpoints for sql queries
    user: Access endpoints at the user level
    workgroup: Access endpoints at the workgroup level

    Examples
    --------
    >>> session.project.get_projects()
    array[Project...]
    >>> session.dataset.get_dataset(my_dataset_uid)
    Dataset

    See Also
    --------
    rhino_health.lib.endpoints.code_object.code_object_endpoints: Available code_object endpoints
    rhino_health.lib.endpoints.code_run.code_run_endpoints: Available code_run endpoints
    rhino_health.lib.endpoints.dataset.dataset_endpoints: Available dataset endpoints
    rhino_health.lib.endpoints.data_schema.data_schema_endpoints: Available data_schema endpoints
    rhino_health.lib.endpoints.project.project_endpoints: Available project endpoints
    rhino_health.lib.endpoints.sql_query.sql_query_endpoints: Available sql_query endpoints
    rhino_health.lib.endpoints.user.user_endpoints: Available user endpoints
    rhino_health.lib.endpoints.workgroup.workgroup_endpoints: Available workgroup endpoints
    """

    @rhino_error_wrapper
    def __init__(
        self,
        rhino_api_url: str = ApiEnvironment.PROD_API_URL,
        sdk_version: str = SDKVersion.PREVIEW,
        show_traceback: bool = False,
    ):
        setup_traceback(sys.excepthook, show_traceback)
        self.rhino_api_url = rhino_api_url
        self.sdk_version = sdk_version
        if sdk_version not in VERSION_TO_ENDPOINTS.keys():
            raise ValueError(
                "The api version you specified is not supported in this version of the SDK"
            )
        self.code_object: LTSCodeObjectEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.CODE_OBJECT
        ](self)
        self.dataset: LTSDatasetEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.DATASET
        ](self)
        self.data_schema: LTSDataSchemaEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.DATA_SCHEMA
        ](self)
        # TODO: Should there be dicomweb here
        self.federated_dataset: FederatedDatasetEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.FEDERATED_DATASET
        ](self)
        self.code_run: LTSCodeRunEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.CODE_RUN
        ](self)
        self.project: LTSProjectEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.PROJECT
        ](self)
        self.sql_query: SQLQueryEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.SQL_QUERY
        ](self)
        self.user: SQLQueryEndpoints = VERSION_TO_ENDPOINTS[sdk_version][EndpointTypes.USER](self)
        self.workgroup: LTSWorkgroupEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.WORKGROUP
        ](self)
        self.api_url = url_for(self.rhino_api_url, VERSION_TO_CLOUD_API[sdk_version])
