# smaj_kyber

`smaj_kyber` is a Python package that wraps the [Kyber](https://pq-crystals.org/kyber/) post-quantum Key Encapsulation Mechanism (KEM) using Python’s `ctypes` and a compiled C shared library.

✅ This implementation is a lightweight wrapper around the **C reference implementation** of Kyber submitted to **NIST** as part of the Post-Quantum Cryptography standardization process.

⚠️ This package is created strictly for **research and educational purposes**. It is not audited or recommended for production use.

---

## Features

- ✅ Bindings to the C reference implementation
- ✅ Support for Kyber512, Kyber768, and Kyber1024
- ✅ No need for C++ or pybind11 — pure `ctypes` usage
- ✅ Easy to switch modes inside Python code
- ✅ Cross platform Linux, Windows , macOS

---

## Usage Example

```python
from smaj_kyber import keygen, encapsulate, decapsulate, set_mode

# Set mode: "512", "768", or "1024"
set_mode("512")

# Bob generates a keypair
pk, sk = keygen()

# Alice uses pk to encapsulate a shared secret
ct, ss1 = encapsulate(pk)

# Bob uses his sk to decapsulate and derive the same shared secret
ss2 = decapsulate(ct, sk)

print("Shared secret 1:", ss1.hex())
print("Shared secret 2:", ss2.hex())
print("Match:", ss1 == ss2)
