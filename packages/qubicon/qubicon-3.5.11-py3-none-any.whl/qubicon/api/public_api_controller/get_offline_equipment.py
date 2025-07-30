from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from qubicon.api import errors
from qubicon.api.client import AuthenticatedClient, Client
from qubicon.models.get_offline_equipment_statuses_item import GetOfflineEquipmentStatusesItem
from qubicon.api.types import UNSET, Response, Unset


def _get_kwargs(
    *,
    search: Union[Unset, str] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    statuses: Union[Unset, List[GetOfflineEquipmentStatusesItem]] = UNSET,
    gmp: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["search"] = search

    json_sort: Union[Unset, List[str]] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    json_statuses: Union[Unset, List[str]] = UNSET
    if not isinstance(statuses, Unset):
        json_statuses = []
        for statuses_item_data in statuses:
            statuses_item = statuses_item_data.value
            json_statuses.append(statuses_item)

    params["statuses"] = json_statuses

    params["gmp"] = gmp

    params["page"] = page

    params["size"] = size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/public-api/offline-equipment",
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
    search: Union[Unset, str] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    statuses: Union[Unset, List[GetOfflineEquipmentStatusesItem]] = UNSET,
    gmp: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        search (Union[Unset, str]):
        sort (Union[Unset, List[str]]):
        statuses (Union[Unset, List[GetOfflineEquipmentStatusesItem]]):
        gmp (Union[Unset, bool]):
        page (Union[Unset, int]):
        size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        search=search,
        sort=sort,
        statuses=statuses,
        gmp=gmp,
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
    search: Union[Unset, str] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    statuses: Union[Unset, List[GetOfflineEquipmentStatusesItem]] = UNSET,
    gmp: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        search (Union[Unset, str]):
        sort (Union[Unset, List[str]]):
        statuses (Union[Unset, List[GetOfflineEquipmentStatusesItem]]):
        gmp (Union[Unset, bool]):
        page (Union[Unset, int]):
        size (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        search=search,
        sort=sort,
        statuses=statuses,
        gmp=gmp,
        page=page,
        size=size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
