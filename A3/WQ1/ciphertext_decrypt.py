with open("p2p1", "rb") as diff_text:
    text = []
    byte = diff_text.read(1)
    while byte:
        chr_int = int.from_bytes(byte, byteorder='big')
        print(chr_int)
        text.append(chr(chr_int))
        byte = diff_text.read(1)
    print(text)
