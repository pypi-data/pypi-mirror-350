from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from qubicon.api import errors
from qubicon.api.client import AuthenticatedClient, Client
from qubicon.models.import_offline_equipment_data_file_async_body import ImportOfflineEquipmentDataFileAsyncBody
from qubicon.models.job_dto import JobDto
from qubicon.api.types import Response


def _get_kwargs(
    id: int,
    *,
    body: ImportOfflineEquipmentDataFileAsyncBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/public-api/offline-equipment/{id}/import",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[JobDto]:
    if response.status_code == 200:
        response_200 = JobDto.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[JobDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ImportOfflineEquipmentDataFileAsyncBody,
) -> Response[JobDto]:
    """
    Args:
        id (int):
        body (ImportOfflineEquipmentDataFileAsyncBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobDto]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ImportOfflineEquipmentDataFileAsyncBody,
) -> Optional[JobDto]:
    """
    Args:
        id (int):
        body (ImportOfflineEquipmentDataFileAsyncBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobDto
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ImportOfflineEquipmentDataFileAsyncBody,
) -> Response[JobDto]:
    """
    Args:
        id (int):
        body (ImportOfflineEquipmentDataFileAsyncBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobDto]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ImportOfflineEquipmentDataFileAsyncBody,
) -> Optional[JobDto]:
    """
    Args:
        id (int):
        body (ImportOfflineEquipmentDataFileAsyncBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobDto
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
