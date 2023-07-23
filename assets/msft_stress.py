from msft import enterprise_value

cash = 192559
debt = 147075
shares_outstanding = 7435

print("| r | price per share |")
print("|---|-----------------|")
for i in range(0, 500, 50):
    r = i / 1000
    prices = []
    for _ in range(100):
        ev = enterprise_value(r)
        market_cap = ev + cash - debt
        price = market_cap / shares_outstanding
        prices.append(price)
    price = sum(prices) / len(prices)
    print("| {:.2f} | {:.2f} |".format(r, price))
