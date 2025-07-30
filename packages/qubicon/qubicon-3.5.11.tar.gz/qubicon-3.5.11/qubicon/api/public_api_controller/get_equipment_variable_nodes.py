from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from qubicon.api import errors
from qubicon.api.client import AuthenticatedClient, Client
from qubicon.models.get_equipment_variable_nodes_node_usage_types_item import GetEquipmentVariableNodesNodeUsageTypesItem
from qubicon.api.types import UNSET, Response, Unset


def _get_kwargs(
    *,
    server_ids: Union[Unset, List[int]] = UNSET,
    equipment_ids: Union[Unset, List[int]] = UNSET,
    gmp_equipments: Union[Unset, bool] = UNSET,
    mapped: Union[Unset, bool] = UNSET,
    monitored: Union[Unset, bool] = UNSET,
    setpoint_phase_id_not: Union[Unset, int] = UNSET,
    node_usage_types: Union[Unset, List[GetEquipmentVariableNodesNodeUsageTypesItem]] = UNSET,
    process_id: Union[Unset, int] = UNSET,
    single_value: Union[Unset, bool] = UNSET,
    physical_quantity_unit_id: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_server_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(server_ids, Unset):
        json_server_ids = server_ids

    params["serverIds"] = json_server_ids

    json_equipment_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(equipment_ids, Unset):
        json_equipment_ids = equipment_ids

    params["equipmentIds"] = json_equipment_ids

    params["gmpEquipments"] = gmp_equipments

    params["mapped"] = mapped

    params["monitored"] = monitored

    params["setpointPhaseIdNot"] = setpoint_phase_id_not

    json_node_usage_types: Union[Unset, List[str]] = UNSET
    if not isinstance(node_usage_types, Unset):
        json_node_usage_types = []
        for node_usage_types_item_data in node_usage_types:
            node_usage_types_item = node_usage_types_item_data.value
            json_node_usage_types.append(node_usage_types_item)

    params["nodeUsageTypes"] = json_node_usage_types

    params["processId"] = process_id

    params["singleValue"] = single_value

    params["physicalQuantityUnitId"] = physical_quantity_unit_id

    params["search"] = search

    json_sort: Union[Unset, List[str]] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params["page"] = page

    params["size"] = size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/public-api/opcua-node/variable",
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
    server_ids: Union[Unset, List[int]] = UNSET,
    equipment_ids: Union[Unset, List[int]] = UNSET,
    gmp_equipments: Union[Unset, bool] = UNSET,
    mapped: Union[Unset, bool] = UNSET,
    monitored: Union[Unset, bool] = UNSET,
    setpoint_phase_id_not: Union[Unset, int] = UNSET,
    node_usage_types: Union[Unset, List[GetEquipmentVariableNodesNodeUsageTypesItem]] = UNSET,
    process_id: Union[Unset, int] = UNSET,
    single_value: Union[Unset, bool] = UNSET,
    physical_quantity_unit_id: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        server_ids (Union[Unset, List[int]]):
        equipment_ids (Union[Unset, List[int]]):
        gmp_equipments (Union[Unset, bool]):
        mapped (Union[Unset, bool]):
        monitored (Union[Unset, bool]):
        setpoint_phase_id_not (Union[Unset, int]):
        node_usage_types (Union[Unset, List[GetEquipmentVariableNodesNodeUsageTypesItem]]):
        process_id (Union[Unset, int]):
        single_value (Union[Unset, bool]):
        physical_quantity_unit_id (Union[Unset, int]):
        search (Union[Unset, str]):
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
        server_ids=server_ids,
        equipment_ids=equipment_ids,
        gmp_equipments=gmp_equipments,
        mapped=mapped,
        monitored=monitored,
        setpoint_phase_id_not=setpoint_phase_id_not,
        node_usage_types=node_usage_types,
        process_id=process_id,
        single_value=single_value,
        physical_quantity_unit_id=physical_quantity_unit_id,
        search=search,
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
    server_ids: Union[Unset, List[int]] = UNSET,
    equipment_ids: Union[Unset, List[int]] = UNSET,
    gmp_equipments: Union[Unset, bool] = UNSET,
    mapped: Union[Unset, bool] = UNSET,
    monitored: Union[Unset, bool] = UNSET,
    setpoint_phase_id_not: Union[Unset, int] = UNSET,
    node_usage_types: Union[Unset, List[GetEquipmentVariableNodesNodeUsageTypesItem]] = UNSET,
    process_id: Union[Unset, int] = UNSET,
    single_value: Union[Unset, bool] = UNSET,
    physical_quantity_unit_id: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        server_ids (Union[Unset, List[int]]):
        equipment_ids (Union[Unset, List[int]]):
        gmp_equipments (Union[Unset, bool]):
        mapped (Union[Unset, bool]):
        monitored (Union[Unset, bool]):
        setpoint_phase_id_not (Union[Unset, int]):
        node_usage_types (Union[Unset, List[GetEquipmentVariableNodesNodeUsageTypesItem]]):
        process_id (Union[Unset, int]):
        single_value (Union[Unset, bool]):
        physical_quantity_unit_id (Union[Unset, int]):
        search (Union[Unset, str]):
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
        server_ids=server_ids,
        equipment_ids=equipment_ids,
        gmp_equipments=gmp_equipments,
        mapped=mapped,
        monitored=monitored,
        setpoint_phase_id_not=setpoint_phase_id_not,
        node_usage_types=node_usage_types,
        process_id=process_id,
        single_value=single_value,
        physical_quantity_unit_id=physical_quantity_unit_id,
        search=search,
        sort=sort,
        page=page,
        size=size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
