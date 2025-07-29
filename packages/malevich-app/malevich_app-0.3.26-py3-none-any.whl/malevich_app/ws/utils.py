import json
from typing import Callable
from pydantic import BaseModel
from malevich_app.export.abstract.abstract import WSMessage


async def ws_call(ws, f: Callable, msg: WSMessage):
    try:
        res, response = await f(msg.payload)
    except BaseException as ex:
        res_msg = WSMessage(
            operationId=msg.operationId,
            error=str(ex),
            operation=msg.operation,
            id=msg.id,
        )
    else:
        if response is None:
            ok = True   # only ping
        else:
            ok = response.status_code < 300

        if msg.operation == "stream":
            if ok:
                async for chunk in res.body_iterator:
                    intermediate_msg = WSMessage(
                        operationId=msg.operationId,
                        payload=chunk,
                        operation=msg.operation,
                        id=msg.id,
                    )
                    await ws.send(intermediate_msg.model_dump_json())
            payload = None
        else:
            payload = res
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            elif isinstance(payload, BaseModel):
                payload = payload.model_dump_json()

        res_msg = WSMessage(
            operationId=msg.operationId,
            payload=payload,
            error=None if ok else f"response code={response.status_code}",
            operation=msg.operation,
            id=msg.id,
        )
    await ws.send(res_msg.model_dump_json())
