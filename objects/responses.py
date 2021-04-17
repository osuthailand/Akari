from starlette.responses import JSONResponse
from typing import Any
import orjson

class ajson(JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)