import os

from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter


async def connect_temporal() -> Client:
    """Connect to Temporal the way this app requires — every client must use
    the same data converter, or API and workers disagree on payload
    serialization. Always connect through here, never Client.connect directly.
    """
    address = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
    return await Client.connect(address, data_converter=pydantic_data_converter)
