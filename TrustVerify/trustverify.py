

import hashlib
import json
import os
import argparse

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


# --- Part 1: Hashing and Integrity ---

def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read in chunks so large files don't load fully into memory
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def generate_manifest(directory):
    manifest = {}

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            manifest[filename] = hash_file(filepath)
            print(f"  [+] {filename}  ->  {manifest[filename][:16]}...")

    with open("metadata.json", "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"\n  Saved metadata.json ({len(manifest)} files)")


def check_integrity(directory):
    if not os.path.exists("metadata.json"):
        print("  Error: metadata.json not found. Run --manifest first.")
        return

    with open("metadata.json", "r") as f:
        saved = json.load(f)

    all_ok = True

    for filename, saved_hash in saved.items():
        filepath = os.path.join(directory, filename)

        if not os.path.exists(filepath):
            print(f"  MISSING  : {filename}")
            all_ok = False
            continue

        if hash_file(filepath) == saved_hash:
            print(f"  OK       : {filename}")
        else:
            print(f"  MODIFIED : {filename}")
            all_ok = False

    print()
    if all_ok:
        print("  All files intact.")
    else:
        print("  Warning: some files were modified or are missing.")


# --- Part 2: RSA Keys and Signatures ---

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("  private_key.pem  ->  keep this secret")
    print("  public_key.pem   ->  share with the receiver")


def sign_manifest():
    if not os.path.exists("metadata.json"):
        print("  Error: metadata.json not found. Run --manifest first.")
        return
    if not os.path.exists("private_key.pem"):
        print("  Error: private_key.pem not found. Run --keygen first.")
        return

    manifest_hash = hash_file("metadata.json")

    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )

    # RSA signs the hash of the file, not the file itself
    signature = private_key.sign(
        manifest_hash.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    with open("signature.sig", "wb") as f:
        f.write(signature)

    print("  Signature saved to signature.sig")
    print("  Send to receiver: metadata.json + signature.sig + public_key.pem")


def verify_signature():
    for fname in ["metadata.json", "signature.sig", "public_key.pem"]:
        if not os.path.exists(fname):
            print(f"  Error: {fname} not found.")
            return

    current_hash = hash_file("metadata.json")

    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

    with open("signature.sig", "rb") as f:
        signature = f.read()

    try:
        public_key.verify(
            signature,
            current_hash.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("  Verification passed. Manifest is authentic.")

    except Exception:
        # verify() raises an exception if the signature does not match
        print("  Verification failed. Manifest may have been tampered with.")


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        prog="TrustVerify",
        description="File integrity and digital signature tool"
    )

    parser.add_argument("--hash",     metavar="FILE",      help="Hash a single file")
    parser.add_argument("--manifest", metavar="DIRECTORY", help="Generate metadata.json for a directory")
    parser.add_argument("--check",    metavar="DIRECTORY", help="Check files against metadata.json")
    parser.add_argument("--keygen",   action="store_true", help="Generate RSA key pair")
    parser.add_argument("--sign",     action="store_true", help="Sign metadata.json with private key")
    parser.add_argument("--verify",   action="store_true", help="Verify signature using public key")

    args = parser.parse_args()

    if args.hash:
        if not os.path.exists(args.hash):
            print(f"  File not found: {args.hash}")
        else:
            print(f"  SHA-256: {hash_file(args.hash)}")

    elif args.manifest:
        if not os.path.isdir(args.manifest):
            print(f"  Directory not found: {args.manifest}")
        else:
            generate_manifest(args.manifest)

    elif args.check:
        if not os.path.isdir(args.check):
            print(f"  Directory not found: {args.check}")
        else:
            check_integrity(args.check)

    elif args.keygen:
        generate_keys()

    elif args.sign:
        sign_manifest()

    elif args.verify:
        verify_signature()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
