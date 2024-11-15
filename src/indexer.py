from bitcoin_rpc import BitcoinRPC
from database import init_db, Block, Transaction
from datetime import datetime

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
            self.db.add(transaction)
        
        self.db.commit()

    def _calculate_fee(self, tx):
        if 'coinbase' in tx['vin'][0]:  # Skip coinbase transactions
            return 0
        
        total_in = sum(
            float(self.rpc.get_transaction(vin['txid'])['vout'][vin['vout']]['value'])
            for vin in tx['vin']
        )
        total_out = sum(float(vout['value']) for vout in tx['vout'])
        return total_in - total_out

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
    # Example: Index the first 1000 blocks
    indexer.index_range(2, 5) 