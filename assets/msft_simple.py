def discounted_cashflow(cash_flow, discount_rate, n):
    return cash_flow / (1 + discount_rate) ** n


def net_income(revenue, gross_margin, operating_expenses, tax_rate):
    operating_income = revenue * gross_margin - operating_expenses
    return operating_income * (1 - tax_rate)


cash = 192559  # in millions
debt = 147075

cloud_growth = 0.25
other_growth = 0.15
discount_rate = 0.095

cloud_revenue = 75251
other_revenue = 123019
gross_margin = 0.68
operating_expenses = 52237
tax_rate = 0.13
enterprise_value = 0

# up to year n = 2
for n in range(1, 3):
    cloud_revenue *= 1 + cloud_growth
    other_revenue *= 1 + other_growth
    cashflow = net_income(
        cloud_revenue + other_revenue, gross_margin, operating_expenses, tax_rate
    )
    enterprise_value += discounted_cashflow(cashflow, discount_rate, n)


# from year n = 3 to n = 10
cloud_growth = 0.15
other_growth = 0.15
for n in range(3, 11):
    other_growth -= 0.02
    cloud_revenue *= 1 + cloud_growth
    other_revenue *= 1 + other_growth
    cashflow = net_income(
        cloud_revenue + other_revenue, gross_margin, operating_expenses, tax_rate
    )
    enterprise_value += discounted_cashflow(cashflow, discount_rate, n)

print("Enterprise value (mm): {:,.0f}".format(enterprise_value))
market_cap = enterprise_value + cash - debt
print("Market cap (mm): {:,.0f}".format(market_cap))
shares_outstanding = 7435
print("Price per share: {:.2f}".format(market_cap / shares_outstanding))
