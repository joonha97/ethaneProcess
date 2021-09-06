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

# SGBJ smart contract
# put employ code to geth console & start mining => then we will get contract address
# CONTRACTADDR = Web3.toChecksumAddress("0xB201a0e33f7c0c672629be21bF027701A39D0F4B")
# CONTRACTADDR = Web3.toChecksumAddress("0x17c33F7747098BF36c950cdd4B0681231B38E581") # (joonha)
# abiString = '[ { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": false, "inputs": [ { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "address", "name": "userAddr", "type": "address" } ], "name": "addDeposit", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "address", "name": "userAddr", "type": "address" } ], "name": "addWashCount", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "balanceSum", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "depositWinners", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "greet", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "greeting", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "interestRate", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "lottoEpoch", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "roundNumber", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [], "name": "selectWinner", "outputs": [ { "internalType": "address", "name": "", "type": "address" }, { "internalType": "address", "name": "", "type": "address" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "uint256", "name": "newLottoEpoch", "type": "uint256" } ], "name": "setEpoch", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "string", "name": "newGreeting", "type": "string" } ], "name": "setGreeting", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "userCount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "users", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "", "type": "address" } ], "name": "usersBalance", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "", "type": "address" } ], "name": "usersWashCount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "washCountSum", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "washCountWinners", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "name": "winningsAmount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "address", "name": "userAddr", "type": "address" } ], "name": "withdrawDeposit", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]'
# CONTRACTABI = json.loads(abiString)
# sgbjContract = fullnode.eth.contract(address=CONTRACTADDR, abi=CONTRACTABI)

# gas amount for transaction (should be large enough)
# GAS = 1000000


# functions
def main():
    
    if ACCOUNT_NUM < TX_PER_BLOCK:
        print("too less accounts. at least", TX_PER_BLOCK, "accounts are needed")
        return

    print("Insert ", ACCOUNT_NUM, " accounts")

    # unlock coinbase
    fullnode.geth.personal.unlockAccount(fullnode.eth.coinbase, PASSWORD, 0)

    # stop mining
    fullnode.geth.miner.stop()

    # get current block
    currentBlock = fullnode.eth.blockNumber

    # main loop for send txs
    print("start sending transactions")
    offset = 1
    txNums = [int(TX_PER_BLOCK/THREAD_COUNT)]*THREAD_COUNT
    txNums[0] += TX_PER_BLOCK%THREAD_COUNT
    for i in range(int(ACCOUNT_NUM / TX_PER_BLOCK)):
        # set arguments for multithreading function
        arguments = []
        for j in range(THREAD_COUNT):
            arguments.append((txNums[j], offset))
            offset += txNums[j]

        # send transactions
        sendPool.starmap(sendTransactions, arguments)
        print("inserted ", (i+1)*TX_PER_BLOCK, "accounts")

        # mining
        fullnode.geth.miner.start(1)  # start mining
        while (fullnode.eth.blockNumber == currentBlock):
            pass # just wait for mining
        fullnode.geth.miner.stop()  # stop mining
        currentBlock = fullnode.eth.blockNumber


# (EOA)
# def sendTransaction(to):
#     #print("start try to send tx to full node")
#     #print("to: ", to, "/ from: ", fullnode.eth.coinbase)
#     while True:
#         try:
#             fullnode.eth.sendTransaction(
#                 {'to': to, 'from': fullnode.eth.coinbase, 'value': '1', 'gas': '21000', 'data': ""})
#             break
#         except:
#             continue



def sendTransactions(num, offset):
    for i in range(int(num)):
        # set receiver
        if INCREMENTAL_RECEIVER_ADDRESS:
            to = intToAddr(int(offset+i))
        else:
            to = makeRandHex()

        # if the upper bound is set, select receiver within the bound
        if MAX_ADDRESS != 0:
            to = intToAddr(random.randint(1, MAX_ADDRESS))
        
        # set send amount
        if INCREMENTAL_SEND_AMOUNT:
            amount = int(offset+i)
        else:
            amount = int(1) # int(1) (joonha)

        # print("to: ", to, "/ from: ", fullnode.eth.coinbase, "/ amount:", amount)

        while True:
            try:
                # EOA Transaction
                # fullnode.eth.sendTransaction(
                #     {'to': to, 'from': fullnode.eth.coinbase, 'value': hex(amount), 'gas': '21000', 'data': ""})
                # Contract Transaction
                sendContractTransaction(
                    # CA : from/data
                    # EOA : to/from/value/gas/data
                    # SGBJ contract obj code into 'data' field
                    {'from': fullnode.eth.coinbase, 'data': "60806040523480156200001157600080fd5b50610bb960068190555060146007819055506040805190810160405280600a81526020017f77686f2061726520753f00000000000000000000000000000000000000000000815250600c90805190602001906200007092919062000077565b5062000126565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10620000ba57805160ff1916838001178555620000eb565b82800160010185558215620000eb579182015b82811115620000ea578251825591602001919060010190620000cd565b5b509050620000fa9190620000fe565b5090565b6200012391905b808211156200011f57600081600090555060010162000105565b5090565b90565b61156d80620001366000396000f3fe60806040526004361061010c576000357c01000000000000000000000000000000000000000000000000000000009004806307973ccf146101115780630ceb2cef1461013c5780631bcc43621461017757806320c2a3d6146101a257806333a99e041461021d578063365b98b2146102a75780634e2786fb146103225780635050dad01461034d578063583243351461039c5780635cc635de146104015780637b91527a1461047c5780637c3a00fd146104a7578063892d2be2146104d2578063a413686214610537578063bac47e68146105ff578063bfdeb6491461062a578063cfae321714610685578063d7f1b25b14610715578063ef690cc014610770578063fb8b799214610800575b600080fd5b34801561011d57600080fd5b5061012661085b565b6040518082815260200191505060405180910390f35b34801561014857600080fd5b506101756004803603602081101561015f57600080fd5b8101908080359060200190929190505050610861565b005b34801561018357600080fd5b5061018c61086b565b6040518082815260200191505060405180910390f35b3480156101ae57600080fd5b506101db600480360360208110156101c557600080fd5b8101908080359060200190929190505050610871565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561022957600080fd5b506102326108af565b604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019250505060405180910390f35b3480156102b357600080fd5b506102e0600480360360208110156102ca57600080fd5b8101908080359060200190929190505050610ebd565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561032e57600080fd5b50610337610efb565b6040518082815260200191505060405180910390f35b34801561035957600080fd5b506103866004803603602081101561037057600080fd5b8101908080359060200190929190505050610f01565b6040518082815260200191505060405180910390f35b3480156103a857600080fd5b506103eb600480360360208110156103bf57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610f24565b6040518082815260200191505060405180910390f35b34801561040d57600080fd5b5061043a6004803603602081101561042457600080fd5b8101908080359060200190929190505050610f3c565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561048857600080fd5b50610491610f7a565b6040518082815260200191505060405180910390f35b3480156104b357600080fd5b506104bc610f80565b6040518082815260200191505060405180910390f35b3480156104de57600080fd5b50610521600480360360208110156104f557600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610f86565b6040518082815260200191505060405180910390f35b34801561054357600080fd5b506105fd6004803603602081101561055a57600080fd5b810190808035906020019064010000000081111561057757600080fd5b82018360208201111561058957600080fd5b803590602001918460018302840111640100000000831117156105ab57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610f9e565b005b34801561060b57600080fd5b50610614610fb8565b6040518082815260200191505060405180910390f35b34801561063657600080fd5b506106836004803603604081101561064d57600080fd5b8101908080359060200190929190803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610fbe565b005b34801561069157600080fd5b5061069a61112c565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156106da5780820151818401526020810190506106bf565b50505050905090810190601f1680156107075780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561072157600080fd5b5061076e6004803603604081101561073857600080fd5b8101908080359060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506111ce565b005b34801561077c57600080fd5b5061078561133c565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156107c55780820151818401526020810190506107aa565b50505050905090810190601f1680156107f25780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561080c57600080fd5b506108596004803603604081101561082357600080fd5b8101908080359060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506113da565b005b60035481565b8060068190555050565b60055481565b600a8181548110151561088057fe5b906000526020600020016000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60008060006108bf600454611486565b90506000806001600080549050038154811015156108d957fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905060008090505b600080549050811015610a675760016000808381548110151561092b57fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054831115610a19576001600080838154811015156109aa57fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205483039250610a5a565b600081815481101515610a2857fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169150610a67565b808060010191505061090c565b50610a73600554611486565b9150600080600160008054905003815481101515610a8d57fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905060008090505b600080549050811015610c9457600260008083815481101515610adf57fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054841115610bcd57600260008083815481101515610b5e57fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205484039350610c0a565b600081815481101515610bdc57fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1691505b6000600260008084815481101515610c1e57fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508080600101915050610ac0565b5060006005819055506000600454905060008090505b600654811015610cda5760075460640182029150606482811515610cca57fe5b0491508080600101915050610caa565b5060045481039050600281811515610cee57fe5b04600160008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540192505081905550600281811515610d4757fe5b048103600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055508060046000828254019250508190555060098390806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050600a8290806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050600b8190806001815401808255809150509060018203906000526020600020016000909192909190915055506001600860008282540192505081905550828295509550505050509091565b600081815481101515610ecc57fe5b906000526020600020016000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60085481565b600b81815481101515610f1057fe5b906000526020600020016000915090505481565b60016020528060005260406000206000915090505481565b600981815481101515610f4b57fe5b906000526020600020016000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60045481565b60075481565b60026020528060005260406000206000915090505481565b80600c9080519060200190610fb492919061149c565b5050565b60065481565b81600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055508160046000828254019250508190555060008090505b6000805490508110156110ae578173ffffffffffffffffffffffffffffffffffffffff1660008281548110151561105457fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614156110a15750611128565b8080600101915050611021565b5060008190806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550506003600081548092919060010191905055505b5050565b6060600c8054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156111c45780601f10611199576101008083540402835291602001916111c4565b820191906000526020600020905b8154815290600101906020018083116111a757829003601f168201915b5050505050905090565b81600260008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055508160056000828254019250508190555060008090505b6000805490508110156112be578173ffffffffffffffffffffffffffffffffffffffff1660008281548110151561126457fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614156112b15750611338565b8080600101915050611231565b5060008190806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550506003600081548092919060010191905055505b5050565b600c8054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156113d25780601f106113a7576101008083540402835291602001916113d2565b820191906000526020600020905b8154815290600101906020018083116113b557829003601f168201915b505050505081565b81600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020541015151561142557fe5b81600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540392505081905550816004600082825403925050819055505050565b600060028281151561149457fe5b049050919050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106114dd57805160ff191683800117855561150b565b8280016001018555821561150b579182015b8281111561150a5782518255916020019190600101906114ef565b5b509050611518919061151c565b5090565b61153e91905b8082111561153a576000816000905550600101611522565b5090565b9056fea165627a7a723058200746d895035cda19945beb6848b8e05cbd7984dd196ab161989b914a7a9077640029"})
                break
            except:
                time.sleep(1)
                continue



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

    totalStartTime = datetime.now()
    sendPool = Pool(THREAD_COUNT) # -> important: this should be in this "__main__" function
    
    # transaction release
    main()
    
    # storage trie of this contract
    print("\nBlock Number:\t\t\t" + str(fullnode.eth.blockNumber))
    print("Number of Transactions:\t\t" + str(len(getBlockTransactionHash(fullnode.eth.blockNumber)))) # number of Txs in this block
    prevContractAddr = contractAddress(getBlockTransactionHash(fullnode.eth.blockNumber - 1)[0]) # contract address of this transaction # only one contract -> [0]
    print("Previous Contract Address:\t" + str(prevContractAddr))
    contractAddr = contractAddress(getBlockTransactionHash(fullnode.eth.blockNumber)[0]) # contract address of this transaction # only one contract -> [0]
    print("Contract Address:\t\t" + str(contractAddr))
    # print("Storage of this contract:\t" + str(getStorageAt(contractAddr, fullnode.eth.blockNumber).hex())) # ??? position = The index position of the storage ... what?

    print("Prev Address's Balance:\t\t" + str(fullnode.eth.getBalance(prevContractAddr)))
    print("Contract Address's Balance:\t" + str(fullnode.eth.getBalance(contractAddr)))


    print("")

    for i in range(0, 20): # there are (2^32 - 1) slots
        print("Storage of this contract:\t" + str(i) + "\t" + str(getStorageAt(contractAddr, i).hex()))

    totalEndTime = datetime.now() - totalStartTime
    print("\ntotal elapsed:", totalEndTime.seconds, "seconds")
    print("DONE")
    
