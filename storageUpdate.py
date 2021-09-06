from web3 import Web3
import sys
#import socket
import random
#import rlp
import time
#import numpy as np
import os, binascii
from datetime import datetime
from multiprocessing import Pool
from flask import Flask, request, jsonify
from flask_cors import CORS
import json


# Settings
FULL_PORT = "8081"
PASSWORD = "1234"

# Account number
ACCOUNT_NUM = int(sys.argv[1])
TX_PER_BLOCK = 1 # 200

# multiprocessing
THREAD_COUNT = 1

# tx arguments option
INCREMENTAL_RECEIVER_ADDRESS = True # set tx receiver: incremental vs random
INCREMENTAL_SEND_AMOUNT = True      # set send amount: incremental vs same (1 wei)
MAX_ADDRESS = 0                     # set max address to set the receiver address upper bound (0 means there is no bound)

# providers
fullnode = Web3(Web3.HTTPProvider("http://localhost:" + FULL_PORT))

# Ethereum coinbase account
PASSWORD = "1234"
fullnode.geth.personal.unlockAccount(fullnode.eth.coinbase, PASSWORD, 0)
fullnode.eth.defaultAccount = fullnode.eth.coinbase

# simpleStorage.sol smart contract
# put employ code to geth console & start mining => then we will get contract address
CONTRACTADDR = Web3.toChecksumAddress("0x17c33F7747098BF36c950cdd4B0681231B38E581")
CONTRACT = fullnode.eth.contract(address=CONTRACTADDR)

# gas amount for transaction (should be large enough)
GAS = 1000000





# dictionaries
setter = dict()
getter = dict()





def makeRandHex():
	randHex = binascii.b2a_hex(os.urandom(20))
	return Web3.toChecksumAddress("0x" + randHex.decode('utf-8'))

def intToAddr(num):
    intToHex = f'{num:0>40x}'
    return Web3.toChecksumAddress("0x" + intToHex)

# (joonha)
def getStorageAt(address, position):
    # Get the storage at a specific position of an address.
    # https://web3js.readthedocs.io/en/v1.2.11/web3-eth.html#getstorageat
    return fullnode.eth.getStorageAt(address, position, "latest")

# (joonha)
def sendContractTransaction(transactionObject):
    # Sends a transaction to the network.
    # https://web3js.readthedocs.io/en/v1.2.11/web3-eth.html#sendtransaction
    try:
        fullnode.eth.sendTransaction(transactionObject)
        print("[SUCCESS] Sending Contract Transaction succeeded.")
        return 1
    except:
        print("[FAIL] Sending Contract Transaction failed.")
        return 0

# (joonha)
def getBlockTransactionHash(blockHashOrBlockNumber):
    # Returns a block matching the block number or block hash.
    # https://web3js.readthedocs.io/en/v1.2.11/web3-eth.html#getblock
    return fullnode.eth.getBlock(blockHashOrBlockNumber).transactions # multiple Txs -> Array

# (joonha)
def contractAddress(transactionHash):
    # Returns the receipt of a transaction by transaction hash.
    # The contract address created, if the transaction was a contract creation, otherwise null.
    # https://web3js.readthedocs.io/en/v1.2.11/web3-eth.html#gettransactionreceipt
    return fullnode.eth.getTransactionReceipt(transactionHash).contractAddress






if __name__ == "__main__":

    try:
        fullnode.geth.miner.start(1)

        print("flag 1")
        tx_hash = CONTRACT.functions.setter(1, 10).transact({'gas':GAS}) # error
        print("flag 2")
        print("Storage Map:\t\t\t" + str(CONTRACT.functions.getter(1))) # error
        print("flag 3")
        tx_receipt = fullnode.eth.waitForTransactionReceipt(tx_hash)
    
    except:
        print("ERROR: cannot connect to Ethereum node. Start ethereum node first")
        sys.exit()

    


    totalStartTime = datetime.now()
    sendPool = Pool(THREAD_COUNT) # -> important: this should be in this "__main__" function
    
    # # transaction release
    # main()
    
    # storage trie of this contract
    print("\nBlock Number:\t\t\t" + str(fullnode.eth.blockNumber))
    print("Number of Transactions:\t\t" + str(len(getBlockTransactionHash(fullnode.eth.blockNumber)))) # number of Txs in this block
    
    updatingContractAddr = contractAddress(getBlockTransactionHash(fullnode.eth.blockNumber)[0]) # contract address of this transaction # only one contract -> [0]
    print("Updating Contract Address:\t" + str(updatingContractAddr))
    print("Updated Contract Address:\t" + str(CONTRACTADDR))

    print("")

    for i in range(0, 20): # there are (2^32 - 1) slots (=contract storage)
        print("Storage of this contract:\t" + str(i) + "\t" + str(getStorageAt(CONTRACTADDR, i).hex()))

    totalEndTime = datetime.now() - totalStartTime
    print("\ntotal elapsed:", totalEndTime.seconds, "seconds")
    print("DONE")
    
