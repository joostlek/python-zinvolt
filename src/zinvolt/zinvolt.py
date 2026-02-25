"""Asynchronous Python client for Zinvolt."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import logging
from typing import Any, Self

from aiohttp import ClientSession
from aiohttp.hdrs import METH_GET, METH_POST, METH_PUT
from mashumaro.codecs.orjson import ORJSONDecoder
import orjson
from yarl import URL

from zinvolt.models import (
    Battery,
    BatteryListResponse,
    BatteryState,
    BatteryUnit,
    CustomMode,
    GlobalSettings,
    OnlineStatus,
    OnlineStatusResponse,
    PhotovoltaicData,
    SmartMode,
)

VERSION = "1"

_LOGGER = logging.getLogger(__package__)

HOST = "app.zinvolt.com"


@dataclass
class ZinvoltClient:
    """Main class for handling connections with the Zinvolt API."""

    token: str | None = None
    session: ClientSession | None = None
    request_timeout: int = 10
    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        data: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> str:
        """Handle a request to the Zinvolt API."""
        url = URL.build(host=HOST, scheme="https").joinpath(f"api/public/v2/{uri}")
        base_headers = {
            "User-Agent": f"python-zinvolt/{VERSION}",
        }
        if self.token:
            base_headers["Authorization"] = f"Bearer {self.token}"

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        if headers is None:
            headers = {}

        async with asyncio.timeout(self.request_timeout):
            response = await self.session.request(
                method,
                url,
                headers=base_headers | headers,
                json=data,
            )

        return await response.text()

    async def _get(self, uri: str) -> str:
        """Handle a GET request to the Zinvolt API."""
        return await self._request(uri, method=METH_GET)

    async def _put(self, uri: str, data: dict[str, Any]) -> str:
        """Handle a PUT request to the Zinvolt API."""
        return await self._request(uri, method=METH_PUT, data=data)

    async def _post(self, uri: str, data: dict[str, Any]) -> str:
        """Handle a POST request to the Zinvolt API."""
        return await self._request(uri, method=METH_POST, data=data)

    async def login(self, email: str, password: str) -> str:
        """Login to the Zinvolt API."""
        result = await self._post("login", {"email": email, "password": password})
        self.token = orjson.loads(result)["token"]  # pylint: disable=no-member
        return self.token

    async def get_batteries(self) -> list[Battery]:
        """Retrieve the list of batteries from the Zinvolt API."""
        result = await self._get("system/batteries")
        return BatteryListResponse.from_json(result).batteries

    async def get_battery_status(self, battery_id: str) -> BatteryState:
        """Retrieve the battery status for the given battery ID."""
        result = await self._get(f"system/{battery_id}/basic/current-state")
        return BatteryState.from_json(result)

    async def is_battery_online(self, battery_id: str) -> bool:
        """Retrieve the battery status for the given battery ID."""
        result = await self._get(f"system/{battery_id}/basic/online-status")
        return (
            OnlineStatusResponse.from_json(result).online_status is OnlineStatus.ONLINE
        )

    async def get_photovoltaic_data(self, battery_id: str) -> list[PhotovoltaicData]:
        """Retrieve the photovoltaic data for the given battery ID."""
        result = await self._get(f"system/{battery_id}/basic/pv-data")
        return ORJSONDecoder(list[PhotovoltaicData]).decode(result)

    async def get_global_settings(self, battery_id: str) -> GlobalSettings:
        """Retrieve the global settings for the given battery ID."""
        result = await self._get(f"system/{battery_id}/configuration/global-settings")
        return GlobalSettings.from_json(result)

    async def get_custom_modes(self, battery_id: str) -> list[CustomMode]:
        """Retrieve the custom modes for the given battery ID."""
        result = await self._get(f"system/{battery_id}/custom-mode")
        return ORJSONDecoder(list[CustomMode]).decode(result)

    async def get_battery_unit(
        self, battery_id: str, battery_serial_number: str
    ) -> BatteryUnit:
        """Retrieve the battery unit for the given battery ID."""
        result = await self._get(
            f"system/{battery_id}/unit/battery/{battery_serial_number}"
        )
        return BatteryUnit.from_json(result)

    async def set_smart_mode(
        self, battery_id: str, smart_mode: SmartMode | str
    ) -> None:
        """Retrieve the custom modes for the given battery ID."""
        data: dict[str, Any] = {}
        if not isinstance(smart_mode, SmartMode):
            data["custom_mode_id"] = smart_mode
            data["mode"] = SmartMode.CUSTOM
        else:
            data["mode"] = smart_mode
        await self._put(f"system/{battery_id}/operation/switch-smart-mode", data=data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The ZinvoltClient object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
