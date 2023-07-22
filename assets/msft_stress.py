from msft import enterprise_value

cash = 192559
debt = 147075
shares_outstanding = 7435

for i in range(0, 300):
    r = i / 1000
    ev = enterprise_value(r)
    market_cap = ev + cash - debt
    price = market_cap / shares_outstanding
    print(f"r = {r} price per share: {price:.2f}")
