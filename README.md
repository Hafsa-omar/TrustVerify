# TrustVerify — File Integrity & Digital Signature CLI Tool

A Python-based Command Line Interface (CLI) tool that allows a Sender to sign 
files and a Receiver to verify their integrity and origin using SHA-256 hashing 
and RSA digital signatures.

> Mini Project I — Information Security Course

**Team Members:**
- Fadumo Jamal Salad — 210208954
- Hafsa Omar Ismail Samatar — 210208735
- Sabreen Elmi Aidarus Gure — 210208856

**Demo Video:** https://youtu.be/IQ7F9aUUM9c


---

## What It Does

TrustVerify has 6 commands:

- `--hash` — Compute the SHA-256 hash of any file
- `--manifest` — Scan a directory and save all hashes to metadata.json
- `--check` — Detect modified, missing, or newly added files
- `--keygen` — Generate an RSA public/private key pair
- `--sign` — Sign metadata.json using the private key
- `--verify` — Verify the signature using the public key

---

## Installation

Make sure Python is installed, then run:

    python -m pip install cryptography

---

## Usage

**Part 1 — Hashing and Integrity**

    python trustverify.py --hash myfiles/report.pdf
    python trustverify.py --manifest ./myfiles
    python trustverify.py --check ./myfiles

**Part 2 — Digital Signatures**

    python trustverify.py --keygen
    python trustverify.py --sign
    python trustverify.py --verify

---

## Demo Workflow

    1. python trustverify.py --manifest ./myfiles   → creates metadata.json
    2. python trustverify.py --keygen               → creates keys
    3. python trustverify.py --sign                 → creates signature.sig
    4. python trustverify.py --verify               → Verification Passed

    # Tamper with metadata.json, then:
    5. python trustverify.py --verify               → Verification Failed

---

## Why Hashing Alone Is Not Enough

Hashing detects whether a file was changed, but it does not prove who sent it.
Anyone can modify a file, re-run the hashing tool, and produce a new metadata.json
with updated hashes. The receiver would have no way to know the files were tampered
with. This is the difference between integrity (file unchanged) and authenticity
(came from the real sender). Hashing alone only provides integrity.

---

## How RSA Ensures Non-Repudiation

RSA uses two linked keys — a Private Key (kept secret by the sender) and a Public
Key (shared openly). The sender signs the SHA-256 hash of metadata.json using their
Private Key, producing a signature.sig file. The receiver then decrypts the signature
using the Public Key and compares it to their own hash of metadata.json. If they
match, the manifest is authentic and untampered.

Since only the Private Key holder can produce a valid signature, a verified signature
mathematically proves the identity of the sender. An attacker cannot forge a signature
without the Private Key — this is what ensures non-repudiation.

---

## Project Structure

    TrustVerify/
    ├── trustverify.py       ← main CLI script
    ├── metadata.json        ← generated manifest
    ├── public_key.pem       ← share with receiver
    ├── signature.sig        ← generated signature
    └── .gitignore           ← excludes private_key.pem

Never share private_key.pem — it must stay secret with the Sender.

---

## Libraries Used

- hashlib — built-in Python library for SHA-256 hashing
- cryptography — for RSA key generation, signing, and verification
- argparse — built-in Python library for CLI interface
- json — built-in Python library for metadata storage

---

## License

This project was developed for educational purposes — Information Security Course.
