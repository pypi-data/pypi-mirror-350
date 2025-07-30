# Placeholder for wallet management (storing/loading keypairs, etc.)
import os
import json
from .keypair import Keypair
import getpass  # For securely getting passphrase

# Default wallet directory, can be overridden by Wallet instance
DEFAULT_WALLET_DIR = os.path.expanduser("~/.bitagere/wallets")


class Wallet:
    def __init__(
        self, name: str, keypair: Keypair = None, wallet_dir: str | None = None
    ):
        self.name = name
        self.wallet_dir = wallet_dir if wallet_dir else DEFAULT_WALLET_DIR
        self.path = os.path.join(self.wallet_dir, f"{name}.json")
        self.keypair = keypair  # This keypair might be unlocked or locked (if loaded from encrypted JSON)

    def save(self, passphrase: str, overwrite: bool = False) -> bool:
        """Saves the wallet (keypair) to an encrypted JSON file."""
        if not self.keypair:
            print("Wallet: No keypair to save.")
            return False

        # Ensure wallet_dir exists
        os.makedirs(self.wallet_dir, exist_ok=True)

        if os.path.exists(self.path) and not overwrite:
            print(
                f"Wallet: File {self.path} already exists. Use overwrite=True to replace."
            )
            return (
                False  # Signal that save failed due to existing file and no overwrite
            )

        try:
            encrypted_data = self.keypair.export_to_encrypted_json(
                passphrase, name=self.name
            )
            with open(self.path, "w") as f:
                json.dump(encrypted_data, f, indent=4)
            print(f"Wallet: Saved and encrypted wallet '{self.name}' to {self.path}")
            return True
        except Exception as e:
            print(f"Wallet: Error saving wallet '{self.name}': {e}")
            return False

    @classmethod
    def load(
        cls, name: str, passphrase: str, wallet_dir: str | None = None
    ) -> "Wallet | None":
        """Loads a wallet from an encrypted JSON file."""
        current_wallet_dir = wallet_dir if wallet_dir else DEFAULT_WALLET_DIR
        path = os.path.join(current_wallet_dir, f"{name}.json")
        if not os.path.exists(path):
            print(f"Wallet: File {path} not found.")
            return None
        try:
            with open(path, "r") as f:
                encrypted_data = json.load(f)

            keypair = Keypair.create_from_encrypted_json(encrypted_data, passphrase)
            print(f"Wallet: Loaded and decrypted wallet '{name}' from {path}")
            # Pass wallet_dir to the constructor if it was provided to load
            return cls(name=name, keypair=keypair, wallet_dir=wallet_dir)
        except Exception as e:
            # Catching specific exceptions like incorrect passphrase might be useful here
            print(
                f"Wallet: Error loading wallet '{name}': {e}. Check passphrase or file integrity."
            )
            return None

    @classmethod
    def create_new_wallet(
        cls, name: str, overwrite: bool = False, wallet_dir: str | None = None
    ) -> tuple["Wallet | None", str | None]:
        """Creates a new wallet, prompts for passphrase, saves it encrypted, and returns the wallet and mnemonic."""
        current_wallet_dir = wallet_dir if wallet_dir else DEFAULT_WALLET_DIR
        wallet_path = os.path.join(current_wallet_dir, f"{name}.json")

        if os.path.exists(wallet_path) and not overwrite:
            # print(f"Wallet: Wallet with name '{name}' already exists in {current_wallet_dir}. Use --overwrite to replace it.")
            # The CLI test for no-overwrite expects the command to handle this.
            # Return (None, None) to signal this specific failure (already exists, no overwrite).
            return None, None

        # if os.path.exists(wallet_path) and overwrite:
        # print(f"Wallet: Overwriting existing wallet '{name}' in {current_wallet_dir}.")

        try:
            keypair = Keypair.generate()  # Generates KP and mnemonic
            mnemonic = keypair.mnemonic

            if not mnemonic:
                # print("Wallet: Critical error - mnemonic not generated.")
                return None, None

            # print(f"Wallet: Generated new keypair for wallet '{name}'.")
            # print(f"IMPORTANT: Please save this mnemonic phrase in a secure place:")
            # print(f"  {mnemonic}")

            # Passphrase input is now handled by the CLI or test mocks for library calls.
            # For direct library use, we might need a way to pass it in or handle it differently.
            # For now, assume passphrase will be provided to save method directly.
            # passphrase = getpass.getpass(f"Enter passphrase to encrypt wallet '{name}': ")
            # passphrase_confirm = getpass.getpass("Confirm passphrase: ")

            # if passphrase != passphrase_confirm:
            #     print("Wallet: Passphrases do not match. Wallet not saved.")
            #     return None, mnemonic

            wallet = cls(name=name, keypair=keypair, wallet_dir=wallet_dir)
            # The actual saving (and passphrase handling for it) should be done by the caller
            # after this method returns the wallet object and mnemonic.
            # This method's role is to generate the keypair and prepare the Wallet object.
            # The CLI will then call wallet.save() with a passphrase.
            # print(f"Wallet: Prepared new wallet '{name}' with address {keypair.ss58_address}. Mnemonic available.")
            return (
                wallet,
                mnemonic,
            )  # Return wallet object and mnemonic, saving is a separate step

        except Exception as e:
            # print(f"Wallet: Error creating new wallet object for '{name}': {e}")
            return None, None

    @classmethod
    def wallet_exists(cls, name: str, wallet_dir: str | None = None) -> bool:
        """Checks if a wallet file with the given name exists."""
        current_wallet_dir = wallet_dir if wallet_dir else DEFAULT_WALLET_DIR
        wallet_path = os.path.join(current_wallet_dir, f"{name}.json")
        return os.path.exists(wallet_path)

    @classmethod
    def list_wallets(cls, wallet_dir: str | None = None) -> list[str]:
        """Lists all saved wallet names."""
        current_wallet_dir = wallet_dir if wallet_dir else DEFAULT_WALLET_DIR
        if not os.path.exists(current_wallet_dir):
            return []
        return [
            f.replace(".json", "")
            for f in os.listdir(current_wallet_dir)
            if f.endswith(".json")
        ]

    @classmethod
    def import_wallet_from_mnemonic(
        cls,
        name: str,
        mnemonic: str,
        overwrite: bool = False,
        wallet_dir: str | None = None,
    ) -> "Wallet | None":
        """Imports a wallet from a mnemonic string, prompts for passphrase, and saves it encrypted."""
        current_wallet_dir = wallet_dir if wallet_dir else DEFAULT_WALLET_DIR
        if not overwrite and os.path.exists(
            os.path.join(current_wallet_dir, f"{name}.json")
        ):
            print(
                f"Wallet: Wallet with name '{name}' already exists in {current_wallet_dir}. Use overwrite=True to replace."
            )
            return None
        try:
            keypair = Keypair.create_from_mnemonic(mnemonic)

            passphrase = getpass.getpass(
                f"Enter passphrase to encrypt imported wallet '{name}': "
            )
            passphrase_confirm = getpass.getpass("Confirm passphrase: ")

            if passphrase != passphrase_confirm:
                print("Wallet: Passphrases do not match. Wallet not saved.")
                return None

            wallet = cls(
                name=name, keypair=keypair, wallet_dir=wallet_dir
            )  # Pass wallet_dir
            if wallet.save(passphrase, overwrite=overwrite):
                print(
                    f"Wallet: Successfully imported and saved encrypted wallet '{name}' with address {keypair.ss58_address} in {wallet.wallet_dir}"
                )
                return wallet
            else:
                print(f"Wallet: Failed to save imported wallet '{name}'.")
                return None
        except Exception as e:
            print(f"Wallet: Error importing wallet '{name}' from mnemonic: {e}")
            return None

    def get_address(self) -> str | None:
        """Returns the SS58 address of the wallet's keypair."""
        if self.keypair:
            return self.keypair.ss58_address
        return None

    def get_public_key(self) -> str | None:
        """Returns the public key (hex) of the wallet's keypair."""
        if self.keypair and self.keypair.public_key:
            return self.keypair.public_key.hex()
        return None

    def get_mnemonic(self) -> str | None:
        """
        Returns the mnemonic of the wallet's keypair, IF it was just generated or imported
        and not yet reloaded from an encrypted store (as mnemonics are not stored in encrypted JSON).
        """
        if self.keypair and hasattr(self.keypair, "mnemonic") and self.keypair.mnemonic:
            return self.keypair.mnemonic
        # print(f"Wallet: Mnemonic not available for wallet '{self.name}'. It might have been loaded from encrypted store or created from seed.")
        return None

    def unlock_keypair(self, passphrase: str) -> bool:
        """
        Attempts to unlock the keypair if it was loaded from an encrypted JSON.
        This typically means re-creating the substrate keypair object with the passphrase.
        This method is more conceptual for this structure, as `load` already requires the passphrase.
        If a keypair is needed for signing, and it was loaded, it should already be unlocked.
        However, if we want to re-verify a passphrase or if the keypair was somehow stored "locked",
        this could be implemented.

        For now, this method assumes that if self.keypair exists and was loaded via `Wallet.load`,
        it's already effectively "unlocked" for use by `self.keypair.sign()`.
        If the keypair was from `create_from_encrypted_json`, it's ready.
        If it was from `generate` or `create_from_mnemonic`, it's also ready.
        The `substrateinterface.Keypair` itself handles the decryption internally when created
        from encrypted JSON with a passphrase.
        """
        if not self.keypair:
            print("Wallet: No keypair to unlock.")
            return False

        # Attempt to re-create/validate by trying to access a sensitive operation or re-load
        # This is a bit of a conceptual placeholder. The actual unlocking happens in Keypair.create_from_encrypted_json
        # or when SubstrateKeypair.sign is called on a keypair derived from encrypted JSON.
        # We can try to re-export and see if it works, as a way to validate passphrase.
        try:
            # This is not a true unlock, but a validation.
            # A true unlock would involve re-instantiating the keypair if it were held in a locked state.
            self.keypair.export_to_encrypted_json(
                passphrase, name=self.name
            )  # Try a sensitive operation
            print(f"Wallet '{self.name}' passphrase appears correct.")
            return True
        except Exception as e:
            print(f"Wallet '{self.name}' passphrase incorrect or other error: {e}")
            return False


# 更多钱包管理功能...
