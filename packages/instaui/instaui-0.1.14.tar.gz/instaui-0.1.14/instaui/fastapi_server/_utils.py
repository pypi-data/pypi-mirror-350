from typing import Any, Dict, List, Optional
from instaui.runtime._app import get_app_slot
from instaui.skip import is_skip_output
import pydantic


class ResponseData(pydantic.BaseModel):
    values: Optional[List[Any]] = None
    skips: Optional[List[int]] = None


def update_app_page_info(data: Dict):
    app = get_app_slot()

    page_info = data.get("page", {})
    app._page_path = page_info["path"]

    if "params" in page_info:
        app._page_params = page_info["params"]

    if "queryParams" in page_info:
        app._query_params = page_info["queryParams"]


def response_data(outputs_binding_count: int, result: Any):
    data = ResponseData()
    if outputs_binding_count > 0:
        if not isinstance(result, tuple):
            result = [result]

        result_infos = [(r, int(is_skip_output(r))) for r in result]

        if len(result_infos) == 1 and result_infos[0][1] == 1:
            return data

        data.values = [0 if info[1] == 1 else info[0] for info in result_infos]
        skips = [info[1] for info in result_infos]

        if sum(skips) > 0:
            data.skips = skips

    return data
