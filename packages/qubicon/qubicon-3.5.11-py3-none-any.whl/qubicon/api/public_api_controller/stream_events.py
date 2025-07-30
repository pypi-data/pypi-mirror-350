from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from qubicon.api import errors
from qubicon.api.client import AuthenticatedClient, Client
from qubicon.models.server_sent_event_abstract_server_sent_event_dto import ServerSentEventAbstractServerSentEventDto
from qubicon.models.stream_events_types_item import StreamEventsTypesItem
from qubicon.api.types import UNSET, Response, Unset


def _get_kwargs(
    *,
    types: Union[Unset, List[StreamEventsTypesItem]] = UNSET,
    nonce: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_types: Union[Unset, List[str]] = UNSET
    if not isinstance(types, Unset):
        json_types = []
        for types_item_data in types:
            types_item = types_item_data.value
            json_types.append(types_item)

    params["types"] = json_types

    params["nonce"] = nonce

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/public-api/events-stream",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ServerSentEventAbstractServerSentEventDto"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.text
        for response_200_item_data in _response_200:
            response_200_item = ServerSentEventAbstractServerSentEventDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ServerSentEventAbstractServerSentEventDto"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    types: Union[Unset, List[StreamEventsTypesItem]] = UNSET,
    nonce: Union[Unset, str] = UNSET,
) -> Response[List["ServerSentEventAbstractServerSentEventDto"]]:
    """
    Args:
        types (Union[Unset, List[StreamEventsTypesItem]]):
        nonce (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ServerSentEventAbstractServerSentEventDto']]
    """

    kwargs = _get_kwargs(
        types=types,
        nonce=nonce,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    types: Union[Unset, List[StreamEventsTypesItem]] = UNSET,
    nonce: Union[Unset, str] = UNSET,
) -> Optional[List["ServerSentEventAbstractServerSentEventDto"]]:
    """
    Args:
        types (Union[Unset, List[StreamEventsTypesItem]]):
        nonce (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ServerSentEventAbstractServerSentEventDto']
    """

    return sync_detailed(
        client=client,
        types=types,
        nonce=nonce,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    types: Union[Unset, List[StreamEventsTypesItem]] = UNSET,
    nonce: Union[Unset, str] = UNSET,
) -> Response[List["ServerSentEventAbstractServerSentEventDto"]]:
    """
    Args:
        types (Union[Unset, List[StreamEventsTypesItem]]):
        nonce (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ServerSentEventAbstractServerSentEventDto']]
    """

    kwargs = _get_kwargs(
        types=types,
        nonce=nonce,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    types: Union[Unset, List[StreamEventsTypesItem]] = UNSET,
    nonce: Union[Unset, str] = UNSET,
) -> Optional[List["ServerSentEventAbstractServerSentEventDto"]]:
    """
    Args:
        types (Union[Unset, List[StreamEventsTypesItem]]):
        nonce (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ServerSentEventAbstractServerSentEventDto']
    """

    return (
        await asyncio_detailed(
            client=client,
            types=types,
            nonce=nonce,
        )
    ).parsed
