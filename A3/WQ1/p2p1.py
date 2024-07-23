with open("p2p1", "wb") as p2p1:
    with open("ciphertext1", "rb") as ciphertext1:
        with open("ciphertext2", "rb") as ciphertext2:
            ct1 = int.from_bytes(ciphertext1.read(1), byteorder='big')
            ct2 = int.from_bytes(ciphertext2.read(1), byteorder='big')
            while ct1:
                p2p1.write(int.to_bytes((ct2 - ct1) % 256, byteorder='big', length=1))
                ct1 = int.from_bytes(ciphertext1.read(1), byteorder='big')
                ct2 = int.from_bytes(ciphertext2.read(1), byteorder='big') 