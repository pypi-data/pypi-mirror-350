import ctypes
import os
import platform

# ----------------------------
# Configuration
# ----------------------------

# Default Kyber mode (can be changed at runtime)
KYBER_MODE = "768"

# Map platform to shared library file extensions
EXTENSIONS = {
    "Darwin": ".dylib",  # macOS
    "Linux": ".so",  # Linux
    "Windows": ".dll"  # Windows
}

# Map architecture for Linux dynamic file naming
ARCH_SUFFIXES = {
    "x86_64": "x86_64",
    "arm64": "arm64",
    "aarch64": "arm64",
    "armv7l": "armv7"
}

# Kyber mode config: (PK_LEN, SK_LEN, CT_LEN, SS_LEN)
MODE_PARAMS = {
    "512": (800, 1632, 768, 32),
    "768": (1184, 2400, 1088, 32),
    "1024": (1568, 3168, 1568, 32)
}

# ----------------------------
# System Detection
# ----------------------------

SYSTEM = platform.system()
ARCH = platform.machine()

if SYSTEM not in EXTENSIONS:
    raise RuntimeError(f"Unsupported operating system: {SYSTEM}")

LIB_EXT = EXTENSIONS[SYSTEM]


# ----------------------------
# Library Resolver
# ----------------------------

def get_lib_filename(base: str) -> str:
    """Get the correct library filename based on OS and architecture."""
    if SYSTEM == "Darwin":
        return f"{base}_universal.dylib"
    elif SYSTEM == "Linux":
        if ARCH not in ARCH_SUFFIXES:
            raise RuntimeError(f"Unsupported Linux architecture: {ARCH}")
        suffix = ARCH_SUFFIXES[ARCH]
        return f"{base}_{suffix}.so"
    elif SYSTEM == "Windows":
        return f"{base}.dll"
    else:
        raise RuntimeError(f"Unsupported platform: {SYSTEM}")


# ----------------------------
# Global State
# ----------------------------

PK_LEN, SK_LEN, CT_LEN, SS_LEN = MODE_PARAMS[KYBER_MODE]
libname = get_lib_filename(f"libkyber{KYBER_MODE}")
LIB_PATH = os.path.join(os.path.dirname(__file__), "lib", libname)

if not os.path.exists(LIB_PATH):
    raise FileNotFoundError(f"Library not found: {LIB_PATH}")

lib = ctypes.CDLL(LIB_PATH)
Uint8Array = ctypes.POINTER(ctypes.c_ubyte)

# Function signatures
lib.keypair.argtypes = [Uint8Array, Uint8Array]
lib.encapsulate.argtypes = [Uint8Array, Uint8Array, Uint8Array]
lib.decapsulate.argtypes = [Uint8Array, Uint8Array, Uint8Array]


# ----------------------------
# Public API
# ----------------------------

def set_mode(mode: str):
    """Change Kyber mode at runtime. Use '512', '768', or '1024'."""
    global PK_LEN, SK_LEN, CT_LEN, SS_LEN, libname, lib, LIB_PATH

    if mode not in MODE_PARAMS:
        raise ValueError("Invalid mode. Choose '512', '768', or '1024'.")

    PK_LEN, SK_LEN, CT_LEN, SS_LEN = MODE_PARAMS[mode]
    libname = get_lib_filename(f"libkyber{mode}")
    LIB_PATH = os.path.join(os.path.dirname(__file__), "lib", libname)

    if not os.path.exists(LIB_PATH):
        raise FileNotFoundError(f"Library not found: {LIB_PATH}")

    lib = ctypes.CDLL(LIB_PATH)

    lib.keypair.argtypes = [Uint8Array, Uint8Array]
    lib.encapsulate.argtypes = [Uint8Array, Uint8Array, Uint8Array]
    lib.decapsulate.argtypes = [Uint8Array, Uint8Array, Uint8Array]


def keygen():
    pk = (ctypes.c_ubyte * PK_LEN)()
    sk = (ctypes.c_ubyte * SK_LEN)()
    lib.keypair(pk, sk)
    return bytes(pk), bytes(sk)


def encapsulate(pk: bytes):
    assert len(pk) == PK_LEN
    pk_buf = (ctypes.c_ubyte * PK_LEN).from_buffer_copy(pk)
    ct = (ctypes.c_ubyte * CT_LEN)()
    ss = (ctypes.c_ubyte * SS_LEN)()
    lib.encapsulate(pk_buf, ct, ss)
    return bytes(ct), bytes(ss)


def decapsulate(ct: bytes, sk: bytes):
    assert len(ct) == CT_LEN
    assert len(sk) == SK_LEN
    ct_buf = (ctypes.c_ubyte * CT_LEN).from_buffer_copy(ct)
    sk_buf = (ctypes.c_ubyte * SK_LEN).from_buffer_copy(sk)
    ss = (ctypes.c_ubyte * SS_LEN)()
    lib.decapsulate(ct_buf, sk_buf, ss)
    return bytes(ss)
