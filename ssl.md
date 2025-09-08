# Learn OpenSSL 

Purpouse of SSL/TLS is protect the data in three ways:

1. **Confidenciality**: Data is only accesible by Client and Server (Encryption)
2. **Integrity**: Data is not modified between Clinet and Server (Hashing)
3. **Authentication**:  Client/Server are indeed who they say they are (PKI)

## Anti-Replay and Non-Repudiation

- **AntiReplay**: provided with built-in sequence numbers, buil-in to Integrity + Authentication mechanism
- **Non-Repudiation**: sender cannot later deny sending a message, byproduct of Integrity + Authentication


## Key Player of SSL

- **Client**
    - Entity initiating the TLS handshake
    - web browser, phone, apps, IoT
    - Optionally authenticated (rare)

- **Server**
    - Entity receiving the TLS handshake
    - Web Server, apache, nginx, IIS, Load balancer
    - Alwat authenticated

- **Certificate Authority**
    - Governing entity that issues Certificates
    - Trusted by Client and Server
    - Provides Trust Anchor
        - If we trust the CA, we trust what the CA trust

## Hashing

Algorithm which takes as input message of arbitrary lenght and produces as output a "fingerprint" of the original message

Result of hashing algorithm is called a **Digest**. Digest is also known: checksum, fingerprint, hash CRC

Hashing algorithms must satisfy four requeriments:
1. Infeasible to produce a given digest
2. Impossible to extact original message
3. Slight change produce drastic differences
4. Resulting digest is fixed width (length)

### Collisions

- Two messages result in identical digests
- Cannnot by avoided, it is a byproduct of "fixed width digests"
- Can only be made more rare

### Message Authentication Code (MAC)
- concept combining Message + Secret Key when calculating Digest
- Provides integrity and authntication for bulk data transfer
- Message + secret key must be combined in the same way
- Industry standard implementation of MAC: HMAC (Hash Based MEssage Authetication COde(RFC 2104)

## Encryption

- Encryption is used to provide Confidentiality
- confidentiality: Only intended recipient can interpret the Data
- Key Based Encryption: combines industry vetted algorithm with a Secret Key

### Key based Encryption

1. Symmetric Encryption: Encrypt and decrypt using the same keys
    - Strenght: 
        - faster -lower CPU Cost
        - Cipher text is same size as plain text
    - Weakness:
        - Secret key must be shared - Less Secure
    - ideal for bulk Data
    - Some algorithms are: DES, RC4, ·DES, AES, ChaCha20

2. Asymmetric Encryption: Encrypt and decrypt using different keys
    - Two different keys that are matematically realted
    - What one key Encrypts, only the other can Decrypt
        - one key will be made public
        - other key will be kept private
    - Strenght: 
        - Private Key is never shared - More Secure
    - Weakness:
        - Slower - Requieres much larger key sizes
        - Cipher text expansion
    - Ideal for restricted to limited Data
    - Some algorithm are: DSA, RSA, Diffie-Hellman, ECDSA, ECDH
    - Asymmetric Key Pairs can provide Encryption and signatures


### Hybirid  Encryption

Concept of using both asymmetric nd symmetric Encryption:

- Asymmectric encryption to facilitate a key exchange mean establish symmetric keys

- Secret Key used with smmetric Encryption for bulk data
    
### Signatures

- uses the sneder's private key to encrypt the hash of a data
- provides integrity adn authentication for what is signed

## PKI Public key infraestructure

Three entities form a PKI: Client, Server and CA
- Client: need to connect securely or verify an identity
- Server needs to prove its identity
- Certificate Authority: validate identities and generates certificates

