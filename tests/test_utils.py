import pytest
from src.utils import scriptpubkey_to_address, save_block_data, load_block_data
import os

def test_scriptpubkey_to_address_with_single_address():
    scriptpubkey = {
        'address': 'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq'
    }
    assert scriptpubkey_to_address(scriptpubkey) == 'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq'

def test_scriptpubkey_to_address_with_addresses_array():
    scriptpubkey = {
        'addresses': ['bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq']
    }
    assert scriptpubkey_to_address(scriptpubkey) == 'bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq'

def test_scriptpubkey_to_address_with_pubkey():
    scriptpubkey = {
        'asm': '04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f OP_CHECKSIG',
        'desc': 'pk(04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f)#vlz6ztea',
        'hex': '4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac',
        'type': 'pubkey'
    }
    assert scriptpubkey_to_address(scriptpubkey) == '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'

def test_save_and_load_block_data(tmp_path):
    # Test data
    block_data = {
        "height": 12345,
        "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
        "time": 1231006505
    }
    
    # Save block data
    data_dir = str(tmp_path / "blocks")
    saved_path = save_block_data(block_data, data_dir=data_dir)
    
    # Verify file exists
    assert os.path.exists(saved_path)
    
    # Load and verify data
    loaded_data = load_block_data(12345, data_dir=data_dir)
    assert loaded_data == block_data

def test_save_block_data_missing_height(tmp_path):
    block_data = {
        "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
    }
    
    with pytest.raises(ValueError, match="Block data must contain 'height' field"):
        save_block_data(block_data, data_dir=str(tmp_path))

def test_load_block_data_nonexistent(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_block_data(99999, data_dir=str(tmp_path))