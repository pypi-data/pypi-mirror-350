from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ...models.get_list_of_computable_models_calculation_styles_item import (
    GetListOfComputableModelsCalculationStylesItem,
)
from ...models.get_list_of_computable_models_statuses_item import GetListOfComputableModelsStatusesItem
from ...models.get_list_of_computable_models_types_item import GetListOfComputableModelsTypesItem
from qubicon.api.types import UNSET, Response, Unset


def _get_kwargs(
    *,
    statuses: Union[Unset, List[GetListOfComputableModelsStatusesItem]] = UNSET,
    calculation_styles: Union[Unset, List[GetListOfComputableModelsCalculationStylesItem]] = UNSET,
    types: Union[Unset, List[GetListOfComputableModelsTypesItem]] = UNSET,
    output_physical_quantity_unit_ids: Union[Unset, List[int]] = UNSET,
    output_physical_quantity_ids: Union[Unset, List[int]] = UNSET,
    name: Union[Unset, str] = UNSET,
    deleted: Union[Unset, bool] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_statuses: Union[Unset, List[str]] = UNSET
    if not isinstance(statuses, Unset):
        json_statuses = []
        for statuses_item_data in statuses:
            statuses_item = statuses_item_data.value
            json_statuses.append(statuses_item)

    params["statuses"] = json_statuses

    json_calculation_styles: Union[Unset, List[str]] = UNSET
    if not isinstance(calculation_styles, Unset):
        json_calculation_styles = []
        for calculation_styles_item_data in calculation_styles:
            calculation_styles_item = calculation_styles_item_data.value
            json_calculation_styles.append(calculation_styles_item)

    params["calculationStyles"] = json_calculation_styles

    json_types: Union[Unset, List[str]] = UNSET
    if not isinstance(types, Unset):
        json_types = []
        for types_item_data in types:
            types_item = types_item_data.value
            json_types.append(types_item)

    params["types"] = json_types

    json_output_physical_quantity_unit_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(output_physical_quantity_unit_ids, Unset):
        json_output_physical_quantity_unit_ids = output_physical_quantity_unit_ids

    params["outputPhysicalQuantityUnitIds"] = json_output_physical_quantity_unit_ids

    json_output_physical_quantity_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(output_physical_quantity_ids, Unset):
        json_output_physical_quantity_ids = output_physical_quantity_ids

    params["outputPhysicalQuantityIds"] = json_output_physical_quantity_ids

    params["name"] = name

    params["deleted"] = deleted

    json_sort: Union[Unset, List[str]] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params["page"] = page

    params["size"] = size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/public-api/computable-models",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    statuses: Union[Unset, List[GetListOfComputableModelsStatusesItem]] = UNSET,
    calculation_styles: Union[Unset, List[GetListOfComputableModelsCalculationStylesItem]] = UNSET,
    types: Union[Unset, List[GetListOfComputableModelsTypesItem]] = UNSET,
    output_physical_quantity_unit_ids: Union[Unset, List[int]] = UNSET,
    output_physical_quantity_ids: Union[Unset, List[int]] = UNSET,
    name: Union[Unset, str] = UNSET,
    deleted: Union[Unset, bool] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        statuses (Union[Unset, List[GetListOfComputableModelsStatusesItem]]):
        calculation_styles (Union[Unset, List[GetListOfComputableModelsCalculationStylesItem]]):
        types (Union[Unset, List[GetListOfComputableModelsTypesItem]]):
        output_physical_quantity_unit_ids (Union[Unset, List[int]]):
        output_physical_quantity_ids (Union[Unset, List[int]]):
        name (Union[Unset, str]):
        deleted (Union[Unset, bool]):
        sort (Union[Unset, List[str]]):
        page (Union[Unset, int]):
        size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        statuses=statuses,
        calculation_styles=calculation_styles,
        types=types,
        output_physical_quantity_unit_ids=output_physical_quantity_unit_ids,
        output_physical_quantity_ids=output_physical_quantity_ids,
        name=name,
        deleted=deleted,
        sort=sort,
        page=page,
        size=size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    statuses: Union[Unset, List[GetListOfComputableModelsStatusesItem]] = UNSET,
    calculation_styles: Union[Unset, List[GetListOfComputableModelsCalculationStylesItem]] = UNSET,
    types: Union[Unset, List[GetListOfComputableModelsTypesItem]] = UNSET,
    output_physical_quantity_unit_ids: Union[Unset, List[int]] = UNSET,
    output_physical_quantity_ids: Union[Unset, List[int]] = UNSET,
    name: Union[Unset, str] = UNSET,
    deleted: Union[Unset, bool] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        statuses (Union[Unset, List[GetListOfComputableModelsStatusesItem]]):
        calculation_styles (Union[Unset, List[GetListOfComputableModelsCalculationStylesItem]]):
        types (Union[Unset, List[GetListOfComputableModelsTypesItem]]):
        output_physical_quantity_unit_ids (Union[Unset, List[int]]):
        output_physical_quantity_ids (Union[Unset, List[int]]):
        name (Union[Unset, str]):
        deleted (Union[Unset, bool]):
        sort (Union[Unset, List[str]]):
        page (Union[Unset, int]):
        size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        statuses=statuses,
        calculation_styles=calculation_styles,
        types=types,
        output_physical_quantity_unit_ids=output_physical_quantity_unit_ids,
        output_physical_quantity_ids=output_physical_quantity_ids,
        name=name,
        deleted=deleted,
        sort=sort,
        page=page,
        size=size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
