import csv
import requests
import json

# 你的Evmos节点RPC URL
EVMOS_RPC_URL = 'https://evmos.lava.build/lava-referer-74873735-1631-4095-b955-4e26e95780a5/'

def get_evmos_balance(address):
    # 构建JSON-RPC请求
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # 发起POST请求
        response = requests.post(EVMOS_RPC_URL, headers=headers, data=json.dumps(payload))
        # 解析响应并返回以太坊余额（以wei为单位）
        if response.status_code == 200:
            balance_wei = int(response.json()['result'], 16)
            return balance_wei
        else:
            print(f"Failed to fetch balance for address {address}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching balance for address {address}: {str(e)}")
        return None

# 读取CSV文件
with open('wallet.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    # 遍历每一行，查询地址余额并打印结果
    for row in reader:
        address = row[0]
        balance_wei = get_evmos_balance(address)
        if balance_wei is not None:
            # 将wei转换为以太币，并打印结果
            balance_evmos = balance_wei / 10**18
            print(f"Address: {address}, Balance: {balance_evmos} EVMOS")
