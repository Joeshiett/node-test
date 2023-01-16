import pytest 
import time
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
        else:
            pytest.fail(f'Websocket Connection not established!')

    except WebSocketBadStatusException as bad_status:
        pytest.fail(f'failed due to {bad_status}')
    except ConnectionRefusedError as conn_refused:
        pytest.fail(f'failed due to {conn_refused}')

# Test JSON RPC connectivity
def test_json_rpc():
    url = 'http://127.0.0.1:9933'
    payload = {"jsonrpc":"2.0","method":"system_name","params":[],"id":1}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    
# Test Block Production
def test_block_production():
    try:
        ws_provider = SubstrateInterface(
            url="ws://127.0.0.1:9944",
        )
        
        # List to store Block numbers
        block_num = []           
        def subscription_handler(obj, update_nr, subscription_id):
            block_num.append(obj['header']['number'])
            if update_nr > 5:
                return block_num 

        result = ws_provider.subscribe_block_headers(subscription_handler)
        res = all(i < j for i, j in zip(result, result[1:]))
        if res is True:
            assert True 
        else:
            pytest.fail('Blocks not being produced')

    except WebSocketBadStatusException as bad_status:
        pytest.fail(f'failed due to {bad_status}')
    except ConnectionRefusedError as conn_refused:
        pytest.fail(f'failed due to {conn_refused}')
