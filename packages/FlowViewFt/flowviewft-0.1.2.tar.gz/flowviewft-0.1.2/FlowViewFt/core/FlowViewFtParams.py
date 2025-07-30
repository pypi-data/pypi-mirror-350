from typing import Optional

class FlowViewFtParams:
    def __init__(self, params: Optional[dict] = None):
        self._params = params or {}

    def get(self, key: str):
        return self._params.get(key)

    def get_all(self) -> dict:
        return self._params

    def __getitem__(self, key: str):
        return self._params.get(key)

    def __setitem__(self, key: str, value):
        self._params[key] = value

    def __contains__(self, key: str):
        return key in self._params
