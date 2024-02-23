import csv
import asyncio
import aiohttp
from web3 import Web3
import random  # 添加了这一行

# 替换成你的Lava RPC链接
RpcUrl = 'https://eth1.lava.build/lava-referer-74873735-1631-4095-b955-4e26e95780a5/'
provider = Web3(Web3.HTTPProvider(RpcUrl))

csvFilePath = './wallet.csv'

async def checkBalanceAndAppend(line, provider):
    columns = line.split(',')
    address = columns[0].strip()
    try:
        balance = provider.eth.getBalance(address)
        balanceEther = provider.fromWei(balance, 'ether')
        print(f"Address: {address} - Balance: {balanceEther} ETH")
        return f"\n{line}{',' if len(columns) > 1 else ''}{balanceEther}"
    except Exception as e:
        print(f"Error fetching balance for address {address}: {e}")
        return f"\n{line}"

async def main():
    with open(csvFilePath, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)
        newCsvContent = lines[0][0] if 'balance' in lines[0] else lines[0][0] + ',balance'

        for line in lines[1:]:
            if line:
                await asyncio.sleep((await asyncio.get_event_loop().run_in_executor(None, lambda: random.randint(1000, 3000))) / 1000)
                result = await checkBalanceAndAppend(line[0], provider)
                newCsvContent += result

    print(newCsvContent)

asyncio.run(main())
