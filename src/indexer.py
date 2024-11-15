import time
from bitcoin_rpc import BitcoinRPC
from database import Input, Output, init_db, Block, Transaction
from datetime import datetime

from utils import scriptpubkey_to_address

class BitcoinIndexer:
    def __init__(self):
        self.rpc = BitcoinRPC()
        self.db = init_db()

    def index_block(self, height):
        # Get block hash
        block_hash = self.rpc.get_block_hash(height)
        print(f"Block hash: {block_hash}")
        
        # Get full block data
        block_data = self.rpc.get_block(block_hash)
        
        # Create block record
        block = Block(
            height=height,
            hash=block_hash,
            timestamp=datetime.fromtimestamp(block_data['time'])
        )
        
        # Add block to database
        self.db.add(block)
        
        # Index all transactions in the block
        for tx in block_data['tx']:
            transaction = Transaction(
                txid=tx['txid'],
                block_height=height,
                timestamp=datetime.fromtimestamp(block_data['time']),
                fee=self._calculate_fee(tx),
                size=tx['size']
            )
            for vin in tx['vin']:
                if 'txid' not in vin or 'vout' not in vin:
                    continue
                input = Input(txid=vin['txid'], vout=vin['vout'])
                self.db.add(input)
            for vout in tx['vout']:
                if 'n' not in vout or 'value' not in vout or 'scriptPubKey' not in vout:
                    continue
                if vout["scriptPubKey"]["type"] == "multisig":
                    continue
                output = Output(txid=tx['txid'], n=vout['n'], value=vout['value'], address=scriptpubkey_to_address(vout['scriptPubKey']))
                self.db.add(output)
            self.db.add(transaction)
        
        self.db.commit()

    def _calculate_fee(self, tx):
        return tx.get('fee', 0)

    def index_range(self, start_height, end_height):
        for height in range(start_height, end_height + 1):
            try:
                print(f"Indexing block {height}")
                self.index_block(height)
            except Exception as e:
                print(f"Error indexing block {height}: {str(e)}")
                # roll back the transaction
                self.db.rollback()
                continue

if __name__ == "__main__":
    indexer = BitcoinIndexer()
    # time when it started and when it ended
    start_time = time.time()
    indexer.index_range(800_001, 800_100)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
