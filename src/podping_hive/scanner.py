import asyncio
import enum
import inspect
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from functools import wraps
from timeit import default_timer as timer
from typing import Any, List, Literal, Optional

import backoff
from lighthive.client import Client
from lighthive.datastructures import Operation
from lighthive.exceptions import RPCNodeException
from lighthive.helpers.account import VOTING_MANA_REGENERATION_IN_SECONDS
from lighthive.node_picker import compare_nodes
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pydantic import BaseModel, Field, validator
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError

from podping_hive.database import block_at_postion
from podping_hive.hive_calls import keep_checking_hive_stream
from podping_hive.podping import Podping


async def main_loop():
    # start_block = await block_at_postion(-1)
    time_delta = timedelta(hours=1)
    await keep_checking_hive_stream(time_delta=time_delta)
    # await keep_checking_hive_stream(start_block=start_block)


if __name__ == "__main__":
    debug = False
    logging.basicConfig(
        level=logging.INFO if not debug else logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(module)-14s %(lineno) 5d : %(message)s",
        datefmt="%m-%dT%H:%M:%S",
    )
    # client = get_client()
    # logging.info(client.current_node)
    try:
        asyncio.run(main_loop())

    except asyncio.CancelledError as ex:
        logging.warning("asyncio.CancelledError raised")
        logging.warning(ex)
        raise
    except KeyboardInterrupt:
        logging.info("Interrupted with ctrc-C")
