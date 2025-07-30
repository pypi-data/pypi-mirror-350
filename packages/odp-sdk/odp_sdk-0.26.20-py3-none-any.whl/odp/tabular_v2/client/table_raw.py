import io
from typing import TYPE_CHECKING, Iterator, Optional, Union

if TYPE_CHECKING:
    from odp.tabular_v2.client import Table


class Raw:
    def __init__(self, table: "Table"):
        self.table = table

    def list(self, query: Optional[str] = None, vars: Optional[dict] = None) -> list:
        res = self.table._client._request(
            "/api/table/v2/raw/list",
            params={"table_id": self.table._id, "query": query, "vars": vars},
            data={},
        )
        body = res.json()
        return body["files"]

    def upload(self, name: str, data: Union[bytes, io.IOBase]) -> str:
        res = self.table._client._request(
            "/api/table/v2/raw/upload",
            params={"table_id": self.table._id, "name": name},
            data=data,
        )
        body = res.json()
        return body["raw_id"]

    def update_meta(self, raw_id: str, data: Union[bytes, io.IOBase]) -> dict:
        res = self.table._client._request(
            "/api/table/v2/raw/update_meta",
            params={"table_id": self.table._id, "raw_id": raw_id},
            data=data,
        )
        return res.json()

    def download(self, raw_id: str) -> Iterator[bytes]:
        res = self.table._client._request(
            "/api/table/v2/raw/download",
            params={"table_id": self.table._id, "raw_id": raw_id},
        )
        return res.iter()

    def ingest(self, raw_id: str) -> dict:
        res = self.table._client._request(
            "/api/table/v2/raw/ingest",
            params={"table_id": self.table._id, "raw_id": raw_id},
            data={},
        )
        body = res.json()
        return body
