from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ...models.get_online_equipments_statuses_item import GetOnlineEquipmentsStatusesItem
from ...models.get_online_equipments_types_item import GetOnlineEquipmentsTypesItem
from qubicon.api.types import UNSET, Response, Unset


def _get_kwargs(
    *,
    server_id: Union[Unset, int] = UNSET,
    master_equipment_ids: Union[Unset, List[int]] = UNSET,
    parent_equipment_id: Union[Unset, int] = UNSET,
    ancestor_equipment_id: Union[Unset, int] = UNSET,
    standalone: Union[Unset, bool] = UNSET,
    statuses: Union[Unset, List[GetOnlineEquipmentsStatusesItem]] = UNSET,
    types: Union[Unset, List[GetOnlineEquipmentsTypesItem]] = UNSET,
    gmp: Union[Unset, bool] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["serverId"] = server_id

    json_master_equipment_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(master_equipment_ids, Unset):
        json_master_equipment_ids = master_equipment_ids

    params["masterEquipmentIds"] = json_master_equipment_ids

    params["parentEquipmentId"] = parent_equipment_id

    params["ancestorEquipmentId"] = ancestor_equipment_id

    params["standalone"] = standalone

    json_statuses: Union[Unset, List[str]] = UNSET
    if not isinstance(statuses, Unset):
        json_statuses = []
        for statuses_item_data in statuses:
            statuses_item = statuses_item_data.value
            json_statuses.append(statuses_item)

    params["statuses"] = json_statuses

    json_types: Union[Unset, List[str]] = UNSET
    if not isinstance(types, Unset):
        json_types = []
        for types_item_data in types:
            types_item = types_item_data.value
            json_types.append(types_item)

    params["types"] = json_types

    params["gmp"] = gmp

    json_sort: Union[Unset, List[str]] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params["page"] = page

    params["size"] = size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/public-api/online-equipment",
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
    server_id: Union[Unset, int] = UNSET,
    master_equipment_ids: Union[Unset, List[int]] = UNSET,
    parent_equipment_id: Union[Unset, int] = UNSET,
    ancestor_equipment_id: Union[Unset, int] = UNSET,
    standalone: Union[Unset, bool] = UNSET,
    statuses: Union[Unset, List[GetOnlineEquipmentsStatusesItem]] = UNSET,
    types: Union[Unset, List[GetOnlineEquipmentsTypesItem]] = UNSET,
    gmp: Union[Unset, bool] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        server_id (Union[Unset, int]):
        master_equipment_ids (Union[Unset, List[int]]):
        parent_equipment_id (Union[Unset, int]):
        ancestor_equipment_id (Union[Unset, int]):
        standalone (Union[Unset, bool]):
        statuses (Union[Unset, List[GetOnlineEquipmentsStatusesItem]]):
        types (Union[Unset, List[GetOnlineEquipmentsTypesItem]]):
        gmp (Union[Unset, bool]):
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
        server_id=server_id,
        master_equipment_ids=master_equipment_ids,
        parent_equipment_id=parent_equipment_id,
        ancestor_equipment_id=ancestor_equipment_id,
        standalone=standalone,
        statuses=statuses,
        types=types,
        gmp=gmp,
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
    server_id: Union[Unset, int] = UNSET,
    master_equipment_ids: Union[Unset, List[int]] = UNSET,
    parent_equipment_id: Union[Unset, int] = UNSET,
    ancestor_equipment_id: Union[Unset, int] = UNSET,
    standalone: Union[Unset, bool] = UNSET,
    statuses: Union[Unset, List[GetOnlineEquipmentsStatusesItem]] = UNSET,
    types: Union[Unset, List[GetOnlineEquipmentsTypesItem]] = UNSET,
    gmp: Union[Unset, bool] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        server_id (Union[Unset, int]):
        master_equipment_ids (Union[Unset, List[int]]):
        parent_equipment_id (Union[Unset, int]):
        ancestor_equipment_id (Union[Unset, int]):
        standalone (Union[Unset, bool]):
        statuses (Union[Unset, List[GetOnlineEquipmentsStatusesItem]]):
        types (Union[Unset, List[GetOnlineEquipmentsTypesItem]]):
        gmp (Union[Unset, bool]):
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
        server_id=server_id,
        master_equipment_ids=master_equipment_ids,
        parent_equipment_id=parent_equipment_id,
        ancestor_equipment_id=ancestor_equipment_id,
        standalone=standalone,
        statuses=statuses,
        types=types,
        gmp=gmp,
        sort=sort,
        page=page,
        size=size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
