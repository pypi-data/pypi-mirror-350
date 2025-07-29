blockcheck is a high-performance Python package designed to give you quick and reliable access to essential Bitcoin blockchain data. Leveraging the speed and efficiency of Rust under the hood, blockcheck allows you to effortlessly query Bitcoin addresses for their balances, transaction counts, and total received amounts, all powered by the robust bitcoin blockchain

Whether you're building a cryptocurrency wallet, a blockchain analytics tool, or simply need to track specific Bitcoin addresses, blockcheck provides a fast and easy-to-use solution without the overhead typically associated with raw API interactions.

Key Features
Blazing Fast Performance: Written in Rust, blockcheck compiles to native code, offering superior speed and memory efficiency compared to pure Python implementations, especially for data-intensive operations.
Simple & Intuitive API: Interact with the bitcoin blockchain API through a clean and Pythonic interface. No need to worry about HTTP requests or JSON parsing – blockcheck handles it all.
Essential Bitcoin Metrics: Easily retrieve:
Current Balance: The spendable balance of a given Bitcoin address (in satoshis).
Transaction Count: The total number of transactions associated with the address.
Total Received: The cumulative amount of Bitcoin ever received by the address (in satoshis).
Reliable Data Source: Utilizes the widely recognized and trusted bitcoin blockchain API for accurate and up-to-date information.
Installation
Getting blockcheck up and running is straightforward. Simply use pip:

Bash

pip install blockcheck
Note: As blockcheck contains Rust extensions, a Rust toolchain will be required on your system for successful installation if pre-compiled wheels are not available for your specific environment. Most users, however, will find the installation seamless.

Usage
Interacting with blockcheck is designed to be as simple as possible. After installation, you can import the blockcheck module and use its primary function, get_balance.

Python

import blockcheck

# A well-known Bitcoin address (Satoshi Nakamoto's Genesis Block address)
address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"

try:
    # Retrieve balance, transaction count, and total received
    balance, n_tx, total_received = blockcheck.get_balance(address)

    print(f"--- Bitcoin Address Details ---")
    print(f"Address: {address}")
    print(f"Current Balance: {balance} satoshis")
    print(f"Total Transactions: {n_tx}")
    print(f"Total Received: {total_received} satoshis")
    print(f"-----------------------------")

    # You can also convert satoshis to BTC for readability
    balance_btc = balance / 10**8
    total_received_btc = total_received / 10**8
    print(f"\nIn BTC:")
    print(f"Current Balance: {balance_btc} BTC")
    print(f"Total Received: {total_received_btc} BTC")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please check the address or your internet connection.")

Error Handling
blockcheck aims to provide clear error messages for common issues, such as an invalid Bitcoin address or network problems. It's always a good practice to wrap your blockcheck calls in try...except blocks to gracefully handle potential API errors or connectivity issues.

Contribution & Support
blockcheck is an open-source project, and contributions are welcome! If you encounter issues, have feature requests, or would like to contribute code, please visit the GitHub repository.
