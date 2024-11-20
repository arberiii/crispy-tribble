from bitcoinrpc.authproxy import AuthServiceProxy

class BitcoinRPC:
    def __init__(self, rpc_url: str):
        if not rpc_url:
            raise ValueError("BITCOIN_RPC_URL environment variable is not set")
        self.rpc = AuthServiceProxy(rpc_url)

    def get_block_count(self):
        return self.rpc.getblockcount()

    def get_block_hash(self, height):
        return self.rpc.getblockhash(height)

    def get_block(self, block_hash):
        return self.rpc.getblock(block_hash, 2)  # 2 for verbose transaction data

    def get_transaction(self, txid):
        return self.rpc.getrawtransaction(txid, True)  # True for verbose output

