RANDOMNESS = True

if RANDOMNESS:
    import numpy as np


def discounted_cashflow(cash_flow, discount_rate, n):
    return cash_flow / (1 + discount_rate) ** n


def net_income(revenue, gross_margin, operating_expenses, tax_rate):
    operating_income = revenue * gross_margin - operating_expenses
    return operating_income * (1 - tax_rate)


def service_growth_rate(n, r=None):
    if n < 3:
        return 0.29
    else:
        if RANDOMNESS:
            return np.random.normal(r, 0.02)
        else:
            return 0.15


def gross_margin():
    if RANDOMNESS:
        return np.random.normal(0.68, 0.01)
    else:
        return 0.68


def operating_expenses_growth_rate():
    if RANDOMNESS:
        return np.random.normal(0.02, 0.01)
    else:
        return 0.0


def enterprise_value(r):
    product_growth = 0.01
    discount_rate = 0.095

    product_revenue = 72732  # millions
    service_revenue = 125538
    operating_expenses = 50000
    tax_rate = 0.13
    enterprise_value = 0

    # up to year n = 2
    for n in range(1, 3):
        product_revenue *= 1 + product_growth
        service_revenue *= 1 + service_growth_rate(n, r)
        operating_expenses *= 1 + operating_expenses_growth_rate()
        cashflow = net_income(
            product_revenue + service_revenue,
            gross_margin(),
            operating_expenses,
            tax_rate,
        )
        enterprise_value += discounted_cashflow(cashflow, discount_rate, n)

    # from year n = 3 to n = 10
    product_growth = -0.01
    for n in range(3, 11):
        product_revenue *= 1 + product_growth
        service_revenue *= 1 + service_growth_rate(n, r)
        operating_expenses *= 1 + operating_expenses_growth_rate()
        cashflow = net_income(
            product_revenue + service_revenue,
            gross_margin(),
            operating_expenses,
            tax_rate,
        )
        enterprise_value += discounted_cashflow(cashflow, discount_rate, n)
    return enterprise_value


cash = 192559
debt = 147075
r = 0.15
ev = enterprise_value(0.15)

print("Enterprise value (mm): {:,.0f}".format(ev))
market_cap = ev + cash - debt
print("Market cap (mm): {:,.0f}".format(market_cap))
shares_outstanding = 7435
print("Price per share: {:.2f}".format(market_cap / shares_outstanding))
