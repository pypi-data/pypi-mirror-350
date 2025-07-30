import asyncio
import logging

from aiohttp import ClientSession, ClientResponse
from aiohttp.http_exceptions import HttpProcessingError

from x_client import HttpNotFound, df_hdrs


class Client:
    host: str | None  # required
    headers: dict[str, str] = df_hdrs
    cookies: dict[str, str] = None
    proxy: str = None
    session: ClientSession

    def __init__(
        self, host: str = None, headers: dict[str, str] = None, cookies: dict[str, str] = None, proxy: str = None
    ):
        base_url = f"https://{h}" if (h := host or self.host) else h
        hdrs, cooks = {**self.headers, **(headers or {})}, {**(self.cookies or {}), **(cookies or {})}
        self.session = ClientSession(base_url, headers=hdrs, cookies=cooks, proxy=proxy)

    async def close(self):
        await self.session.close()

    # noinspection PyMethodMayBeStatic
    def _prehook(self, _payload: dict = None):
        return {}

    async def _get(self, url: str, params: dict = None, data_key: str = None):
        asyncio.get_running_loop()
        resp = await self.session.get(url, params=params, headers=self._prehook(params))
        return await self._proc(resp, data_key=data_key)

    async def _post(self, url: str, json: dict = None, data: dict = None, data_key: str = None):
        resp = await self.session.post(url, json=json, data=data, headers=self._prehook(data))
        return await self._proc(resp, data_key=data_key)

    async def _delete(self, url: str, params: dict = None):
        resp: ClientResponse = await self.session.delete(url, params=params, headers=self._prehook(params))
        return await self._proc(resp)

    async def _proc(self, resp: ClientResponse, data_key: str = None) -> dict | str:
        if not str(resp.status).startswith("2"):
            logging.error(f"response {resp.status}: {await resp.text()}")
            if resp.status == 404:
                raise HttpNotFound()
            raise HttpProcessingError(code=resp.status, message=await resp.text())
        if resp.content_type.endswith("/json"):
            if not (data := await resp.json()):
                logging.warning("empty response: " + await resp.text())
            if data_key:
                if res := data.get(data_key):
                    return res
                logging.warning("empty response: " + await resp.text())
                raise HttpProcessingError()
            return data
        return await resp.text()

    METHS = {
        "GET": _get,
        "POST": _post,
        "DELETE": _delete,
    }
