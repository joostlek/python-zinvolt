"""Asynchronous Python client for Netgear routers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiohttp.hdrs import METH_GET, METH_POST
from aioresponses import aioresponses
import pytest

from . import load_fixture
from .const import HEADERS, URL

if TYPE_CHECKING:
    from syrupy import SnapshotAssertion
    from zinvolt.zinvolt import ZinvoltClient


async def test_login(
    responses: aioresponses,
    client: ZinvoltClient,
    snapshot: SnapshotAssertion,
) -> None:
    """Test loggign in."""
    responses.post(
        f"{URL}login",
        status=200,
        body=load_fixture("login.json"),
    )
    assert await client.login(email="test@test.com", password="abc") == snapshot
    responses.assert_called_once_with(
        f"{URL}login",
        METH_POST,
        headers=HEADERS,
        json={
            "email": "test@test.com",
            "password": "abc",
        },
    )


@pytest.mark.parametrize(
    ("method", "kwargs", "endpoint", "fixture"),
    [
        ("get_batteries", {}, "system/batteries", "batteries"),
        (
            "get_battery_status",
            {"battery_id": "123123"},
            "system/123123/basic/current-state",
            "current_state",
        ),
        (
            "is_battery_online",
            {"battery_id": "123123"},
            "system/123123/basic/online-status",
            "online_status",
        ),
        (
            "get_photovoltaic_data",
            {"battery_id": "123123"},
            "system/123123/basic/pv-data",
            "pv_data",
        ),
        (
            "get_global_settings",
            {"battery_id": "123123"},
            "system/123123/configuration/global-settings",
            "global_settings",
        ),
    ],
    ids=[
        "get_batteries",
        "get_battery_status",
        "is_battery_online",
        "get_photovoltaic_data",
        "get_global_settings",
    ],
)
async def test_retrieve_data(
    responses: aioresponses,
    client: ZinvoltClient,
    snapshot: SnapshotAssertion,
    method: str,
    kwargs: dict[str, Any],
    endpoint: str,
    fixture: str,
) -> None:
    """Test retrieving data."""
    responses.get(
        f"{URL}{endpoint}",
        status=200,
        body=load_fixture(f"{fixture}.json"),
    )
    assert await getattr(client, method)(**kwargs) == snapshot
    responses.assert_called_once_with(
        f"{URL}{endpoint}",
        METH_GET,
        headers=HEADERS,
        json=None,
    )
