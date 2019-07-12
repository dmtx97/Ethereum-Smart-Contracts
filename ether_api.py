import urllib.request, json
import os, os.path
import requests
from bs4 import BeautifulSoup

page = requests.get('https://etherscan.io/contractsVerified/1?filter=solc&ps=100')
soup = BeautifulSoup(page.text, 'html.parser')

contract_address = []
for val in soup.select('a[class*="hash-tag text-truncate"]'):
    contract_address.append(val.get_text())

api_key = ""

for contract in contract_address:
    uri = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address={}&apikey={}".format(contract, api_key)

    with urllib.request.urlopen(uri) as url:
        data = json.loads(url.read().decode())
        code = data["result"]
        code = code[0]
        code = code.get("SourceCode")

    if not os.path.isdir("./output"):
        os.mkdir('./output')

    if "pragma solidity ^0.5" in code:
        with open('./output/%s.sol' % contract, 'w+') as f:
            f.write(code)
