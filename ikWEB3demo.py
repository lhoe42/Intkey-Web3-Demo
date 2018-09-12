import sys
import web3

from web3 import Web3
from solc import compile_source

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def get(key):
    value  = intkey.functions.get(key).call()
    return value

def gasCost(keyhash):
    return w3.eth.getTransactionReceipt(keyhash)['gasUsed']

def print_action(tx_hash,key,transaction_type):
    print(key,' was',transaction_type,'and has a new value of {}\n'.format(get(key)))
    print('This transaction cost',gasCost(tx_hash),'gas.\n')

def dec(key):
    tx_hash = intkey.functions.dec(key).transact()
    print_action(tx_hash,key,'decremented')

def inc(key):
    tx_hash = intkey.functions.inc(key).transact()
    print_action(tx_hash,key,'incremented')

def set_intkey(key,value):
    tx_hash = intkey.functions.set(key,value).transact()
    print_action(tx_hash,key,'set')


def deploy_contract(w3, contract_interface):
    # deploys a contract and returns contract address
    tx_hash = w3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin']).deploy()
    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address

print()
print('Intkey Contract Demo')
print()
print()

# localhost: ganache client and specify intkey contract
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.HTTPProvider("https://api-dev.veriteos.com/v1/rpc", request_kwargs={'auth': ('veriteos_demo_key_0','')}))
compiled_sol = compile_source_file('intkey.sol')

# Use the first test account 
w3.eth.defaultAccount = w3.eth.accounts[0]

#separate KV pair of id and interface
contract_id, contract_interface = compiled_sol.popitem()

# deploy contract to w3 
# contract_address = deploy_contract(w3, contract_interface
contract_address = w3.toChecksumAddress("0x8558eb5eeb9ea968cf6e8e6f264d488c202b5c94")
print("Deployed contract {0} to address: {1}\n".format(contract_id, contract_address))

# instantiate the deployed contract
intkey = w3.eth.contract(address=contract_address, abi= contract_interface['abi'],)

key = 1

while key != 42: #enter 42 to exit
    k = input('Which key should I modify?')
    key = int(k)
    action = input('Should I set, dec or inc it? (s,d or i):')
    if str(action) == 'd':
        dec(key)
    elif str(action) == 'i':
        inc(key)
    elif str(action) == 's':
        value = input('what should i set it to?')
        set_intkey(key,int(value))
    
    
