import pyRofex


from src.handlers import market_data_handler, order_report_handler, error_handler, exception_handler


def connect(available_watch_products):

    # websocket connection

    pyRofex.init_websocket_connection(
        market_data_handler=market_data_handler,
        order_report_handler=order_report_handler,
        error_handler=error_handler,
        exception_handler=exception_handler
    )

    # subscription to market data

    entries = [
        pyRofex.MarketDataEntry.BIDS,
        pyRofex.MarketDataEntry.OFFERS,
        pyRofex.MarketDataEntry.LAST
    ]
    pyRofex.market_data_subscription(available_watch_products, entries=entries)

    # subscription to execution reports
    pyRofex.order_report_subscription(snapshot=True)