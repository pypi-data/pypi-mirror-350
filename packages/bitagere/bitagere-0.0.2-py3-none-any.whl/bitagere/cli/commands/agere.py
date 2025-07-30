import click
import json
from bitagere.substrate.interface import AgereInterface
import getpass

NETWORK_URLS = {
    "local": "ws://127.0.0.1:9944",
    "signet": "wss://signet.bevm.io/ws",
    # "mainnet": "wss://your-mainnet-node.com/ws", # Example for future mainnet
}


# Helper functions for colored output
def print_success(message):
    click.echo(click.style(message, fg="green"))


def print_error(message):
    click.echo(click.style(message, fg="red"))


def print_info(message):
    click.echo(click.style(message, fg="blue"))  # Or 'yellow' or 'cyan'


def _resolve_node_url(network_name: str, custom_url: str = None) -> str:
    if custom_url:
        print_info(f"Using custom node URL: {custom_url}")
        return custom_url

    url = NETWORK_URLS.get(network_name)
    if not url:
        # Should not happen if click.Choice is used correctly, but as a safeguard:
        print_error(f"Unknown network: {network_name}. Defaulting to 'local'.")
        return NETWORK_URLS["local"]

    print_info(f"Using '{network_name}' network URL: {url}")
    return url


def _get_passphrase(passphrase: str = None) -> str:
    if not passphrase:
        try:
            passphrase = getpass.getpass("Enter passphrase for wallet: ")
        except Exception as e:
            print_error(f"Failed to get passphrase: {e}")
            raise click.Abort()
    return passphrase


@click.group("agere")
def agere_cmds():
    """Placeholder for Agere-specific commands. Currently, all subcommands have been moved."""
    # If in the future, Agere-specific commands are added (e.g., interacting with a unique Agere pallet),
    # they would be defined here.
    # For now, this group might appear empty or show a help message indicating that
    # common operations like transfer, balance, etc., are now top-level.
    print_info(
        "Agere-specific commands will be listed here. Common operations are now top-level."
    )
    pass


# To keep the `agere` command group in `main.py` functional without errors if no subcommands are added here yet:
# You could add a simple placeholder command or ensure the group itself provides useful help.
@agere_cmds.command("info")
def agere_info():
    """Displays information about the Agere module or its CLI group."""
    click.echo("This is the command group for Agere-specific interactions.")
    click.echo(
        "General commands like transfer, balance, submit-extrinsic, chain-info, etc., have been moved to the top level or other groups."
    )
    click.echo(
        "Future commands specific to unique Agere pallet functionalities will be added here."
    )


if __name__ == "__main__":
    agere_cmds()
