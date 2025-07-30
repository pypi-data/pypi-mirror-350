import json
import time

import websocket

def on_message(ws, message):
    print(f"Received message: {message}")
    msg = json.loads(message)
    print(f"Received message: {msg}")
    # {
    #     "sender": "",
    #     "receiver": "",
    #     "type": "tool_call",
    #     "tool_call": {
    #         "name": "add",
    #         "args": {
    #             "x": 1.0,
    #             "y": 2.0,
    #             "complex": {
    #                 "x": 1.0,
    #                 "y": 2.0
    #             }
    #         },
    #         "id": "call_a7fb9c9c1d134550a8348f"
    #     },
    #     "direction": "bi-directional"
    # }
    if msg['type'] == 'tool_call':
        tool_call = msg['tool_call']
        if tool_call['name'] == 'add':
            args = tool_call['args']
            res = int(args['x']) + int(args['y'])
#            time.sleep(5)

            if msg["direction"] == "bi-directional":
                ws.send(json.dumps({
                    'type': 'tool_call_response',
                    'response': {
                        'type': 'tool',
                        'artifact': f'x + y = {res}',
                        'content': res,
                        'status': 'success',
                        'tool_call_id': tool_call['id']
                    },
                    'receiver': tool_call['id']
                }))
        elif tool_call['name'] == 'print':
            print(tool_call['args']['message'])


def on_error(ws, error):
    print(f"Error occurred: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Closed ###")

def on_open(ws):
    print("Opened connection")
    print('======do register======')
    print(ws)
    ws.send(json.dumps({
        "type": "tool_register",
        "toolkit_name": "calculator",
        "toolkit_description": "calculator",
        "tools": [
            {
                "name": "add",
                "description": "add two numbers and return sum",
                "args_schema": {
                    "x": {
                        "type": "float",
                        "required": False,
                        "description": "one number",
                    },
                    "y": {
                        "type": "float",
                        "required": False,
                        "description": "one number",
                    },
                    "complex": {
                        "x": {
                            "type": "float",
                            "required": False,
                            "description": "one number",
                        },
                        "y": {
                            "type": "float",
                            "required": False,
                            "description": "one number",
                        },
                    }
                },
                "direction": "bi-directional"
            },
            {
                "name": "print",
                "description": "print",
                "args_schema": {
                    "message": {
                        "type": "string",
                        "required": False,
                        "description": "echo message",
                    }
                },
                "direction": "one-way"
            }
        ]
    }))

    # time.sleep(5)
    # ws.send(json.dumps({
    #     "type": "tool_unregister",
    #     "toolkit_name": "calculator",
    # }))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8888/websocket",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
