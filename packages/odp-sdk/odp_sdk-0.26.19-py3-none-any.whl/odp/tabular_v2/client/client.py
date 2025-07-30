import io
import logging
from typing import TYPE_CHECKING, Dict, Iterator, Optional, Union

import requests
from requests.adapters import HTTPAdapter

from odp.tabular_v2.util import Iter2Reader
from odp.util.util import size2human

if TYPE_CHECKING:
    from odp.tabular_v2.client.table import Table


class Client:
    def __init__(self, base_url: str):
        self._base_url = base_url

    class Response:
        # Abstraction for response object, shared between http client and test client
        def __init__(self, res: Union[requests.Response, Iterator[bytes], Dict, bytes]):
            if isinstance(res, requests.Response):
                if res.status_code == 204:
                    raise FileNotFoundError(res.text)
                res.raise_for_status()
            # logging.info("response: %s", res)
            self.res = res

        def reader(self):
            if isinstance(self.res, bytes):
                return io.BytesIO(self.res)
            if isinstance(self.res, Iterator):
                return Iter2Reader(self.res)
            return self.res.raw

        def iter(self) -> Iterator[bytes]:
            if isinstance(self.res, bytes):
                return iter([self.res])
            if isinstance(self.res, Iterator):
                return self.res
            return self.res.iter_content()

        def all(self) -> bytes:
            if isinstance(self.res, bytes):
                return self.res
            if isinstance(self.res, Iterator):
                return b"".join(self.res)
            return self.res.content

        def json(self) -> dict:
            if self.res is None:
                return None
            if isinstance(self.res, dict):
                return self.res
            return self.res.json()

    def _request(
        self,
        path: str,
        data: Union[Dict, bytes, Iterator[bytes], io.IOBase, None] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Response:
        with requests.Session() as s:
            adapter = HTTPAdapter(pool_connections=4, pool_maxsize=4, max_retries=8)
            s.mount("http://", adapter)
            s.mount("https://", adapter)
            if isinstance(data, dict):
                logging.info("sending %s %s %s", path, params, data)
                res = s.post(self._base_url + path, headers=headers, params=params, json=data, stream=True)
            elif isinstance(data, bytes):
                logging.info("sending %s %s (%s)", path, params, size2human(len(data)) if data else "-")
                res = s.post(self._base_url + path, headers=headers, params=params, data=data, stream=True)
            elif isinstance(data, io.IOBase):
                logging.info("sending file-like %s %s", path, params)
                res = s.post(self._base_url + path, headers=headers, params=params, data=data, stream=True)
            elif isinstance(data, Iterator):
                logging.info("sending %s %s iterator...", path, params)
                res = s.post(self._base_url + path, headers=headers, params=params, data=data, stream=True)
            elif data is None:
                logging.info("sending %s %s no data", path, params)
                res = s.post(self._base_url + path, headers=headers, params=params, stream=True)
            else:
                raise ValueError(f"unexpected type {type(data)}")
        logging.info("got response %s", res.status_code)
        return self.Response(res)

    def table(self, table_id: str) -> "Table":
        """
        create a table handler for the given table_id
        @param table_id:
        @return:
        """
        from odp.tabular_v2.client import Table

        return Table(self, table_id)
