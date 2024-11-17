import decimal
import hashlib
import base58
import os
from pathlib import Path
import simplejson as json


def scriptpubkey_to_address(script: dict, network: str = "mainnet") -> str:
    """
    Converts a Bitcoin scriptPubKey to a Bitcoin address.
    
    :param script_pub_key: JSON string containing the scriptPubKey object.
    :param network: Bitcoin network ('mainnet' or 'testnet').
    :return: Bitcoin address as a string.
    """
    if 'address' in script:
        return script['address']
    elif 'addresses' in script and script['addresses']:
        return script['addresses'][0]
    # Extract the asm field and filter out OP_ codes
    asm = script.get("asm", "")
    components = asm.split(" ")
    clean_components = [comp for comp in components if not comp.startswith("OP_")]
    
    # Determine if it's a P2PKH or P2PK script
    if len(clean_components) == 1:
        # P2PK (Public Key)
        pubkey = clean_components[0]
        # Step 2: SHA-256 Hash
        sha256_hash = hashlib.sha256(bytes.fromhex(pubkey)).digest()
        # Step 3: RIPEMD-160 Hash
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        pubkey_hash = ripemd160.digest()
    elif len(clean_components) == 2:
        # P2PKH (Public Key Hash)
        pubkey_hash = bytes.fromhex(clean_components[0])
    else:
        raise ValueError(f"Unsupported scriptPubKey format {script}")
    
    # Step 4: Add network prefix
    prefix = b'\x00' if network == "mainnet" else b'\x6F'  # 0x00 for mainnet, 0x6F for testnet
    prefixed_hash = prefix + pubkey_hash
    
    # Step 5: Compute checksum
    checksum = hashlib.sha256(hashlib.sha256(prefixed_hash).digest()).digest()[:4]
    
    # Step 6: Append checksum
    final_bytes = prefixed_hash + checksum
    
    # Step 7: Base58 Encode
    address = base58.b58encode(final_bytes).decode('utf-8')
    return address

def save_block_data(block_data: dict, data_dir: str = "data/blocks") -> str:
    """
    Saves block data to a JSON file in the specified directory.
    
    Args:
        block_data (dict): The block data to save
        data_dir (str): Directory to save the block data (default: "data/blocks")
        
    Returns:
        str: Path to the saved file
    """
    # Create directory if it doesn't exist
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    # Use block height as filename
    block_height = block_data.get('height')
    if block_height is None:
        raise ValueError("Block data must contain 'height' field")
    
    # Create filename with block height padded to 8 digits
    filename = f"{block_height:08d}.json"
    file_path = os.path.join(data_dir, filename)
    
    # Save block data to file
    with open(file_path, 'w') as f:
        json.dump(block_data, f, indent=2)
    
    return file_path

def load_block_data(block_height: int, data_dir: str = "data/blocks") -> dict:
    """
    Loads block data from a JSON file.
    
    Args:
        block_height (int): The height of the block to load
        data_dir (str): Directory containing block data (default: "data/blocks")
        
    Returns:
        dict: The block data
        
    Raises:
        FileNotFoundError: If the block data file doesn't exist
    """
    filename = f"{block_height:08d}.json"
    file_path = os.path.join(data_dir, filename)
    
    with open(file_path, 'r') as f:
        return json.load(f)

