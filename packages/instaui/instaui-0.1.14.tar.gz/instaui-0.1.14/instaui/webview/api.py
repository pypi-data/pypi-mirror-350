from typing import Any, Dict


from instaui.runtime._app import get_app_slot
from instaui.handlers import watch_handler
from instaui.handlers import event_handler
from instaui.skip import is_skip_output


class Api:
    def watch_call(self, data: Dict):
        hkey = data.pop("key")
        handler_info = watch_handler.get_handler_info(hkey)
        if handler_info is None:
            return {"error": "watch handler not found"}

        update_app_page_info(data)

        result = handler_info.fn(
            *handler_info.get_handler_args(_get_binds_from_data(data))
        )
        return response_data(handler_info.outputs_binding_count, result)

    def event_call(self, data: Dict):
        handler = event_handler.get_handler(data["hKey"])
        if handler is None:
            raise ValueError("event handler not found")

        update_app_page_info(data)


        args = [bind for bind in data.get("bind", [])]

        result = handler.fn(*handler.get_handler_args(args))
        return response_data(handler.outputs_binding_count, result)


def update_app_page_info(data: Dict):
    app = get_app_slot()

    page_info = data.get("page", {})
    app._page_path = page_info["path"]

    if "params" in page_info:
        app._page_params = page_info["params"]

    if "queryParams" in page_info:
        app._query_params = page_info["queryParams"]


def _get_binds_from_data(data: Dict):
    return data.get("input", [])


def response_data(outputs_binding_count: int, result: Any):
    data = {}
    if outputs_binding_count > 0:
        if not isinstance(result, tuple):
            result = [result]

        result_infos = [(r, int(is_skip_output(r))) for r in result]

        if len(result_infos) == 1 and result_infos[0][1] == 1:
            return data

        data["values"] = [0 if info[1] == 1 else info[0] for info in result_infos]
        skips = [info[1] for info in result_infos]

        if sum(skips) > 0:
            data["skips"] = skips

    return data
