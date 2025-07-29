# Source: https://github.com/fivetran/fivetran_sdk/tree/v2/examples/destination_connector/python
import csv

from Crypto.Cipher import AES
from zstandard import ZstdDecompressor


# AES decryption function
def aes_decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv=ciphertext[: AES.block_size])
    plaintext = cipher.decrypt(ciphertext[AES.block_size :])
    return plaintext.rstrip(b"\0")


# Zstandard decompression function
def zstd_decompress(compressed_data):
    decompressor = ZstdDecompressor()
    return decompressor.decompressobj().decompress(compressed_data)


# Read the encrypted and compressed data
def decrypt_file(input_file_path, value):
    with open(input_file_path, "rb") as file:
        encrypted_and_compressed_data = file.read()
        decrypted_data = aes_decrypt(value, encrypted_and_compressed_data)
        decompressed_data = zstd_decompress(decrypted_data)
        csv_data = decompressed_data.decode("utf-8")
        csv_reader = csv.reader(csv_data.splitlines())
        headers = next(csv_reader)
        for row in csv_reader:
            yield dict(zip(headers, row))
