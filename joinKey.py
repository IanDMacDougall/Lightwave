"""
Project: Lightwave Communications
Authors: Ian MacDougall, Gage Pavia
Date Created: 12 October 2023
Last Modified: 30 November 2023
File Description: Manages the call key functionalities.
Repository: https://github.com/macdougalliatwit/lightwave
"""

import zlib
import base64
import secrets
import string


def compress_data( data ):
    xor_key = generate_key_for_data()
    data = xor_key + xor_cipher( data, xor_key )
    return zlib.compress( data.encode() )

def encode_data( data ):
    # If data is compressed, use it directly. Otherwise, encode the original data
    return base64.urlsafe_b64encode( data ).decode('utf-8')


def decode_data( encoded_data ):
    return base64.urlsafe_b64decode( encoded_data.encode('utf-8') )
 
def decompress_data( compressed_data ):
    uncompressed_data = zlib.decompress( compressed_data ).decode()
    xor_key = uncompressed_data[:6]
    data = uncompressed_data[6:]
    return xor_cipher( data, xor_key )

def xor_cipher( data, key ):
    return ''.join( chr( ord( c ) ^ ord( key[ i % len( key ) ] ) ) for i, c in enumerate( data ) )
 

def generate_key_for_data( length=6 ):
    usable_chars = string.ascii_letters + string.digits + string.punctuation

    random_key = ''.join( secrets.choice( usable_chars ) for _ in range( length ) )
    return random_key

