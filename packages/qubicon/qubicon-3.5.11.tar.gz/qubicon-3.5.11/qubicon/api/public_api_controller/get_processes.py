from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from qubicon.api import errors
from qubicon.api.client import AuthenticatedClient, Client
from qubicon.models.get_processes_statuses_item import GetProcessesStatusesItem
from qubicon.models.get_processes_types_item import GetProcessesTypesItem
from qubicon.api.types import UNSET, Response, Unset


def _get_kwargs(
    *,
    name: Union[Unset, str] = UNSET,
    deleted: Union[Unset, bool] = UNSET,
    start_date: Union[Unset, int] = UNSET,
    end_date: Union[Unset, int] = UNSET,
    statuses: Union[Unset, List[GetProcessesStatusesItem]] = UNSET,
    archived_or_will_be_archived: Union[Unset, bool] = UNSET,
    types: Union[Unset, List[GetProcessesTypesItem]] = UNSET,
    ids: Union[Unset, List[int]] = UNSET,
    lot_ids: Union[Unset, List[int]] = UNSET,
    organism_ids: Union[Unset, List[int]] = UNSET,
    kpi_model_ids: Union[Unset, List[int]] = UNSET,
    material_ids: Union[Unset, List[int]] = UNSET,
    stream_ids: Union[Unset, List[int]] = UNSET,
    user_stream_ids: Union[Unset, List[int]] = UNSET,
    online_equipment_ids: Union[Unset, List[int]] = UNSET,
    offline_equipment_ids: Union[Unset, List[int]] = UNSET,
    online_equipment_group_first_ids: Union[Unset, List[int]] = UNSET,
    offline_equipment_group_first_ids: Union[Unset, List[int]] = UNSET,
    recipe_ids: Union[Unset, List[int]] = UNSET,
    organism_and_vial_tuples: Union[Unset, List[str]] = UNSET,
    material_and_lot_tuples: Union[Unset, List[str]] = UNSET,
    gmp: Union[Unset, bool] = UNSET,
    imported: Union[Unset, bool] = UNSET,
    group_ids: Union[Unset, List[int]] = UNSET,
    master_recipe_ids: Union[Unset, List[int]] = UNSET,
    part_of_experiment: Union[Unset, bool] = UNSET,
    sampling_values: Union[Unset, List[str]] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["name"] = name

    params["deleted"] = deleted

    params["startDate"] = start_date

    params["endDate"] = end_date

    json_statuses: Union[Unset, List[str]] = UNSET
    if not isinstance(statuses, Unset):
        json_statuses = []
        for statuses_item_data in statuses:
            statuses_item = statuses_item_data.value
            json_statuses.append(statuses_item)

    params["statuses"] = json_statuses

    params["archivedOrWillBeArchived"] = archived_or_will_be_archived

    json_types: Union[Unset, List[str]] = UNSET
    if not isinstance(types, Unset):
        json_types = []
        for types_item_data in types:
            types_item = types_item_data.value
            json_types.append(types_item)

    params["types"] = json_types

    json_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(ids, Unset):
        json_ids = ids

    params["ids"] = json_ids

    json_lot_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(lot_ids, Unset):
        json_lot_ids = lot_ids

    params["lotIds"] = json_lot_ids

    json_organism_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(organism_ids, Unset):
        json_organism_ids = organism_ids

    params["organismIds"] = json_organism_ids

    json_kpi_model_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(kpi_model_ids, Unset):
        json_kpi_model_ids = kpi_model_ids

    params["kpiModelIds"] = json_kpi_model_ids

    json_material_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(material_ids, Unset):
        json_material_ids = material_ids

    params["materialIds"] = json_material_ids

    json_stream_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(stream_ids, Unset):
        json_stream_ids = stream_ids

    params["streamIds"] = json_stream_ids

    json_user_stream_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(user_stream_ids, Unset):
        json_user_stream_ids = user_stream_ids

    params["userStreamIds"] = json_user_stream_ids

    json_online_equipment_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(online_equipment_ids, Unset):
        json_online_equipment_ids = online_equipment_ids

    params["onlineEquipmentIds"] = json_online_equipment_ids

    json_offline_equipment_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(offline_equipment_ids, Unset):
        json_offline_equipment_ids = offline_equipment_ids

    params["offlineEquipmentIds"] = json_offline_equipment_ids

    json_online_equipment_group_first_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(online_equipment_group_first_ids, Unset):
        json_online_equipment_group_first_ids = online_equipment_group_first_ids

    params["onlineEquipmentGroupFirstIds"] = json_online_equipment_group_first_ids

    json_offline_equipment_group_first_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(offline_equipment_group_first_ids, Unset):
        json_offline_equipment_group_first_ids = offline_equipment_group_first_ids

    params["offlineEquipmentGroupFirstIds"] = json_offline_equipment_group_first_ids

    json_recipe_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(recipe_ids, Unset):
        json_recipe_ids = recipe_ids

    params["recipeIds"] = json_recipe_ids

    json_organism_and_vial_tuples: Union[Unset, List[str]] = UNSET
    if not isinstance(organism_and_vial_tuples, Unset):
        json_organism_and_vial_tuples = organism_and_vial_tuples

    params["organismAndVialTuples"] = json_organism_and_vial_tuples

    json_material_and_lot_tuples: Union[Unset, List[str]] = UNSET
    if not isinstance(material_and_lot_tuples, Unset):
        json_material_and_lot_tuples = material_and_lot_tuples

    params["materialAndLotTuples"] = json_material_and_lot_tuples

    params["gmp"] = gmp

    params["imported"] = imported

    json_group_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(group_ids, Unset):
        json_group_ids = group_ids

    params["groupIds"] = json_group_ids

    json_master_recipe_ids: Union[Unset, List[int]] = UNSET
    if not isinstance(master_recipe_ids, Unset):
        json_master_recipe_ids = master_recipe_ids

    params["masterRecipeIds"] = json_master_recipe_ids

    params["partOfExperiment"] = part_of_experiment

    json_sampling_values: Union[Unset, List[str]] = UNSET
    if not isinstance(sampling_values, Unset):
        json_sampling_values = sampling_values

    params["samplingValues"] = json_sampling_values

    json_sort: Union[Unset, List[str]] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    params["page"] = page

    params["size"] = size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/public-api/processes",
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
    name: Union[Unset, str] = UNSET,
    deleted: Union[Unset, bool] = UNSET,
    start_date: Union[Unset, int] = UNSET,
    end_date: Union[Unset, int] = UNSET,
    statuses: Union[Unset, List[GetProcessesStatusesItem]] = UNSET,
    archived_or_will_be_archived: Union[Unset, bool] = UNSET,
    types: Union[Unset, List[GetProcessesTypesItem]] = UNSET,
    ids: Union[Unset, List[int]] = UNSET,
    lot_ids: Union[Unset, List[int]] = UNSET,
    organism_ids: Union[Unset, List[int]] = UNSET,
    kpi_model_ids: Union[Unset, List[int]] = UNSET,
    material_ids: Union[Unset, List[int]] = UNSET,
    stream_ids: Union[Unset, List[int]] = UNSET,
    user_stream_ids: Union[Unset, List[int]] = UNSET,
    online_equipment_ids: Union[Unset, List[int]] = UNSET,
    offline_equipment_ids: Union[Unset, List[int]] = UNSET,
    online_equipment_group_first_ids: Union[Unset, List[int]] = UNSET,
    offline_equipment_group_first_ids: Union[Unset, List[int]] = UNSET,
    recipe_ids: Union[Unset, List[int]] = UNSET,
    organism_and_vial_tuples: Union[Unset, List[str]] = UNSET,
    material_and_lot_tuples: Union[Unset, List[str]] = UNSET,
    gmp: Union[Unset, bool] = UNSET,
    imported: Union[Unset, bool] = UNSET,
    group_ids: Union[Unset, List[int]] = UNSET,
    master_recipe_ids: Union[Unset, List[int]] = UNSET,
    part_of_experiment: Union[Unset, bool] = UNSET,
    sampling_values: Union[Unset, List[str]] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        name (Union[Unset, str]):
        deleted (Union[Unset, bool]):
        start_date (Union[Unset, int]):
        end_date (Union[Unset, int]):
        statuses (Union[Unset, List[GetProcessesStatusesItem]]):
        archived_or_will_be_archived (Union[Unset, bool]):
        types (Union[Unset, List[GetProcessesTypesItem]]):
        ids (Union[Unset, List[int]]):
        lot_ids (Union[Unset, List[int]]):
        organism_ids (Union[Unset, List[int]]):
        kpi_model_ids (Union[Unset, List[int]]):
        material_ids (Union[Unset, List[int]]):
        stream_ids (Union[Unset, List[int]]):
        user_stream_ids (Union[Unset, List[int]]):
        online_equipment_ids (Union[Unset, List[int]]):
        offline_equipment_ids (Union[Unset, List[int]]):
        online_equipment_group_first_ids (Union[Unset, List[int]]):
        offline_equipment_group_first_ids (Union[Unset, List[int]]):
        recipe_ids (Union[Unset, List[int]]):
        organism_and_vial_tuples (Union[Unset, List[str]]):
        material_and_lot_tuples (Union[Unset, List[str]]):
        gmp (Union[Unset, bool]):
        imported (Union[Unset, bool]):
        group_ids (Union[Unset, List[int]]):
        master_recipe_ids (Union[Unset, List[int]]):
        part_of_experiment (Union[Unset, bool]):
        sampling_values (Union[Unset, List[str]]):
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
        name=name,
        deleted=deleted,
        start_date=start_date,
        end_date=end_date,
        statuses=statuses,
        archived_or_will_be_archived=archived_or_will_be_archived,
        types=types,
        ids=ids,
        lot_ids=lot_ids,
        organism_ids=organism_ids,
        kpi_model_ids=kpi_model_ids,
        material_ids=material_ids,
        stream_ids=stream_ids,
        user_stream_ids=user_stream_ids,
        online_equipment_ids=online_equipment_ids,
        offline_equipment_ids=offline_equipment_ids,
        online_equipment_group_first_ids=online_equipment_group_first_ids,
        offline_equipment_group_first_ids=offline_equipment_group_first_ids,
        recipe_ids=recipe_ids,
        organism_and_vial_tuples=organism_and_vial_tuples,
        material_and_lot_tuples=material_and_lot_tuples,
        gmp=gmp,
        imported=imported,
        group_ids=group_ids,
        master_recipe_ids=master_recipe_ids,
        part_of_experiment=part_of_experiment,
        sampling_values=sampling_values,
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
    name: Union[Unset, str] = UNSET,
    deleted: Union[Unset, bool] = UNSET,
    start_date: Union[Unset, int] = UNSET,
    end_date: Union[Unset, int] = UNSET,
    statuses: Union[Unset, List[GetProcessesStatusesItem]] = UNSET,
    archived_or_will_be_archived: Union[Unset, bool] = UNSET,
    types: Union[Unset, List[GetProcessesTypesItem]] = UNSET,
    ids: Union[Unset, List[int]] = UNSET,
    lot_ids: Union[Unset, List[int]] = UNSET,
    organism_ids: Union[Unset, List[int]] = UNSET,
    kpi_model_ids: Union[Unset, List[int]] = UNSET,
    material_ids: Union[Unset, List[int]] = UNSET,
    stream_ids: Union[Unset, List[int]] = UNSET,
    user_stream_ids: Union[Unset, List[int]] = UNSET,
    online_equipment_ids: Union[Unset, List[int]] = UNSET,
    offline_equipment_ids: Union[Unset, List[int]] = UNSET,
    online_equipment_group_first_ids: Union[Unset, List[int]] = UNSET,
    offline_equipment_group_first_ids: Union[Unset, List[int]] = UNSET,
    recipe_ids: Union[Unset, List[int]] = UNSET,
    organism_and_vial_tuples: Union[Unset, List[str]] = UNSET,
    material_and_lot_tuples: Union[Unset, List[str]] = UNSET,
    gmp: Union[Unset, bool] = UNSET,
    imported: Union[Unset, bool] = UNSET,
    group_ids: Union[Unset, List[int]] = UNSET,
    master_recipe_ids: Union[Unset, List[int]] = UNSET,
    part_of_experiment: Union[Unset, bool] = UNSET,
    sampling_values: Union[Unset, List[str]] = UNSET,
    sort: Union[Unset, List[str]] = UNSET,
    page: Union[Unset, int] = UNSET,
    size: Union[Unset, int] = UNSET,
) -> Response[Any]:
    """
    Args:
        name (Union[Unset, str]):
        deleted (Union[Unset, bool]):
        start_date (Union[Unset, int]):
        end_date (Union[Unset, int]):
        statuses (Union[Unset, List[GetProcessesStatusesItem]]):
        archived_or_will_be_archived (Union[Unset, bool]):
        types (Union[Unset, List[GetProcessesTypesItem]]):
        ids (Union[Unset, List[int]]):
        lot_ids (Union[Unset, List[int]]):
        organism_ids (Union[Unset, List[int]]):
        kpi_model_ids (Union[Unset, List[int]]):
        material_ids (Union[Unset, List[int]]):
        stream_ids (Union[Unset, List[int]]):
        user_stream_ids (Union[Unset, List[int]]):
        online_equipment_ids (Union[Unset, List[int]]):
        offline_equipment_ids (Union[Unset, List[int]]):
        online_equipment_group_first_ids (Union[Unset, List[int]]):
        offline_equipment_group_first_ids (Union[Unset, List[int]]):
        recipe_ids (Union[Unset, List[int]]):
        organism_and_vial_tuples (Union[Unset, List[str]]):
        material_and_lot_tuples (Union[Unset, List[str]]):
        gmp (Union[Unset, bool]):
        imported (Union[Unset, bool]):
        group_ids (Union[Unset, List[int]]):
        master_recipe_ids (Union[Unset, List[int]]):
        part_of_experiment (Union[Unset, bool]):
        sampling_values (Union[Unset, List[str]]):
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
        name=name,
        deleted=deleted,
        start_date=start_date,
        end_date=end_date,
        statuses=statuses,
        archived_or_will_be_archived=archived_or_will_be_archived,
        types=types,
        ids=ids,
        lot_ids=lot_ids,
        organism_ids=organism_ids,
        kpi_model_ids=kpi_model_ids,
        material_ids=material_ids,
        stream_ids=stream_ids,
        user_stream_ids=user_stream_ids,
        online_equipment_ids=online_equipment_ids,
        offline_equipment_ids=offline_equipment_ids,
        online_equipment_group_first_ids=online_equipment_group_first_ids,
        offline_equipment_group_first_ids=offline_equipment_group_first_ids,
        recipe_ids=recipe_ids,
        organism_and_vial_tuples=organism_and_vial_tuples,
        material_and_lot_tuples=material_and_lot_tuples,
        gmp=gmp,
        imported=imported,
        group_ids=group_ids,
        master_recipe_ids=master_recipe_ids,
        part_of_experiment=part_of_experiment,
        sampling_values=sampling_values,
        sort=sort,
        page=page,
        size=size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
