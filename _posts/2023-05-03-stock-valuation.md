---
layout: post
title:  "Stock valuation from first principles"
date:   2023-05-03 10:00:00 +0000
categories: social-science
---

My starting point for this post is this [reddit thread](https://www.reddit.com/r/ValueInvesting/comments/12e0bpa/microsoft_corporation_msft_valuation_the_big_tech/). 
The thread is from April 6th 2023 and the author is trying to value Microsoft stock.

Given a few assumptions like the revenue growth rate, operating margin and cost of capital, they arrive at a number
of $253 per share. 
Microsoft (MSFT in NASDAQ) is trading at the moment at $305, so the author concludes that the stock is overvalued.

I don't want to know if this person got it right or wrong, but they are clearly using a method, and it turns out
that this is a very popular method for valuing stocks.

In this post, I will try to give an estimate of MSFT stock price using two models (CAPM and DCF) and say a few words
about how these estimates should be used.

## CAPM

The [Capital Asset Pricing Model](https://en.wikipedia.org/wiki/Capital_asset_pricing_model) (CAPM) essentially
says that the expected return of a stock is proportional to the risk that an investor takes by holding that stock.
Thefore, riskier stocks should have higher expected returns - investors are compensated for taking more risk.

As a refresher, a linear model assumes that given two random variables `X` and `Y`:

```
Y = b + m * X + e
```

`b` and `m` are the parameters of the model and `e` is the error term with mean 0.
It's easy to show that

```
b = E(Y) - m * E(X)
m = Cov(X, Y) / Var(X)
```

(the first is trivial taking the expected value of both sides of the equation, the second is a easy 
expanding the covariance and variance terms).

The statement of the CAPM is:

```
R_i = R_f + (R_m - R_f) * b_i + a_i (1)
```

where `R_i` is the return of a stock `i`, `R_f` is the risk-free return rate and `R_m` is the average return of the market. 
This equation uses the independent variable `b_i`, the risk coefficient of `i`, to predict the random variable `R_i`.
`a_i` is the "abnormal" rate of return, which represents the extra return that the stock `i` has just by being itself.

We want to estimate `b_i` and `a_i` from historical data so that we can predict the future return of the stock.
Given `n` observations at times `t` of the return of the stock `i` and the market, we can use linear regression:

```
R_i(t) - R_f(t) = a_i + b_i * (Rm(t) - Rf(t)) + e_i(t) (2)
```

where `e_i(t)` is the error term (note how, in this second equation, `a_i` and `b_i` switched from being random variables to being parameters that we're estimating):

```
b_i = Cov(R_i(t), Rm(t)) / Var(Rm(t))
a_i = E(R_i(t)) - b_i * E(Rm(t))
```

Here is some code

```python
import pandas as pd
import yfinance as yf

# Download the historical data for MSFT and S&P 500
msft = yf.Ticker("MSFT").history(period="2y")
sp500 = yf.Ticker("^GSPC").history(period="2y")

# Set the risk-free rate
risk_free_rate = 0.033 / 252  # Assume 3.3% annualized rate, compounded daily

# Compute the daily returns for MSFT and S&P 500
msft_returns = msft["Close"].pct_change() - risk_free_rate
sp500_returns = sp500["Close"].pct_change() - risk_free_rate

# Compute the covariance of MSFT returns with S&P 500 returns, as well as the variance of S&P 500 returns
covariance = msft_returns.cov(sp500_returns)
variance = sp500_returns.var()

# Compute the b and a of MSFT
b = covariance / variance  
a = msft_returns.mean() - b * sp500_returns.mean()

print(a.round(5), b.round(5))  # today, this gives me 0.00058 1.26472
```

A `b` of 1.26 means that MSFT is heavily dependent on market returns. This is a plot of the daily adjusted returns of MSFT and S&P 500,
together with the linear regression line:

![MSFT and S&P 500 returns](/assets/msft_sp500_returns.png)

Now, to use the CAPM model to predict the expected return of MSFT, we can use

```python
# Compute the expected return of MSFT
expected_return = risk_free_rate + b * (sp500_returns.mean() - risk_free_rate) + a 
```

Today, this gives me 0.00045 which annualized is `(1 + 0.00045)^252 - 1 = 12%`. 
To convert this estimate into a share price, we will use DCF.

## DCF

The [Discounted Cash Flow](https://en.wikipedia.org/wiki/Discounted_cash_flow) (DCF) model is a way to estimate the value of a stock given 
the expected future cash flows of the company. 

To value a stock according to DCF, we project the future cash flows of the company and then discount them to the present. 
For example, we computed that the expected return of MSFT is 12%. 

Let's assume that this is going to be the case for the next 10 years, 
after which the company will grow at a rate of 3.3% (the risk-free rate).
Additionally, we know that Microsoft's cost of capital is 8%, and we'll assume 
it will decrease to 7.8% in 10 years. 

The future value of a present cash at a future time `n` is

```
CF(n) = CF(0) * (1 + g)^n
```

where `CF(0)` is the present value of the cash flow and `g` is the expected growth rate.
To discount this future value to the present, we use the cost of capital `k`:

```
DCF(n) = CF(n) / (1 + k)^n
```

So each cash flow can be presently valued as

```
DCF(n) = CF(0) * (1 + g)^n / (1 + k)^n
```

The sum of all the cash flows is the value of the company:

```
Value = Sum(DCF(n)) for n in [1, \infty)
```

Let's code this up.
We'll assume a present cashflow of $9.65 per share.

```python
def discounted_cashflow(cf, g, k, n):
    """ Present value of a future cashflow at time n """
    return cf * (1 + g)**n / (1 + k)**n

g = 0.12
k = 0.08
cf = 9.65
# up to year n = 10
value = 0
for n in range(1, 11):
    value += discounted_cashflow(cf, g, k, n)

# after year n = 10, the rates change
g = 0.033
k = 0.078
for n in range(11, 500):
    delta = discounted_cashflow(cf, g, k, n)
    value += delta
    if delta < 0.01:
        break
value  # 262.91
```

In theory, this would suggest that this stock, currently sitting at $305, is 
massively overvalued. However, there are a few caveats to this model.

Firstly, it assumes a constant (or stepwise) growth rate and 
cost of capital, which is not realistic. In fact, we saw above that
Microsoft returns are highly correlated with the market.
It also overlooks the elephant in the room: the big premium on microsoft stocks
due to the opportunity with AI. 

The importance of this exercise is that it gives a fundamentals-based estimate 
that we can forecast around. Do you think that AI will be a huge opportunity
for Microsoft? Then that might justify the current price. Do you think that
AI will be a flop? Then you might want to sell.
