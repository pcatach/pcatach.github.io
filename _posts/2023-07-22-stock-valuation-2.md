---
layout: post
title:  "Stock valuation from first principles (part 2)"
date:   2023-07-22 14:00:00 +0000
categories: social-science
---

_(disclaimer: I'm not a financial advisor, this is not financial advice, I'm not responsible for any losses you may incur, etc.)_

In my previous post ([Stock valuation from first principles](./2023-05-03-stock-valuation.md)) I talked about CAPM and how it can be used to compute discount rates, and arrived at a discount rate of 9.5% for Microsoft.
I also mentioned DCF, which says that the enterprise value of an asset is the sum of the present value of all future cash flows.
I used these models to estimate the value of Microsoft shares in a very simplistic way and arrived at a value of $172 per share (or a $1,279 bn market cap).

In this post I will try to improve on that valuation, particularly looking at the earnings, growth rate and terminal value assumptions.
For that, we'll look into the financial statements of Microsoft.
Instead of coming up with a single number, I will try to model the uncertainty of the valuation and present a range of forecasts.

## Balance sheet

Last time I hand-waved the fact that the enterprise value is the market cap plus net liabilities:

```
enterprise_value = market_cap - cash + debt
```

you can think of it as the cost to take over the firm: you would need to pay for all the shares and also pay off all the debt, but you would get all the cash in the balance sheet.

We can find these values looking at Microsoft's balance sheet, which can be found in the SEC (Securities and Exchange Commission) website.
You can go ahead and open [the SEC website](https://www.sec.gov/edgar/searchedgar/companysearch) and search for Microsoft. 

Open the latest report, which will either be a 10-K (annual report) or a 10-Q (quarterly report).
Today (July 2023) the latest report is the 10-Q for the quarter ending on March 31, 2023 (Q3).
Scroll down to the "Balance Sheets" section and you'll see something like this (with values in millions of dollars):

|                                        | Q3 23  | Q4 22  |
| ---                                    | ---:    | ---:    |
| **Assets**                             |        |        |
| Cash and cash equivalents              | 26,562 | 13,932 |
| Short-term investments                 | 77,865 | 90,826 |
| Accounts receivable                    | 37,420 | 44,261 |
| Inventory                              |  2,877 |  3,742 |
| Other current assets                   | 19,265 | 16,964 |
| Property, plant and equipment (PP&E)   | 88,132 | 74,398 |
| Lease assets                           | 13,879 | 13,148 |
| Equity and other investments           |  9,415 |  6,891 |
| Goodwill                               | 67,940 | 67,524 |
| Intangible assets                      |  9,879 | 11,298 |
| Other long-term assets                 | 26,954 | 21,897 |
| **Liabilities**                        |        |        |
| Accounts payable                       | 15,305 | 19,000 |
| Accrued compensation                   | 10,411 |  2,749 |
| Short-term liabilities                 | 47,311 | 52,354 |
| Other current liabilities              | 12,664 | 13,067 |
| Long-term liabilities                  | 69,663 | 75,971 |
| Lease liabilities                      | 12,312 | 11,489 |
| Other long-term liabilities            | 17,437 | 15,526 |
| ---                                    | ---    | ---    |

I highly recommend filling out this table by hand.
It will give you a sense of the company that is difficult to get by just copying and pasting numbers.

**Assets** are things that the company owns, **liabilities** are things that the company owes.
The difference between the two is **equity**, which is the value of the company - what shareholders would get back if the company was sold.

To compute the enterprise value, we need to know what's cash, and what's debt.
"Cash" is any asset that the company can relatively quickly sell ("liquidate", as they like to say) and get cash in return.
Making this choice is a bit of an art, and I'm sure a lot of people would disagree with me, but here's what I would consider as cash:

- Cash and cash equivalents (duh)
- Short-term investments (in the 10-Q they say that these are "investments with original maturities of greater than three months and remaining maturities of less than one year")
- PP&E (I'm assuming that Microsoft could sell these assets and get cash in return, these are offices, data centers, computer and networking equipment, etc.)

What I'm not including: accounts receivable, inventory, other current assets, lease assets, equity and other investments, goodwill, intangible assets, other long-term assets. Fight me.

This gives us a total of $192,559 million in cash on Q3 2023. This is up from $179,156 million in Q4 2022.
Their cash and equivalents increased by $10 bn and short-term investments decreased by $13 bn, at the same time their PP&E increased by $13 bn.
They could have used this cash to pay for some of their debt, but we'll shortly see that their debt didn't change much.
But it's plausible that they liquidated some of their short-term investments and used that to buy more property and equipment.

"Debt" is any short-term or long-term liability, excluding accounts payable, accrued compensation and lease liability (like data center leases).
That's because these are liabilities required for Microsoft to operate, and they are not really debts.
It's worth noting that Microsoft has $15 bn in accounts payable.
How impressive is it that they have $15 bn in unpaid bills?
You got to have a lot of credit with your sppliers to do that.

All debt adds up to $147,075 million in Q3 2023, very close to $156,918 million in Q4 2022.

This give us:

```
net_liabilities = 147,075 - 192,559 = -45,484
```

which can be added to the market cap (today) of `$343.77 per share * 7,435 million shares = $2,556,097 billion` to get the enterprise value:

```
enterprise_value = 2,556,097 + 45,484 = 2,601,581
```

We can summarise this in a table:

|                          | Q3 23     |
| ---                      | ---:       |
| Market cap (mm $)        | 2,556,097 |
| Cash (mm $)              |   192,559 |
| Debt (mm $)              |   147,075 |
| Enterprise value (mm $)  | 2,601,581 |
| Shares outstanding (mm)  |     7,435 |
| Price per share ($)      |    343.77 |

## Income statement

This gives us a sense of what the market thinks Microsoft is worth.
But to build our own valuation model, we need to look at the income statement.
For this, we'll go instead to the 10-K report so we can see the full year.
The income statement it will look something like this:

|                                        |   2022  |   2021  |
| ---                                    |  ---:    |  ---:    |
| **Revenue**                            |         |         |
| Productivity and Business Processes    |  63,364 |  53,915 |
| Intelligent Cloud                      |  75,251 |  60,080 |
| More Personal Computing                |  59,655 |  54,093 |
| **Cost of revenue**                    |         |         |
| Product                                |  19,064 |  18,219 |
| Service                                |  43,586 |  34,013 |
| **Gross margin**                       | 135,620 | 115,856 |
| Research and development (R&D)         |  24,512 |  20,716 |
| Sales and marketing (S&M)              |  21,825 |  20,117 |
| General and administrative (G&A)       |   5,900 |   5,107 |
| **Operating income**                   |  83,383 |  69,916 |
| Taxes and other expenses               |  10,645 |   8,645 |
| **Net income**                         |  72,738 |  61.271 |

I broke the revenue down into 3 segments: 

- Productivity and Business Processes (Office, LinkedIn)
- Intelligent Cloud (Azure)
- More Personal Computing (Windows, Xbox, Surface)

Some things jump to the eye: the gross margin, which is the difference between revenue and cost of revenue, is 68% of revenue.
High gross margins like this are typical of software companies - the cost of producing one more copy of a software is very low.
It's also worth noting that most of the revenue growth comes from services like Office 365 and Azure, not Windows licenses.
This has been a trend for a while.

The operating margins are also very high at 42% of revenue and net income is 37% of revenue.
Microsoft pays $4 bn in taxes, which is a 13% tax rate, compared to an average of 25% in the US.
They do have a significant part of their business outside of the US though.

It's also notable how the cloud sector revenue has grown by 25% in 2022 and net income by 19%.

## Cash flow statement

The point of this exercise was to arrive at the net income, understand how it was generated and how it could grow in the future.
But the net income is not the same as the cash that Microsoft has in the bank.

To match that up (or "reconcile" as they say), we need to look at the cash flow statement.
It's a bit more complicated, but here is what a summary would look like:

|                                         |   2022  |
| ---                                     |  ---:    |
| **Cash flows from operating activities**|         |
| Net income                              |  72,738 |
| Depreciation and amortization (D&A)     |  14,460 |
| Stock-based compensation                |   7,502 |
| Net changes in assets                   | (5,665) |
| Cashflow from operations                |  89,035 |
| **Cash flows from investing activities**|         |
| Debt repayments                         | (9,023) |
| Net stock repurchases                   | (30,855)|
| Dividends paid                          | (18,135)|
| Other                                   |    (863)|
| Cashflow from investing                 | (58,876)|
| **Cash flows from financing activities**|         |
| PP&E purchases                          | (23,886)|
| Acquisitions                            | (22,038)|
| Sales of investments                    |  15,613 |
| Cashflow from financing                 | (30,311)|
| Foreign exchange rate changes           |   (141) |
| **Net cash**                            |   (293) |

This all means that, despite it's incredible net income, Microsoft actually lost $293 million in cash in 2022.

Indeed, if you look at the 10-K balance sheet, you'll see that cash and cash equivalents decreased from $14,224 billion in 2021 to $13,931 billion in 2022, which is very close to the amount we saw in the 10-Q balance sheet for 2023.

Right, so a net loss of 293.
Let's break this down. 
We understand the $72 bn in net income.
We can see a D&A gain of $14 bn.

What does this mean?
If I buy some equipment today worth $100, I'll deduct $100 from my balance sheet cash and add $100 to my balance sheet PP&E.
Now do I have a $100 asset in my balance sheet forever?
No, because this equipment will lose value over time.
Let's say that it loses $10 of value every year, so that in 10 years it's worth $0.
In the first year, I'll add a $10 expense to my income statement as an operating expense (perhaps under G&A or cost of revenue).
I keep adding this $10 expense every year for 10 years.
But if I look at the my actual bank account, I don't see this $10 expense.
So I add it back to my operating cash flow.
(Note: I have to pay taxes on my operating income, not on my operating cash flow).

In the case of Microsoft, their operating expense includes $14 bn in D&A that is added back in the cashflow statement to reconcile the net income with the cashflow from operations.
This is the actual cash that Microsoft generated from its operations.

Any further expenses like debt repayments, stock buybacks, capital expenditures (PP&E purchases) and company acquisitions are deducted from the cashflow from operations to arrive at the net cashflow - this is the quantity that gets added to "cash and cash equivalents" in the balance sheet.

## Forecasting

Now, from the point of view of valuation, I don't really care about all this reconciliation.
Some people would use cash flow from operations in DCF.
But a company's spending on PP&E, acquisitions, stock buybacks, etc. are all decisions that subtract from its income but at least in theory should feed into future growth.
So for the purposes of forecasting, I'll just look at the net income and not worry about the cashflow statement.

The question we have to ask is: how much will this grow in the future?
19% is a very high growth rate, but where is it coming from?
On their [2023 Q3 press release](https://www.microsoft.com/en-us/investor/earnings/FY-2023-Q3/press-release-webcast), Microsoft said that their cloud reveneue grew 22% year-over-year for that quarter ($28.5 bn), citing the innovations in AI and being the "platform of choice" for customers in this space.

In my model, I'll assume that Microsoft's cloud/AI revenue will continue to grow at 25% year-ver-year for the next 2 years, and then slow down to 15% for the following 8 years (let's say competition catches up).
We'll stress test this number later.

For the other sectors (Office, Windows, Xbox, etc.), I'll assume that the growth will continue at around 15% for the next 2 years and then decline year after year until it reaches -1% on year 10 (let's say Microsoft will stop investing in these products and fully focus on AI and infrastructure).

Here are my assumptions:

| cloud segment growth | 25% for 2 years, 15% from year 3 and a maturity of 1%|
| other segment growth | 15% for 2 years, down to -1 on year 10 |
| gross margins | 68% |
| operating expenses | $50 bn |
| tax rate | 13% |
| discount rate | 9.5% |

That will be my 10-year forecast.
So let's code this up:

```python
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

```

Code can be found [here](/assets/msft_simple.py).
Here is the output:

```
Enterprise value (mm): 2,248,030
Market cap (mm): 2,293,514
Price per share: 308.48
```

This is very close to the current valuation.

## Stress testing

Let's stress test this model.
I'll vary the 2-year cloud growth rate `r` between 0 and 45% and see how the price per share changes.

I'll also add some randomness to the model. At each point in time, revenue will increase (or decrease) by a rate sampled from a normal distribution with mean `r` and standard deviation `0.02`.

Similarly, I'll have the gross margin sampled from a normal distribution with mean `0.68` and standard deviation `0.01`, so it's mostly constrained to be between `0.66` and `0.7`.
I'll do a similar thing for the operating expenses, having them grow at a rate sampled from a normal distribution with mean `0.02` and standard deviation `0.01`.

I will simulate each `r` scenario 100 times and take the average price per share.

| r | price per share |
|---|-----------------|
| 0.00 | 167.25 |
| 0.05 | 196.69 |
| 0.10 | 238.18 |
| 0.15 | 292.77 |
| 0.20 | 360.43 |
| 0.25 | 457.31 |
| 0.30 | 577.85 |
| 0.35 | 734.72 |
| 0.40 | 935.60 |
| 0.45 | 1190.69 |

Code can be found [here](/assets/msft_simple.py) and [here](/assets/msft_stress.py).
The simulations suggest that the current price is justified if the cloud/AI growth rate is between 15% and 20%.

## Conclusion

We haven't looked at a lot of things, like the specifics of the cloud market, competition, number of enterprise users, etc.
Taking a very detailed look at Microsoft would take tens if not hundreds of hours, but could unveil significant flaws in the model and assumptions I used.

I have built a model and I'm sure it can be improved. 
From here, I would probably wait for a year and revise my figures for growth rate, gross margin, etc. based on the actual results.

## Appendix: why use the CAPM discount rate?

It might seem confusing that we are using the CAPM discount rate, which is based on the risk of **stock returns**, to discount **cash flows**.
Should the riskiness of future cash flows mirror the volatility of stock price movements?

One straightforward answer is that the share price changes reflect the dividends that the company pays out as each cash flow comes in.
So when share prices fluctuate, they are reflecting a change in expectations about future dividends.
Note that we don't need actual dividends to be issued for this to work - a company might decide to reinvest all its cash flows instead of paying them out as dividends, but this reinvestment is expected to increase dividends further down the line.

Another way of looking at it is that the discount rate represents the opportunity cost of waiting to get dividends instead of investing the same money in a diversified portfolio of stocks with the same risk as the company.
Looking at it this way, it makes sense to use the CAPM rate to discount the cash flows.
