# TrustVerify — File Integrity & Digital Signature CLI Tool

A Python-based Command Line Interface (CLI) tool that allows a **Sender** to sign files and a **Receiver** to verify their integrity and origin using **SHA-256 hashing** and **RSA digital signatures**.

>  Mini Project I — Information Security Course

---

##  Team Members

| Name | Student ID |
|------|-----------|
| Fadumo Jamal Salad | 210208954 |
| Hafsa Omar Ismail Samatar | 210208735 |
| Sabreen Elmi Aidarus Gure | 210208860 |

---

##  Features

| Command | Description |
|---------|-------------|
| `--hash` | Generate SHA-256 hash for any file |
| `--manifest` | Scan a directory and create `metadata.json` |
| `--check` | Detect unauthorized file modifications |
| `--keygen` | Generate RSA public/private key pair |
| `--sign` | Sign `metadata.json` using private key |
| `--verify` | Verify signature using public key |

---

##  Installation

**1. Make sure Python is installed:**
```bash
python --version
```

**2. Install the required library:**
```bash
python -m pip install cryptography
```

---

##  Usage

### Part 1 — Hashing & Integrity
```bash
# Hash a single file
python trustverify.py --hash myfiles/report.pdf

# Generate manifest (scan all files in a folder)
python trustverify.py --manifest ./myfiles

# Check files for tampering
python trustverify.py --check ./myfiles
```

### Part 2 — Digital Signatures
```bash
# Generate RSA key pair
python trustverify.py --keygen

# Sign the manifest (Sender)
python trustverify.py --sign

# Verify the signature (Receiver)
python trustverify.py --verify
```

---

##  Demo Workflow
```
1. python trustverify.py --manifest ./myfiles   → creates metadata.json
2. python trustverify.py --keygen               → creates keys
3. python trustverify.py --sign                 → creates signature.sig
4. python trustverify.py --verify               →  VERIFICATION PASSED

# Tamper with metadata.json, then:
5. python trustverify.py --verify               → VERIFICATION FAILED
```

---

##  Project Structure
```
TrustVerify/
│
├── trustverify.py       ← main CLI script
├── metadata.json        ← generated manifest
├── public_key.pem       ← share with receiver
├── signature.sig        ← generated signature
└── .gitignore           ← excludes private_key.pem
```

>  **Never share `private_key.pem`** — it must stay secret with the Sender.

---

##  Libraries Used

- `hashlib` — built-in Python library for SHA-256 hashing
- `cryptography` — for RSA key generation, signing, and verification
- `argparse` — built-in Python library for CLI interface
- `json` — built-in Python library for metadata storage

---

##  Key Concepts

**Why hashing alone is not enough:**
> A hash proves a file has not changed (integrity), but it cannot prove *who* created it. Anyone can modify a file and re-hash it to cover their tracks.

**How RSA ensures non-repudiation:**
> Only the Sender holds the private key. If the public key successfully verifies the signature, it mathematically proves the Sender signed it — and they cannot deny it.

---

## Demo Video

A 2–5 minute walkthrough covering:
- Running the full sign and verify workflow
- Deliberately tampering with `metadata.json` to trigger **Verification Failed**
- Explanation of why hashing provides integrity but not authenticity

🎥 [Watch on YouTube](PASTE_YOUR_LINK_HERE)

---

## License

This project was developed for educational purposes — Information Security Course.
