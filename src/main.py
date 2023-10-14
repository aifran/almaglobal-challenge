import sys

from src.connection import connect
from src.auth import load_credentials_from_env, ServiceEnum
import pyRofex


def run(watch_products):
    rofex_credentials = load_credentials_from_env(ServiceEnum.ROFEX)

    pyRofex.initialize(
        **rofex_credentials,
        environment=pyRofex.Environment.REMARKET
    )

    available_instruments_response = pyRofex.get_detailed_instruments()

    products = [inst["instrumentId"]["symbol"] for inst in available_instruments_response["instruments"]]

    available_watch_products = [t for t in watch_products if t in products]

    connect(available_watch_products)


if __name__ == "__main__":
    #watch_products = ['GGAL/OCT23', 'DLR/OCT23', 'YPFD/OCT23', 'PAMP/OCT23', 'GGAL/DIC23', 'DLR/DIC23', 'YPFD/DIC23',
    #                  'PAMP/DIC23']
    watch_products = sys.argv[1:]
    run(watch_products)
