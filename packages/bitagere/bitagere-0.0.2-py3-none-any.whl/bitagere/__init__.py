# bitagere SDK
__version__ = "0.0.2"

# Import main modules for library use
from . import substrate
from . import wallet

# Import main classes for convenience
from .substrate import AgereInterface
from .wallet import Wallet, Keypair

__all__ = ["substrate", "wallet", "AgereInterface", "Wallet", "Keypair", "__version__"]
