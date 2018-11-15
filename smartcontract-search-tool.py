#!/usr/bin/python3

from web3 import Web3
import threading
import time
from concurrent import futures
import click
import os

# config
MAX_THREADS = 2  # Number of threads to be used for searching the blocks


web3provider = 'global'
w3 = 'global'
searchContractAddress = 'global'
executor = 'global'
found = False


@click.command()
@click.option('--contract', prompt='Enter contract address', help='contract address to search for')
@click.option('--host', prompt='Enter infura host',
              help='Infura host  https://mainnet.infura.io/<API_SECRET>')
def search(contract, host):
    """Cli tool to search for block hash and transaction hash of a given contract address"""

    try:
        global web3provider, w3, searchContractAddress
        searchContractAddress = contract
        web3provider = Web3.HTTPProvider(host)
        w3 = Web3(web3provider)
        code = w3.eth.getCode(contract)
        if(code.hex() != '0x'):
            print("Valid contract address")
            print("Starting the search")
            startSearch()
        else:
            raise Exception('Not a valid contract address')
    except Exception as e:
        print ("Error :", e)
        exit()


def startSearch():  # Latest blocks will be searched first
    startBlock = 1
    latestBlock = w3.eth.blockNumber
    global executor
    executor = futures.ThreadPoolExecutor(max_workers=MAX_THREADS)
    results = executor.map(searchBlock, range(latestBlock, startBlock, -1))
    real_results = list(results)


def searchBlock(sBlock):
    global found
    if(found == True):
        executor.shutdown(wait=False)
        os._exit(1)
    print("Searching in block: {}".format(sBlock))
    block = w3.eth.getBlock(sBlock)
    for txhash in block.transactions:
        tx = w3.eth.getTransaction(txhash)
        if(tx.to == None):
            txReceipt = w3.eth.getTransactionReceipt(tx.hash)
            if(txReceipt.contractAddress == searchContractAddress):
                print("For contract address: {}".format(searchContractAddress))
                print("Block hash: {}".format(txReceipt.blockHash.hex()))
                print("Transaction hash: {}".format(
                    txReceipt.transactionHash.hex()))
                found = True
                return 1
    return 0


if __name__ == '__main__':
    search()
