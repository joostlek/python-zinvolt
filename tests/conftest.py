"""Asynchronous Python client for Zinvolt."""

from collections.abc import AsyncGenerator, Generator

import aiohttp
from aioresponses import aioresponses
import pytest

from syrupy import SnapshotAssertion
from zinvolt import ZinvoltClient

from .syrupy import ZinvoltSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the Zinvolt extension."""
    return snapshot.use_extension(ZinvoltSnapshotExtension)


@pytest.fixture
async def client() -> AsyncGenerator[ZinvoltClient]:
    """Return a Zinvolt client."""
    async with (
        aiohttp.ClientSession() as session,
        ZinvoltClient("token", session=session) as zinvolt_client,
    ):
        yield zinvolt_client


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
