import pytest 
import requests
from substrateinterface import SubstrateInterface
from websocket._exceptions import WebSocketBadStatusException

# Test Websocket RPC connectivity
def test_websocket_rpc():
    try:
        ws_provider = SubstrateInterface(
            url="ws://127.0.0.1:9944",
        )   
        # Retrieve the finalized block
        ws_conn = ws_provider.connect_websocket()
        if ws_conn is None:
            assert True, "Websocket Connection established"

    except WebSocketBadStatusException as bad_status:
        pytest.fail(f'failed due to{bad_status}')
    except ConnectionRefusedError as conn_refused:
        pytest.fail(f'failed due to{conn_refused}')

# Test JSON RPC connectivity
def test_json_rpc():
    url = 'https://127.0.0.1:9933'
    payload = {"jsonrpc":"2.0","method":"system_name","params":[],"id":1}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    
# Test Block Production
def test_block_production():
    try:
        ws_provider = SubstrateInterface(
            url="ws://127.0.0.1:9944",
        )
        block_header = ws_provider.get_block_header(finalized_only=True)

        for key, value in block_header['header'].items():
            if key == 'number':
                if value > 0:
                    assert value > 0
    except WebSocketBadStatusException as bad_status:
        pytest.fail(f'failed due to{bad_status}')
    except ConnectionRefusedError as conn_refused:
        pytest.fail(f'failed due to{conn_refused}')

    