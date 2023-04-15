import os
import json

from web3 import Web3
from reau_abi import REAU_ABI
from datetime import datetime

RPC_URL = 'https://bsc-dataseed1.binance.org:443'
REAU_CONTRACT = Web3.to_checksum_address('0x4c79b8c9cb0bd62b047880603a9decf36de28344')
DEAD_WALLET = Web3.to_checksum_address('0x000000000000000000000000000000000000dead')

w3 = Web3(Web3.HTTPProvider(RPC_URL))
reau = w3.eth.contract(address=REAU_CONTRACT, abi=REAU_ABI)
decimals = reau.caller.decimals()
total_supply = reau.caller.totalSupply()
total_burnt = reau.caller.balanceOf(DEAD_WALLET)

circulating_supply = total_supply - total_burnt

out_json = {
    'last_updated': 0,
    'results': []
}

if os.path.exists('blackhole.json'):
    with open('blackhole.json', 'r') as file:
        try:
            out_json = json.loads(file.read())
        except:
            print('Failed to open file, creating a new one')

timestamp = int(datetime.utcnow().timestamp())

out_json['last_updated'] = timestamp
out_json['decimals'] = decimals
out_json['results'].append({
    'total_burnt': total_burnt,
    'circulating_supply': circulating_supply,
    'time': timestamp
})

with open('blackhole.json', 'w') as file:
    json.dump(out_json, file, indent=2)

