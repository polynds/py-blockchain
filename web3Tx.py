from web3 import Web3
import ccxt
from eth_abi import abi


def gwei_to_usd(gwei, gas_limit, ticker):
    exchange = ccxt.binance()
    current_ticker_details = exchange.fetch_ticker(ticker)
    ticker_price = current_ticker_details['close']
    price_in_usd = float(gwei * gas_limit) * 0.000000001 * ticker_price
    return price_in_usd


if __name__ == '__main__':
    # Settings
    receiver = '0x2dC336aA3F52B8646db0B508a466A702ccbE0a84'
    RPC = 'https://rpc-mumbai.maticvigil.com'
    privateKey = '5e6e53651fb0e4d8a0adb694fa3863abe8b02c4eb2a6c02ef41031c0e887b49a'
    value = '0.001'  # Value to send

    # Checksum
    web3 = Web3(Web3.HTTPProvider(RPC))
    account = web3.eth.account.from_key(privateKey)
    address_wallet = account.address
    checksum_address = Web3.to_checksum_address(address_wallet)
    print('Wallet: ', address_wallet)

    # Balance
    balance = web3.eth.get_balance(checksum_address)
    ether_balance = Web3.from_wei(balance, 'ether')
    print('Balance: ', round(ether_balance, 3))

    # Gas price
    gas_limit = web3.eth.estimate_gas({"from": address_wallet, "to": receiver}, "latest")
    print('Gas limit: ', gas_limit)
    gas_price = web3.eth.gas_price
    gas_price_in_gwei = web3.from_wei(gas_price, 'gwei')
    print('Gas price: ', gas_price_in_gwei, 'Gwei')
    print('Gas price: ', round(gwei_to_usd(gas_price_in_gwei, gas_limit, 'MATIC/USDT'), 5), '$')

    function_name = ''
    sendData = ''
    data = abi.encode()

    # Build the transaction
    tx = {
        "nonce": web3.eth.get_transaction_count(address_wallet),
        "to": receiver,
        "value": web3.to_wei(value, "ether"),
        "gas": gas_limit,
        "gasPrice": web3.eth.gas_price,
        "chainId": web3.eth.chain_id,
        "data": data,
    }

    # Sign and send tx
    signed_tx = web3.eth.account.sign_transaction(tx, privateKey)
    print("tx:", tx)
    print("address_wallet:", address_wallet)
    print("Raw", signed_tx)
    # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # print("Transaction hash: ", web3.to_hex(tx_hash))
