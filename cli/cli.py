import argparse
import logging
from rich import print
import run
import typer

app = typer.Typer()


def setup_logging(verbose: bool):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


@app.command()
def test():
    print("Hello, World!")


@app.command()
def get_related(
    username: str = typer.Argument(help="Username of the account to scrape"),
    verbose: bool = False,
):
    # Set up logging
    setup_logging(verbose)
    print(
        f"""Running CLI with the following arguments"
    username:       '{username}'
    """
    )
    run.scrape_user_data(username=username)


@app.command()
def get_similar(
    # basic info
    username: str = typer.Argument(help="Username of the account to browse"),
    target_user: str = typer.Argument(help="Username of the account to browse"),
    # optional info for min and max followers
    min_followers: int = typer.Option(default=None, help="Minimum number of followers"),
    max_followers: int = typer.Option(default=None, help="Maximum number of followers"),
    verbose: bool = False,
):
    # Set up logging
    setup_logging(verbose)

    # Tell user to login before running this script
    print(
        f""" Before you run this script, make sure you have already run the following commands in the terminal:
    1. 'instaloader --login [username]' (Write username you used to Confirm)
    """
    )

    print(
        f"""Running CLI with the following arguments"
    username:       '{username}'
    target_user:    '{target_user}'
    min_followers:  {min_followers}
    max_followers:  {max_followers}
    """
    )

    # Run the CLI
    run.similar_account(
        username=username,
        target_user=target_user,
        min_followers=min_followers,
        max_followers=max_followers,
    )


if __name__ == "__main__":
    app()
