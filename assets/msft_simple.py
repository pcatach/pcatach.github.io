DISCOUNT_RATE = 0.095


def discounted_cashflow(cash_flow, discount_rate, n):
    return cash_flow / (1 + discount_rate) ** n


def net_income(revenue, gross_margin, operating_expenses, tax_rate):
    operating_income = revenue * gross_margin - operating_expenses
    return operating_income * (1 - tax_rate)


def cloud_growth_rate(n, r):
    if n < 3:
        return 0.25
    elif n > 10:
        return 0.01
    else:
        return r


def other_growth_rate(n):
    if n < 3:
        return 0.15
    else:
        return 0.15 - 0.02 * (n - 2)


def gross_margin():
    return 0.68


def operating_expenses_growth_rate():
    return 0.0


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

    print("Enterprise value (mm): {:,.0f}".format(ev))
    market_cap = ev + cash - debt
    print("Market cap (mm): {:,.0f}".format(market_cap))
    print("Price per share: {:.2f}".format(market_cap / shares_outstanding))
