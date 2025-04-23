import binascii

def generate_crc32_hash(url):
    crc = binascii.crc32(url.encode())
    return format(crc & 0xFFFFFFFF, '08x')  # Ensure 8-digit hex