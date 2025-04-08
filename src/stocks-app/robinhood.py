import robin_stocks.robinhood as r


def authenticate_robinhood(username, password):
    login = r.login(username, password)
    return login


def fetch_robinhood_holdings():
    holdings = r.account.build_holdings()
    return holdings
