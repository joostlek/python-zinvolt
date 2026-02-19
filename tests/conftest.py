"""Asynchronous Python client for Zinvolt."""

from collections.abc import AsyncGenerator, Generator
from unittest.mock import patch

import aiohttp
from aioresponses import aioresponses
import pytest

from zinvolt import ZinvoltClient
from syrupy import SnapshotAssertion

from .syrupy import ZinvoltSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the Zinvolt extension."""
    return snapshot.use_extension(ZinvoltSnapshotExtension)


@pytest.fixture
async def client() -> AsyncGenerator[ZinvoltClient, None]:
    """Return a Zinvolt client."""
    async with (
        aiohttp.ClientSession() as session,
        ZinvoltClient("token", session=session) as zinvolt_client,
    ):
        yield zinvolt_client


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses

