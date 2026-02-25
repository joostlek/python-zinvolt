"""Asynchronous Python client for Netgear routers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiohttp.hdrs import METH_GET, METH_POST, METH_PUT
from aioresponses import aioresponses
import pytest

from zinvolt.models import SmartMode

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


async def test_set_smart_mode(responses: aioresponses, client: ZinvoltClient) -> None:
    """Test setting smart mode."""
    responses.put(
        f"{URL}system/123123/operation/switch-smart-mode",
        status=200,
    )
    await client.set_smart_mode(battery_id="123123", smart_mode=SmartMode.DYNAMIC)
    responses.assert_called_once_with(
        f"{URL}system/123123/operation/switch-smart-mode",
        METH_PUT,
        headers=HEADERS,
        json={"mode": "DYNAMIC"},
    )


async def test_set_custom_smart_mode(
    responses: aioresponses, client: ZinvoltClient
) -> None:
    """Test setting smart mode."""
    responses.put(
        f"{URL}system/123123/operation/switch-smart-mode",
        status=200,
    )
    await client.set_smart_mode(
        battery_id="123123", smart_mode="EdxM2EsVNJVc6abhbVnbeby5bcq5EBXh"
    )
    responses.assert_called_once_with(
        f"{URL}system/123123/operation/switch-smart-mode",
        METH_PUT,
        headers=HEADERS,
        json={
            "mode": "CUSTOM",
            "custom_mode_id": "EdxM2EsVNJVc6abhbVnbeby5bcq5EBXh",
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
        (
            "get_custom_modes",
            {"battery_id": "123123"},
            "system/123123/custom-mode",
            "custom_modes",
        ),
        (
            "get_battery_unit",
            {"battery_id": "123123", "battery_serial_number": "abc123"},
            "system/123123/unit/battery/abc123",
            "battery_unit",
        ),
    ],
    ids=[
        "get_batteries",
        "get_battery_status",
        "is_battery_online",
        "get_photovoltaic_data",
        "get_global_settings",
        "get_custom_modes",
        "get_battery_unit",
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


@pytest.mark.parametrize(
    ("method", "kwargs", "data"),
    [
        (
            "set_max_output",
            {"max_output": 500},
            {"max_output": 500},
        ),
        (
            "set_lower_threshold",
            {"lower_threshold": 500},
            {"bat_use_cap": 500},
        ),
        (
            "set_upper_threshold",
            {"upper_threshold": 500},
            {"max_charge_power": 500},
        ),
        (
            "set_standby_time",
            {"standby_time": 500},
            {"standby_time": 500},
        ),
    ],
    ids=[
        "set_max_output",
        "set_lower_threshold",
        "set_upper_threshold",
        "set_standby_time",
    ],
)
async def test_setting_global_settings(
    responses: aioresponses,
    client: ZinvoltClient,
    method: str,
    kwargs: dict[str, Any],
    data: dict[str, Any],
) -> None:
    """Test setting global settings."""
    responses.post(
        f"{URL}system/123123/configuration/global-settings",
        status=200,
    )
    await getattr(client, method)(**(kwargs | {"battery_id": "123123"}))
    responses.assert_called_once_with(
        f"{URL}system/123123/configuration/global-settings",
        METH_POST,
        headers=HEADERS,
        json=data,
    )
