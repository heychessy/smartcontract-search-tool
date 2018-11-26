#!/usr/bin/python3

from web3 import Web3
import time
from concurrent.futures import ThreadPoolExecutor
import click
import os

# config
MAX_THREADS = 2  # Number of threads to be used for searching the blocks


web3provider = 'global'
w3 = 'global'
searchContractAddress = 'global'
startBlock = 'global'
latestBlock = 'global'
executor = 'global'
contractBlock = 'global'
found = False


@click.command()
@click.option('--contract', default="0xD70dD291f3aEc40f3719035EF441F2300A4EF289", help='contract address to search for')
@click.option('--host', default="https://mainnet.infura.io/v3/b0b554bc8d514eeabad6429f54eefc12",
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
        # traceback.print_exc()
        exit()


def startSearch():
    global startBlock, latestBlock
    startBlock = 1
    latestBlock = w3.eth.blockNumber
    startTime = time.time()
    global executor
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        chunk = MAX_THREADS
        for i in range(chunk):
            print("Starting thread {}".format(i+1))
            future = executor.submit(searchContractBlock, (
                int((i)*latestBlock/chunk) + 1), int((i+1)*(latestBlock/chunk)))
        print(future.result())
    #results = executor.map(searchContractBlock, range(startBlock, latestBlock), chunksize=latestBlock/MAX_THREADS)
    #real_results = list(results)
    #contractBlock = searchContractBlock(startBlock, latestBlock)
    # print(real_results)
    searchBlock(contractBl=ock)
    endTime = time.time()
    print("It took {}s".format(int(endTime-startTime)))


def searchContractBlock(start, end):
    print("Searching between block {} and {}".format(start, end))
    global found, contractBlock
    mid = int((start+end)/2)
    while(start <= end):
        if(found == True):
            break
        mid = int((start+end)/2)
        # print("{}".format(mid))
        code = w3.eth.getCode(searchContractAddress, mid)
        if(code.hex() != '0x'):
            end = mid
            code = w3.eth.getCode(searchContractAddress, start)
            if(code.hex() != '0x'):
                code = w3.eth.getCode(searchContractAddress, start-1)
                if(code.hex() != '0x'):
                    break
                print("Found contract block: {}".format(start))
                found = True
                contractBlock = start
                return start
            else:
                start = start+1
        else:
            start = mid+1


def searchBlock(sBlock):
    print("Searching info in contract block: {}".format(sBlock))
    block = w3.eth.getBlock(sBlock)
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for txhash in block.transactions:
            future = executor.submit(searchTx, txhash)


def searchTx(txhash):
    tx = w3.eth.getTransaction(txhash)
    if(tx.to == None):
        txReceipt = w3.eth.getTransactionReceipt(tx.hash)
        if(txReceipt.contractAddress == searchContractAddress):
            print("For contract address: {}".format(
                searchContractAddress))
            print("Block hash: {}".format(txReceipt.blockHash.hex()))
            print("Transaction hash: {}".format(
                txReceipt.transactionHash.hex()))
            exit()


if __name__ == '__main__':
    search()
