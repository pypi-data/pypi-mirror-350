from agentic_kit_eda.infrastructure.rpc.fastapi.ws_connection_manager import WsConnectionManager
from agentic_kit_eda.infrastructure.event_driven.ws.ws_message_handler_manager import WsMessageHandlerManager


def create_ws_server(
    connection_manager: WsConnectionManager,
    ws_message_handler_manager: WsMessageHandlerManager,
    ws_path: str = '/websocket',
    title: str = 'Server',
    version: str = '1.0.0'
):
    assert connection_manager is not None
    assert ws_message_handler_manager is not None

    from fastapi import FastAPI
    from starlette.middleware.cors import CORSMiddleware
    from starlette.websockets import WebSocket, WebSocketDisconnect

    app = FastAPI(title=title, version=version)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.websocket(ws_path)
    async def websocket_endpoint(websocket: WebSocket):
        await connection_manager.connect(websocket)
        try:
            while True:
                message = await websocket.receive_json()
                await ws_message_handler_manager.handle_message(websocket=websocket, message=message)
                # await manager.broadcast(f"Client says: {data}")
        except WebSocketDisconnect:
            connection_manager.disconnect(websocket)

    return app
