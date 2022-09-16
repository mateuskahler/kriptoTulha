[![Python Unit Tests](https://github.com/mateuskahler/kriptoTulha/actions/workflows/action-automated-tests.yml/badge.svg)](https://github.com/mateuskahler/kriptoTulha/actions/workflows/action-automated-tests.yml)  
# kriptoTulha
A set of Python functions to store data securely.

https://github.com/mateuskahler/kriptoTulha/blob/main/readme_files/ui_usage_video.mp4

<!--  https://user-images.githubusercontent.com/18375194/190828164-a495957c-911d-4c8e-8f0b-2db49f1e2311.mp4 -->


I used to keep a text file on my desktop with a lot of personal data. Realizing that the habit was growing dangerous, I decided to build a program to encrypt the content.

After studying cryptographic primitives, I created an application to browse my personal notes and passwords.

## Usage
The user interface can be launched with
```sh
python kriptoTulhaUI.py
```

The requirements are listed in `requirements.txt`, and can be installed with
```sh
pip3 install -r requirements.txt
```

This project requires Python >= 3.10, mostly because I enjoy using the type hints.

## Details

Items are manipulated as *title* and *content* pairs, but are never saved to disk in readable form. Decoding them requires providing a user-defined password. The encryption scheme follows:


```mermaid
graph TD
    classDef userProvided stroke:red
    RC[User Content]
    UP[User Password]
    PN[Salt 1]
    SN[Salt 2]
    PK[Primary Key]
    SK[Secondary Key]
    KD1(Key Derivation)
    KD2(Key Derivation)

    UP ---> KD1
    PN --> KD1
    KD1 --> PK

    UP ---> KD2
    SN --> KD2
    KD2 --> SK

    TN[Salt 3]
    CH1(Cryptographic Hash)
    VS[Validity Stamp]
    SK --> CH1
    TN --> CH1
    RC ---> CH1
    CH1 --> VS

    VC[Content Stamped]
    CC(Cipher)
    QN[Salt 4]
    VS --> VC
    RC ---> VC
    VC --> CC
    PK ---> CC
    QN --> CC

    EC[Encrypted Content]
    CC --> EC

    class UP userProvided
    class RC userProvided
```

`Key derivation` is done using Argon2, a memory hard funtion.  
`Validation` is done using Blake2b, a cryptographic hash function.  
`Encryption` is done with ChaCha20, a stream cipher.  

### Key Deviration
Two keys are derived from the user provided password, in combination with random generated salts. The salts are called `Salt 1` and `Salt 2`, and the keys are called `Primary Key` and `Secondary Key`, repectively.  
### Validity Check
A cryptographic hash stamp of the content is generated, the function uses the `Secondary Key` with a new salt, `Salt 3`.   
The stamp is appended to the content to be encrypted as a mean to verify that the correct password is provided during decryption (the decryption cipher will output _something_, no mather what password is provided, but its unlikely that the wrong password will also return the correct hash).
### Encryption
The content, along with `Salt 2` and the `Validity Stamp`, are fed to a cipher using the `Primary Key` and a newly generated salt, called `Salt 4`.

## Output File

<!-- ![file_structure](https://user-images.githubusercontent.com/18375194/190555150-82ae4c0f-f44e-4303-892b-5f581d963ee2.svg) -->
![file_structure](/readme_files/file_structure.svg)

The file is saved on disk containing an unencrypted layer with enough information to regenerate the decryption `Primary key` if the user provides the correct password, this layer contains `Salt 1` and `Salt 4`, of 16 and 12 bytes, respectively.  

Once decrypted, the main layer contains `Salt 2`, which is used to generate the `Secondary key`. The `Secondary key` is used in conjunction with `Salt 3`, which is integrated into the `Validity Stamp`, to compare the resulting cryptographic hash of the content with the expected value.

The hashes matching, the contents of the items are reconstructed. Items are arranged contiguously in the decrypted stream, as pairs of utf-8 strings, preceded by their size in bytes.

# Development 
The program consists of three main modules:
- Tulha, which exposes a class to store items.
- Crypto, which contains routines to encrypt and verify data.
- User interface.

Code style is enforced by `autopep8` and `flake8`, which are listed in the `dev_requirements.txt` file.


# Tests
Tests of encryption and storage routines can be performed with:  
`python -m unittest -v`

The tests are also run as a Github action on pull requests.
