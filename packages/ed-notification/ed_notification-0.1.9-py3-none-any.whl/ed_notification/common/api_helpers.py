from typing import Generic, TypeVar

import jsons
import requests
from ed_domain.documentation.common.api_response import ApiResponse
from ed_domain.documentation.common.endpoint_call_params import \
    EndpointCallParams
from ed_domain.documentation.common.endpoint_description import \
    EndpointDescription

T = TypeVar("T")


class ApiClient(Generic[T]):
    def __init__(self, description: EndpointDescription):
        self._description = description

    def __call__(self, call_params: EndpointCallParams) -> ApiResponse[T]:
        self._validate_endpoint_description(call_params)

        url = self._build_url(call_params)
        method = self._description["method"]
        headers = call_params.get("headers", {})
        params = call_params.get("query_params", {})
        data = (
            call_params.get("request", {})
            if "request_model" in self._description
            else {}
        )

        response = requests.request(
            method, url, headers=headers, params=params, data=jsons.dumps(data)
        )
        return response.json()

    def _build_url(self, call_params: EndpointCallParams) -> str:
        path = self._description["path"]
        path_params = call_params.get("path_params", {})

        for key, value in path_params.items():
            path = path.replace(f"{{{key}}}", str(value))

        return f"{path}"

    def _validate_endpoint_description(self, call_params: EndpointCallParams):
        if request_model := self._description.get("request_model", None):
            if request := call_params.get("request", None):
                if not isinstance(request, type(request_model)):
                    ...
            else:
                raise ValueError("Request is not provided but is expected.")

        if path_params := call_params.get("path_params", None):
            for param in path_params.keys():
                if f"{{{param}}}" not in self._description["path"]:
                    raise ValueError(
                        f"Path parameter '{param}' is not present in the path."
                    )

        if placeholders := [
            part[1:-1]
            for part in self._description["path"].split("/")
            if part.startswith("{") and part.endswith("}")
        ]:
            if "path_params" not in call_params:
                raise ValueError("Path parameters are missing in path_params.")

            for placeholder in placeholders:
                if placeholder not in call_params["path_params"]:
                    raise ValueError(
                        f"Path parameter '{placeholder}' is missing in path_params."
                    )
