# smartcontract-search-tool
Search the blockhash and transaction hash of a deployed smart contract in ethereum using Web3py.

The tool uses a thread pool ( with default 2 threads) to search for the contract address in the ethereum blockchain. It traverses the blockchain starting from the latest block to initial blocks.


# Prerequisite

In order to run this you will need 'click' package in python. If you dont have 'click' package use 

```pip install click```

You will also require an infura host with you API secret. You create the api secret here:
https://infura.io/


# Usage:

Run the following in terminal 

```python3 smartcontract-search-tool.py```

Then provide 

```<valid_contract_address>```

```<infura_host>```


# Configuration: 

You can change the number of threads used to perform the search by changing ```MAX_THREADS``` in the python file.

