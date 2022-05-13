from nbformat import write
import rsa
#from sympy import public


# Use at least 2048 bit keys nowadays, see e.g. https://www.keylength.com/en/4/

publicKeyReloaded = None
privateKeyReloaded = None




def create_keys(key_val= 1516):
    global publicKeyReloaded  , privateKeyReloaded
    publicKey, privateKey = rsa.newkeys(key_val) 


    # Export public keys and private keys in PKCS#1 format, PEM encoded 

    publicKeyPkcs1PEM = publicKey.save_pkcs1().decode('utf8') 
    privateKeyPkcs1PEM = privateKey.save_pkcs1().decode('utf8') 

    privateKey_file= open("private_key.pem" , "w")
    privateKey_file.write(privateKeyPkcs1PEM)
    privateKey_file.close()

    publicKey_file = open("public_key.pem" , "w")
    publicKey_file.write(publicKeyPkcs1PEM)
    privateKey_file.close()


    print(type(privateKeyPkcs1PEM) , privateKeyPkcs1PEM)


def load():
    global publicKeyReloaded, privateKeyReloaded
    # Import public key in PKCS#1 format, PEM encoded
    #''' 
    f= open("public_key.pem" , 'r')
    publicKeyPkcs1PEM  = f.read()
    f.close()

    f= open("private_key.pem" , 'r')
    privateKeyPkcs1PEM  = f.read()
    f.close()

    #'''
    #print(type(privateKeyPkcs1PEM) , privateKeyPkcs1PEM)

    
    #publicKeyPkcs1PEM =  RSA.importKey(open("public_key.pem", "rb"))
    #privateKeyPkcs1PEM =  RSA.importKey(open("private_key.pem", "rb"))


    publicKeyReloaded = rsa.PublicKey.load_pkcs1(publicKeyPkcs1PEM.encode('utf8')) 
    # Import private key in PKCS#1 format, PEM encoded 
    privateKeyReloaded = rsa.PrivateKey.load_pkcs1(privateKeyPkcs1PEM.encode('utf8')) 

    #print("...load function " , publicKeyReloaded)


#print("...main " , publicKeyReloaded)


def encrypt(msg):
    global publicKeyReloaded
    #print("encrypt ....", publicKeyReloaded)
    #msg.encode('utf8')
    msg = str(msg).encode('utf8')
    #print(msg)


    if(publicKeyReloaded == None):
        load()
        if(publicKeyReloaded == None):
            print("Some Error Ocuured while encrypting ")
            return
    return rsa.encrypt(msg, publicKeyReloaded)



def decrypt(msg):

    #print(msg)
    global privateKeyReloaded
    if(privateKeyReloaded == None):
        load()
        if(privateKeyReloaded == None):
            print("Some Error Ocuured while dencrypting ")
            return
    return rsa.decrypt(msg, privateKeyReloaded)


#create_keys()
#load()
#print(data)




#print(decrypt(data).decode('utf8'))




#print("..........")



#d= b'\x00U\x84\xc5\x91[\x11\xa3\xee\x8a\xfd\xd76-\xba\xaa\xe7_n\xda\xbb\xddA\xb4F\x047\xd8\x8b\xd8\xe4\x17\xca\x05mz\xf4V>\x1b=\x8b,\x1eI\xbeh~\xb5\x9b<|\xfa3dV\x84\xb3\x02\x1d\xa7\xf5y73b\xf2\x94\xb0a\x185\xc0W\x8c\x8c\xc4\x0e\\\x01\x02ki\xb00;\xd1\x05Q\xdd\xfd\xbbL\xa5\xd6\xe5^\x81\x11\x98r>\xfc\xbc_\x99\x83\x83\x1d\xd6\x00\xeaa\x1c"\x9f\x98\xe0\xe1\xf7\x8c\x95\x8d\xdaN\xc5k\xa2\x1e\xc7RZ\x9f\xcc8Z1\x97\x9d@\xe9\xbc\xb7\xd0]\xda\xc5p_\x89\x96mY\x9e[\xb1vh\xfe2\xc2|E\\\xa3\x9c\xc7N\xfc$l\xeeV\x12\xab>\x8a\xd1ZQ\xcc\xd5\xd0\xe2\x88\xd1[\xdcD\x05'
#print(decrypt(d))