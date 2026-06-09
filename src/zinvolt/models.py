"""NetgearPy models for device settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class Battery(DataClassORJSONMixin):
    """Battery model."""

    identifier: str = field(metadata=field_options(alias="id"))
    name: str
    serial_number: str


@dataclass
class BatteryListResponse(DataClassORJSONMixin):
    """Battery list response."""

    batteries: list[Battery]


@dataclass
class CustomMode(DataClassORJSONMixin):
    """Custom mode."""

    mode_id: str = field(metadata=field_options(alias="confId"))
    serial_number: str = field(metadata=field_options(alias="sn"))
    name: str
    weeks: list[int]
    enable: bool


class OnlineStatus(StrEnum):
    """Online status."""

    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class SmartMode(StrEnum):
    """Smart mode."""

    DYNAMIC = "DYNAMIC"
    CHARGED = "CHARGED"
    PERFORMANCE = "PERFORMANCE"
    DEFAULT = "DEFAULT"
    FEED = "FEED"
    CUSTOM = "CUSTOM"
    SELF_USE = "SELF_USE"


@dataclass
class CurrentPower(DataClassORJSONMixin):
    """Current power model.

    All telemetry fields are optional because the API omits them when the
    battery is offline (then only ``onlineStatus`` is returned).
    """

    online_status: OnlineStatus = field(metadata=field_options(alias="onlineStatus"))
    state_of_charge: float | None = field(
        metadata=field_options(alias="soc"), default=None
    )
    output_current: float | None = field(
        metadata=field_options(alias="coc"), default=None
    )
    max_power: int | None = field(metadata=field_options(alias="smp"), default=None)
    on_grid: bool | None = field(metadata=field_options(alias="onGrid"), default=None)
    photovoltaic_power: int | None = field(
        metadata=field_options(alias="ppv"), default=None
    )
    power_socket_output: int | None = field(
        metadata=field_options(alias="pso"), default=None
    )
    is_dormant: bool | None = field(
        metadata=field_options(alias="isDormancy"), default=None
    )


@dataclass
class BatteryState(DataClassORJSONMixin):
    """Battery state."""

    serial_number: str = field(metadata=field_options(alias="sn"))
    name: str
    online_status: OnlineStatus = field(metadata=field_options(alias="onlineStatus"))
    current_power: CurrentPower = field(metadata=field_options(alias="currentPower"))
    smart_mode: SmartMode = field(metadata=field_options(alias="smartMode"))
    global_settings: GlobalSettings = field(
        metadata=field_options(alias="globalSettings")
    )


@dataclass
class OnlineStatusResponse(DataClassORJSONMixin):
    """Online state."""

    serial_number: str = field(metadata=field_options(alias="sn"))
    online_status: OnlineStatus = field(metadata=field_options(alias="onlineStatus"))


@dataclass
class PhotovoltaicData(DataClassORJSONMixin):
    """Photovoltaic data."""

    name: str
    power: int


@dataclass
class GlobalSettings(DataClassORJSONMixin):
    """Global settings."""

    max_output: int = field(metadata=field_options(alias="maxOutput"))
    max_output_limit: int = field(metadata=field_options(alias="maxOutputLimit"))
    max_output_unlocked: bool = field(metadata=field_options(alias="maxOutputUnlocked"))
    battery_upper_threshold: int = field(metadata=field_options(alias="batHighCap"))
    battery_lower_threshold: int = field(metadata=field_options(alias="batUseCap"))
    maximum_charge_power: int = field(metadata=field_options(alias="maxChargePower"))
    standby_time: int = field(metadata=field_options(alias="standbyTime"))


class UnitType(StrEnum):
    """Unit type."""

    INVERTER = "INVERTER"
    EMS = "EMS"
    BATTERY = "BATTERY"


class UnitUpdateStatus(StrEnum):
    """Unit update status."""

    NO_UPDATE = "NO_UPDATE"
    UPDATE_AVAILABLE = "UPDATE_AVAILABLE"
    DISCOVER_UPDATED = "DISCOVER_UPDATED"


@dataclass
class UnitVersion(DataClassORJSONMixin):
    """Unit version information."""

    current_version: str = field(metadata=field_options(alias="currentVersion"))
    status: UnitUpdateStatus
    latest_version: str | None = field(
        metadata=field_options(alias="latestVersion"), default=None
    )


@dataclass
class Unit(DataClassORJSONMixin):
    """Unit model."""

    serial_number: str = field(metadata=field_options(alias="usn"))
    name: str
    type: UnitType
    abnormal_amount: int = field(metadata=field_options(alias="abnormalAmount"))
    resettable: bool
    version: UnitVersion


@dataclass
class UnitsResponse(DataClassORJSONMixin):
    """Units list response."""

    units: list[Unit]


@dataclass
class BatteryUnit(DataClassORJSONMixin):
    """Battery unit."""

    serial_number: str = field(metadata=field_options(alias="usn"))
    version: Version
    points: list[Checkpoint]
    battery_model: str = field(metadata=field_options(alias="batteryModel"))
    power: int


@dataclass
class Version(DataClassORJSONMixin):
    """Version information."""

    current_version: str = field(metadata=field_options(alias="currentVersion"))
    latest_version: str | None = field(
        metadata=field_options(alias="latestVersion"), default=None
    )


@dataclass
class Checkpoint(DataClassORJSONMixin):
    """Checkpoint information."""

    point: str
    normal: bool
