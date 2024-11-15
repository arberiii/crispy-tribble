import hashlib
import base58

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

