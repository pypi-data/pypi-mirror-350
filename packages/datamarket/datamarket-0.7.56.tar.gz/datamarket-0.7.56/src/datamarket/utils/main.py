########################################################################################################################
# IMPORTS

import asyncio
import configparser
import logging
import random
import re
import shlex
import subprocess
import time

import pendulum

########################################################################################################################
# FUNCTIONS

logger = logging.getLogger(__name__)


def get_config(config_path):
    cfg = configparser.RawConfigParser()
    cfg.read(config_path)
    return cfg


def set_logger(level):
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(level.upper())
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    log.addHandler(ch)


def ban_sleep(max_time, min_time=0):
    sleep_time = int(random.uniform(min_time, max_time))
    logger.info(f"sleeping for {sleep_time} seconds...")
    time.sleep(sleep_time)


async def ban_sleep_async(max_time, min_time=0):
    sleep_time = int(random.uniform(min_time, max_time))  # noqa: S311
    logger.info(f"sleeping for {sleep_time} seconds...")
    await asyncio.sleep(sleep_time)


def run_bash_command(command):
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    text_lines = []
    for line_b in iter(p.stdout.readline, ""):
        line_str = line_b.decode().strip()

        if not line_str:
            break

        logger.info(line_str)
        text_lines.append(line_str)

    return "\n".join(text_lines)


def text_to_int(text):
    max_int32 = 2147483647
    parsed_str = re.sub(r"[^\d]", "", text)
    if parsed_str:
        num = int(parsed_str)
    else:
        return None

    if -max_int32 < num < max_int32:
        return num


def sleep_out_interval(from_h, to_h, tz="Europe/Madrid", seconds=1800):
    while pendulum.now(tz=tz).hour >= to_h or pendulum.now(tz=tz).hour < from_h:
        logger.warning("time to sleep and not scrape anything...")
        ban_sleep(seconds, seconds)


def sleep_in_interval(from_h, to_h, tz="Europe/Madrid", seconds=1800):
    while from_h <= pendulum.now(tz=tz).hour < to_h:
        logger.warning("time to sleep and not scrape anything...")
        ban_sleep(seconds, seconds)


def parse_field(dict_struct, field_path, format_method=None):
    if not isinstance(field_path, list):
        raise ValueError("Argument field_path must be of type list")

    field_value = dict_struct
    for field in field_path:
        if isinstance(field_value, dict):
            field_value = field_value.get(field)
        elif isinstance(field_value, list):
            field_value = field_value[field] if len(field_value) > field else None
        if field_value is None:
            return None
    return format_method(field_value) if format_method else field_value
