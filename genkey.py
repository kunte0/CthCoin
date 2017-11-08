from ecdsa import SigningKey, NIST384p


# generate the SK
print('[+] Generating Secretkey.')
sk = SigningKey.generate(curve=NIST384p)
sk_pem = sk.to_pem()

print('[+] Writing Secretkey to file.')
f = open('sk.pem', 'wb')
f.write(sk_pem)

f.close()
print('[+] Done.')
