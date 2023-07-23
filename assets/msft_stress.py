import numpy as np

from msft_simple import (
    DISCOUNT_RATE,
    discounted_cashflow,
    net_income,
    other_growth_rate,
)


def cloud_growth_rate(n, r):
    if n < 3:
        return 0.25
    elif n > 10:
        return 0.01
    else:
        return np.random.normal(r, 0.02)


def gross_margin():
    return np.random.normal(0.68, 0.01)


def operating_expenses_growth_rate():
    return np.random.normal(0.02, 0.01)


def enterprise_value(r):
    cloud_revenue = 75251
    other_revenue = 123019
    operating_expenses = 52237
    tax_rate = 0.13
    enterprise_value = 0

    for n in range(1, 50):
        cloud_revenue *= 1 + cloud_growth_rate(n, r)
        other_revenue *= 1 + other_growth_rate(n)
        operating_expenses *= 1 + operating_expenses_growth_rate()
        cashflow = net_income(
            cloud_revenue + other_revenue, gross_margin(), operating_expenses, tax_rate
        )
        enterprise_value += discounted_cashflow(cashflow, DISCOUNT_RATE, n)

    return enterprise_value


if __name__ == "__main__":
    cash = 192559
    debt = 147075
    shares_outstanding = 7435
    r = 0.15
    ev = enterprise_value(r)

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
