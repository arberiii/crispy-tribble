import pytest
from src.utils import scriptpubkey_to_address

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