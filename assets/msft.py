def discounted_cashflow(cash_flow, discount_rate, n):
    return cash_flow / (1 + discount_rate) ** n


cash = 192559  # in millions
debt = 147075

product_growth = 0.01
service_growth = 0.29
discount_rate = 0.095

product_revenue = 72732
service_revenue = 125538

operating_expenses = 50000
taxes = 10000
enterprise_value = 0

# up to year n = 2
for n in range(1, 3):
    product_revenue *= 1 + product_growth
    service_revenue *= 1 + service_growth
    net_income = (product_revenue + service_revenue) - (operating_expenses + taxes)
    enterprise_value += discounted_cashflow(net_income, discount_rate, n)

# from year n = 3 to n = 10
product_growth = -0.01
service_growth = 0.15  # we'll stress test this later
for n in range(3, 11):
    product_revenue *= 1 + product_growth
    service_revenue *= 1 + service_growth
    net_income = (product_revenue + service_revenue) - (operating_expenses + taxes)
    enterprise_value += discounted_cashflow(net_income, discount_rate, n)

print("Enterprise value (mm): {:,.0f}".format(enterprise_value))
market_cap = enterprise_value + cash - debt
print("Market cap (mm): {:,.0f}".format(market_cap))
shares_outstanding = 7435
print("Price per share: {:.2f}".format(market_cap / shares_outstanding))
