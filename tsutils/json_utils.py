import json
import logging
import os
import time

import aiohttp
import backoff

logger = logging.getLogger('tsutils')


def should_download(file_path, expiry_secs):
    if not os.path.exists(file_path):
        logger.debug("file does not exist, downloading " + file_path)
        return True

    ftime = os.path.getmtime(file_path)
    file_age = time.time() - ftime

    if file_age > expiry_secs:
        logger.debug("file {} too old, download it".format(file_path))
        return True
    else:
        return False


def writeJsonFile(file_path, js_data):
    with open(file_path, "w") as f:
        json.dump(js_data, f, indent=4)


def readJsonFile(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def safe_read_json(file_path):
    try:
        return readJsonFile(file_path)
    except Exception as ex:
        logger.error('failed to read {} got exception'.format(file_path), exc_info=True)
    return {}


def validate_json(fp):
    try:
        json.load(open(fp))
        return True
    except:
        return False


@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=60)
@backoff.on_exception(backoff.expo, aiohttp.ServerDisconnectedError, max_time=60)
async def async_cached_dadguide_request(file_path, file_url, expiry_secs):
    if should_download(file_path, expiry_secs):
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                assert resp.status == 200
                with open(file_path, 'wb') as f:
                    f.write(await resp.read())


def writePlainFile(file_path, text_data):
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(text_data)


def readPlainFile(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        return f.read()


async def makeAsyncPlainRequest(file_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            return await resp.text()


async def makeAsyncCachedPlainRequest(file_path, file_url, expiry_secs):
    if should_download(file_path, expiry_secs):
        resp = await makeAsyncPlainRequest(file_url)
        writePlainFile(file_path, resp)
    return readPlainFile(file_path)
