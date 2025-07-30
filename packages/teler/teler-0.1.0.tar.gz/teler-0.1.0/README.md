# Teler 

This library offers a lightweight and developer-friendly abstraction over the FreJun Teler API.

## Media Streaming

With the launch of the first minor version, the library introduces an intuitive interface for integrating real-time call audio streams from Teler into your application, unlocking advanced capabilities such as Conversational AI, Real-time transcription, and Actionable insights.

### `StreamConnector`

This class lets you bridge the call audio stream to an endpoint of your choice. It handles the message relaying between the 2 streams via pluggable handlers, making it highly customizable.
It also handles graceful shutdown of the media streams in case of any unexpected errors.

It takes the following 4 parameters:

1. **stream_type** - Only `StreamType.BIDIRECTIONAL` is supported for now.
2. **remote_url** - The remote websocket URL where the call audio stream needs to be bridged.
3. **call_stream_handler** - A `StreamHandler` coroutine that handles the call audio stream.
4. **remote_stream_handler** - A `StreamHandler` coroutine that handles the remote audio stream.

### `StreamHandler`

A `StreamHandler` coroutine receives the incoming messages on the websocket, processes them and returns a tuple of `(str, StreamOp)`. `StreamOp` is an operation flag that decides the subsequent action the `StreamConnector` will take.

`StreamOp` can be one of:

1. **StreamOp.RELAY** - Relays the message to the other stream. The message needs to be supplied as a string as the first item in the returned tuple.
2. **StreamOp.PASS** - Does not relay any message to the other stream. Any message in the returned tuple will be ignored.
3. **StreamOp.STOP** - Stops both streams, ends the call and exits gracefully. Any message in the returned tuple will be ignored.   

### Sample Usage - FastAPI Echo Server

The following setup bridges the call audio stream to a dummy endpoint that echoes back all incoming messages. As a result, the caller will hear their own voice played back in real time, effectively creating an audio loopback.


```python
import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from teler.streams import StreamConnector, StreamOp, StreamType


router = APIRouter()

logger = logging.getLogger(__name__)

TEST_WEBSOCKET_URL = "wss://{SERVER_DOMAIN}/test-remote-ws"


async def call_stream_handler(message: str):
    msg = json.loads(message)
    if msg["type"] == "audio":
        payload = json.dumps(
            {
                "type": "audio",
                "audio_b64": msg["data"]["audio_b64"],
                "chunk_id": msg["message_id"],
            }
        )
        return (payload, StreamOp.RELAY)
    return ({}, StreamOp.PASS)

async def remote_stream_handler(message: str):
    msg = json.loads(message)
    if msg["type"] == "audio":
        payload = json.dumps(
            {
                "type": "audio",
                "audio_b64": msg["audio_b64"],
                "chunk_id": msg["chunk_id"],
            }
        )
        return (payload, StreamOp.RELAY)
    return ({}, StreamOp.PASS)
    

connector = StreamConnector(
    stream_type=StreamType.BIDIRECTIONAL,
    remote_url=TEST_WEBSOCKET_URL,
    call_stream_handler=call_stream_handler,
    remote_stream_handler=remote_stream_handler,
)


@router.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connected.")
    await connector.bridge_stream(websocket)


@router.websocket("/test-remote-ws")
async def test_remote_ws(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connected.")
    try:
        async for data in websocket.iter_text():
            await websocket.send_text(data)
    except WebSocketDisconnect:
        print("Client disconnected")
```