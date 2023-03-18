---
layout: post
title:  "Occam's Razor from First Principles"
date:   2022-06-08 16:23:00 +0000
categories: maths
---

> “The law of parsimony: Entities should not be multiplied beyond necessity.”

For any propositions X and Y, the conjunction rule says:

```
P(X,Y) <= P(X)
```

If `X` and `Y` are independent, `P(X,Y) = P(X) * P(Y)` and the result follows from `0 <= P(X) <= 1`. If they are not independent, `P(X,Y) = P(X) * P(Y | X)` and the result follows too.

> The “entities” counted by Occam’s Razor should be individually costly in probability; 
this is why we prefer theories with fewer of them.

As an example, consider a lottery that sells a million tickets. 
Given the two hypotheses ‘Tomorrow, someone will win the lottery’ and ‘Tomorrow, I will win the lottery’, the latter is much "simpler". 
But in the former, we can sum over the probabilities that anyone else wins the lottery, so we get a much larger probability.

However, if I win 10 times in a row, the later hypothesis predicts the data much better. 
It has more entities (it must point out a specific individual instead of "someone"), but they are within necessity.

Occam's razor can be formalized in terms of the [Minimum Description Length principle](https://en.wikipedia.org/wiki/Minimum_description_length). 
We encode any hypothesis as a binary string `x` that represents the shortest possible description of the hypothesis. 
The prior for any hypothesis should be inversely proportional to the length of its shortest description.

In our lottery example, the two hypotheses can be represented as a binary string of length 1M (the number of tickets). 
The first 0 or 1 says if the first ticket can be a lottery winner tomorrow or not. Then our first hypothesis is encoded as

```
'11111111...' = '1' x 1,000,000
```

whereas the second hypothesis would be something like

```
'1000000...' = '1' + '0' x 999,999
```

so that we see that the second hypothesis has a longer description, therefore we should assign priors `P(H1) > P(H2)`.

However, if we observe that I win the lottery 10 times in a row, Bayes rule updates those priors in a way that `H2` comes out looking much better.

Let's say, if we start with `P(H1)/P(H2) = 1e20` and we update like

```
P(H1 | 10x I win) = P(10x I win | H1) * P(H1) / P(10x I win)
P(H1 | 10x I win) = (1/1e7)**10 * P(H1) / P(10x I win)
```

and

```
P(H2 | 10x I win) = 1 * P(H2) / P(10x I win)
```

such that `P(H1 | 10x I win) / P(H2 | 10x I win) = 1e-70 * 1e20 = 1e-50` (!!).