import os
import time
from bitcoin_rpc import BitcoinRPC
from database import Input, Output, init_db, Block, Transaction
from datetime import datetime
import threading
from dotenv import load_dotenv

from utils import scriptpubkey_to_address, save_block_data, load_block_data

# Use environment variables for database credentials
load_dotenv()
ENABLE_BLOCK_CACHE = os.getenv('ENABLE_BLOCK_CACHE') == 'true'

class BitcoinIndexer:
    def __init__(self):
        self.rpc = BitcoinRPC()
        self.db = init_db()
        self.cache_dir = "data/blocks"

    def _get_block_data(self, height):
        # Try to load from cache first
        try:
            print(f"Loading block {height} from cache")
            return load_block_data(height, self.cache_dir)
        except FileNotFoundError:
            # If not in cache, fetch from RPC
            # Get block hash
            block_hash = self.rpc.get_block_hash(height)
            print(f"Block hash: {block_hash}")

            print(f"Fetching block {height} from RPC")
            block_data = self.rpc.get_block(block_hash)
            
            # Add height to block data for caching
            block_data['height'] = height
            
            if ENABLE_BLOCK_CACHE:
                # Cache the result
                save_block_data(block_data, self.cache_dir)
            
            return block_data

    def index_block(self, height):
        
        
        # Get block data (now with caching)
        block_data = self._get_block_data(height)
        
        # Create block record
        block = Block(
            height=height,
            hash=block_data['hash'],
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
                input = Input(txid=vin['txid'], vout=vin['vout'], tx_spent=tx['txid'])
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
    NUM_THREADS = 10
    START_BLOCK = 1
    END_BLOCK = 250_000
    
    # Calculate blocks per thread
    blocks_per_thread = (END_BLOCK - START_BLOCK + 1) // NUM_THREADS
    
    indexers = [BitcoinIndexer() for _ in range(NUM_THREADS)]
    threads = []
    
    start_time = time.time()
    
    # Create and start threads
    for i in range(NUM_THREADS):
        start = START_BLOCK + (i * blocks_per_thread)
        end = start + blocks_per_thread - 1 if i < NUM_THREADS - 1 else END_BLOCK
        thread = threading.Thread(
            target=indexers[i].index_range,
            args=(start, end)
        )
        threads.append(thread)
        thread.start()
        print(f"Thread {i+1} processing blocks {start} to {end}")
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
