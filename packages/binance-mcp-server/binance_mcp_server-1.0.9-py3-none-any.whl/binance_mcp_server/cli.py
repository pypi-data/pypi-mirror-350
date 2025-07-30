import os
import typer
from dotenv import load_dotenv
from binance_mcp_server import mcp


app = typer.Typer(add_completion=True)


@app.command()
def binance_mcp_server(
        api_key = typer.Option("", "--api-key", "-k", help="Binance API key", prompt=True, envvar="BINANCE_API_KEY"),
        api_secret = typer.Option("", "--api-secret", "-s", help="Binance API secret", prompt=True, envvar="BINANCE_API_SECRET"),
        binance_testnet = typer.Option(False, "--binance-testnet", "-t", help="Use Binance testnet", envvar="BINANCE_TESTNET")
    ):
    load_dotenv()

    os.environ["api_key"] = str(api_key)
    os.environ["api_secret"] = api_secret
    os.environ["binance_testnet"] = str(binance_testnet).lower()

    mcp.run(transport="stdio")


if __name__ == "__main__":
    app()