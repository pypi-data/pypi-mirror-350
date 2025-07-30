import json
from enum import Enum
from typing import (
    Any,
    Optional,
    TypeVar,
    get_args,
    get_origin,
)

import httpx
from dacite import Config, from_dict

from ..CommunicatorConfiguration import CommunicatorConfiguration
from ..errors import (
    ApiErrorResponseException,
    ApiResponseRetrievalException,
)
from ..models import ErrorResponse
from ..RequestHeaderGenerator import RequestHeaderGenerator

T = TypeVar("T")


def from_dict_with_enum(
    data_class: type[T],
    data: dict[str, Any],
) -> T:
    return from_dict(data_class=data_class, data=data, config=Config(cast=[Enum]))


def is_error_response(parsed: Any) -> bool:
    if not isinstance(parsed, dict):
        return False
    if "errorId" in parsed and not isinstance(parsed["errorId"], str):
        return False
    if "errors" in parsed and not isinstance(parsed["errors"], list):  # noqa: SIM103
        return False
    return True


class BaseApiClient:
    CONTENT_TYPE = "application/json"
    MERCHANT_ID_REQUIRED_ERROR = "Merchant ID is required"
    COMMERCE_CASE_ID_REQUIRED_ERROR = "Commerce Case ID is required"
    CHECKOUT_ID_REQUIRED_ERROR = "Checkout ID is required"
    PAYMENT_INFORMATION_ID_REQUIRED_ERROR = "Payment Information ID is required"
    PAYMENT_EXECUTION_ID_REQUIRED_ERROR = "Payment Execution ID is required"

    def __init__(self, config: CommunicatorConfiguration):
        self.config = config
        self.request_header_generator = RequestHeaderGenerator(config)

    def get_request_header_generator(self) -> Optional[RequestHeaderGenerator]:
        return self.request_header_generator

    def get_config(self) -> CommunicatorConfiguration:
        return self.config

    async def make_api_call(self, request: httpx.Request) -> None:
        if self.request_header_generator:
            request = self.request_header_generator.generate_additional_request_headers(
                request
            )
        response = await self.get_response(request)

        await self.handle_error(response)

    async def make_api_call_with_type(self, request: httpx.Request, type: type[T]) -> T:
        if self.request_header_generator:
            request = self.request_header_generator.generate_additional_request_headers(
                request
            )
        response = await self.get_response(request)
        await self.handle_error(response)
        try:
            data = json.loads(response.text)
            # Check if the expected type is a List
            if get_origin(type) is list:
                item_type = get_args(type)[0]  # Extract the type of the list's elements
                return [
                    from_dict_with_enum(data_class=item_type, data=item)
                    for item in data
                ]
            else:
                return from_dict_with_enum(data_class=type, data=data)
        except json.JSONDecodeError as e:
            raise AssertionError(self.JSON_PARSE_ERROR) from e

    async def handle_error(self, response: httpx.Response) -> None:
        if response.is_success:
            return

        response_body = response.text
        if not response_body:
            raise ApiResponseRetrievalException(response.status_code, response_body)
        try:
            data = json.loads(response.text)
            error = from_dict_with_enum(data_class=ErrorResponse, data=data)
            raise ApiErrorResponseException(
                response.status_code, response_body, error.errors
            )
        except json.JSONDecodeError as e:
            raise ApiResponseRetrievalException(response.status_code, response_body, e)  # noqa: B904

    async def get_response(self, request: httpx.Request) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=str(request.url),
                headers=request.headers,
                content=request.content,
            )

        return response
