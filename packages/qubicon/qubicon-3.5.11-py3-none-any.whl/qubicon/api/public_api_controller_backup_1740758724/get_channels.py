from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ...models.get_channels_node_types_item import GetChannelsNodeTypesItem
from qubicon.api.types import UNSET, Response, Unset


def _get_kwargs(
    process_id: int,
    *,
    process_phase_id: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    node_types: Union[Unset, List[GetChannelsNodeTypesItem]] = UNSET,
    sensor_type_ids: Union[Unset, List[int]] = UNSET,
    physical_quantity_unit_id: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["processPhaseId"] = process_phase_id

    params["name"] = name

    json_node_types: Union[Unset, List[str]] = UNSET
    if not isinstance(node_types, Unset):
        json_node_types = []
        for node_types_item_data in node_types:
            node_types_item = node_types_item_data.value
            json_node_types.append(node_types_item)

    params["nodeTypes"] = json_node_types

    json_sensor_type_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(sensor_type_ids, Unset):
        json_sensor_type_ids = sensor_type_ids

    params["sensorTypeIds"] = json_sensor_type_ids

    params["physicalQuantityUnitId"] = physical_quantity_unit_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/public-api/processes/{process_id}/channels",
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
    process_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    process_phase_id: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    node_types: Union[Unset, List[GetChannelsNodeTypesItem]] = UNSET,
    sensor_type_ids: Union[Unset, List[int]] = UNSET,
    physical_quantity_unit_id: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        process_id (int):
        process_phase_id (Union[Unset, int]):
        name (Union[Unset, str]):
        node_types (Union[Unset, List[GetChannelsNodeTypesItem]]):
        sensor_type_ids (Union[Unset, List[int]]):
        physical_quantity_unit_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        process_phase_id=process_phase_id,
        name=name,
        node_types=node_types,
        sensor_type_ids=sensor_type_ids,
        physical_quantity_unit_id=physical_quantity_unit_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    process_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    process_phase_id: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    node_types: Union[Unset, List[GetChannelsNodeTypesItem]] = UNSET,
    sensor_type_ids: Union[Unset, List[int]] = UNSET,
    physical_quantity_unit_id: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        process_id (int):
        process_phase_id (Union[Unset, int]):
        name (Union[Unset, str]):
        node_types (Union[Unset, List[GetChannelsNodeTypesItem]]):
        sensor_type_ids (Union[Unset, List[int]]):
        physical_quantity_unit_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        process_id=process_id,
        process_phase_id=process_phase_id,
        name=name,
        node_types=node_types,
        sensor_type_ids=sensor_type_ids,
        physical_quantity_unit_id=physical_quantity_unit_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
