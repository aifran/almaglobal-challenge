def annualized_rate(short_term_rate, number_of_days):
    """
    :param short_term_rate: the rate calculated for a period of time
    :param number_of_days: the number of days of the period of time
    :return: the annualized rate
    """
    return (1 + short_term_rate) ** (365 / number_of_days) - 1


def implicit_rate(future, spot):
    """
    :param future: The future strike price
    :param spot: the spot price
    :return: The implicit rate
    """
    if future is None or not spot:
        return None
    return future / spot - 1
