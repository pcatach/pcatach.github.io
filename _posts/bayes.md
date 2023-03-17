---
layout: post
title:  "Introduction to Bayesian Statistics"
date:   2022-06-08 16:23:00 +0000
categories: maths
---

## Bayesian Statistics

A probability is our degree of confidence in a belief, that is how much you anticipate some event to occur.

> An event with Bayesian probability of .6 (or 60%) should be interpreted as stating
> "With confidence 60%, this event contains the true outcome", whereas a frequentist interpretation would view it as stating 
> "Over 100 trials, we should observe event X approximately 60 times."

Ou confidence in a belief can change to reflect new evidence using Bayes' theorem, which can be derived as follows:

```
P(model, evidence) = P(model | evidence ) * P(evidence) = P(evidence | model) * P(model)
P(model | evidence) = P(model) * P(evidence | model) / P(evidence)
```

So if we have a test for a hypothesis that can have a negative or a positive outcome, we can use this rule to update our belief in this hypothesis 
depending on the test outcome.

The probability that a test gives a true positive divided by the probability that a test gives a false positive is known as the likelihood ratio of that test.
The likelihood ratio for a positive result summarizes how much a positive result will slide the prior probability.
The likelihood ratio says how strong the positive test is as evidence.

## Example

Suppose that the prior prevalence of breast cancer in a demographic is 1%. 
Suppose that we, as doctors, have a repertoire of three independent tests for breast cancer. 

Our first test, test A, a mammography, has a likelihood ratio of `80%/9.6% = 8.33`. 
Again, that means a true positive probability of 80% and a false positive probability of 9.6%.

The second test, test B, has a likelihood ratio of 18.0 (for example, from 90% versus 5%); and the third test, test C, has a likelihood ratio of 3.5 
(which could be from 70% versus 20%, or from 35% versus 10%; it makes no difference). 
Suppose a patient gets a positive result on all three tests. What is the probability the patient has breast cancer?

For each test:

```
P(cancer | +) = P(+ | cancer) * P(cancer) / P(+)
P(cancer | +) = P(+ | cancer) * P(cancer) / ( P(+ | cancer) * P(cancer) + P(+ | ¬cancer) * P(¬cancer) )
```

If it was just test A:

```
P(cancer | +) = 80% * 1% / ( 80% * 1% + 9.6% * 99% ) = 7.8%
```

In terms of odds, this is:

```
80 : 9.6 = 25 : 3
```

The prior odds of having cancer are `1:99`. So the odds of having cancer given a positive result are:

```
1 x 25 : 99 x 3 = 25 : 297
```

Or, equivalently, 7.8%.
For all 3 tests combined:

```
P(cancer | all 3) = (80% * 90% * 70%) * 1% / ( (80% * 90% * 70%) * 1% + (9.6% * 5% * 20%) * 99%) = 84%
```

Note that we could have replaced 70%, 20% by 35%, 10% without changing the result.
In terms of odds:

```
18 : 1 (test B)
3.5 : 1 = 7 : 2 (test C)
1 × 25 × 18 × 7 : 99 × 3 × 1 × 2 = 3150 : 594
```

Which gives us a probability of `3150 / (3150 + 594) = 84%`.

## Bayesianism vs Frequentism

The frequentist interpretation: 

> When we say the coin has a 50% probability of being heads after this flip, we mean that there's a class of events similar to this coin flip,
> and across that class, coins come up heads about half the time. That is, the frequency of the coin coming up heads is 50% inside the event class,
> which might be "all other times this particular coin has been tossed" or "all times that a similar coin has been tossed", and so on.

The bayesian interpretation:

> Uncertainty is in the mind, not the environment. If I flip a coin and slap it against my wrist, it's already landed either heads or tails. 
> The fact that I don't know whether it landed heads or tails is a fact about me, not a fact about the coin. 
> The claim "I think this coin is heads with probability 50%" is an expression of my own ignorance, and 50% probability means that I'd bet at 1 : 1 odds
> (or better) that the coin came up heads.

The difference is more apparent when discussing ideas. A frequentist will not assign probability to an idea; 
either it is true or false and it cannot be true 6 times out of 10.

## Bayesian interpretation of Popper falsificationism

Suppose we have a theory A and some evidence X. The likelihood ratio for X, is `P(X|A)/P(X|¬A)`.
Even if you theory can predict X with probability 1, you can’t control the denominator of the likelihood ratio, 
`P(X|¬A)` — there will always be some alternative theories that also predict X, and you may eventually find some evidence that an alternative theory predicts 
by yours doesn't. There's a limit to how high the likelihood ration can be for any evidence X in favour of A.

However, if some new evidence Y is not predicted by A, this has a huge weight against it. 
The likelihood ratio for Y will be negligible. 
This is a consequence of the fact that a high likelihood ratio (that is, strong evidence for A) is not a very high P(X|A), but of a very low P(X|¬A).
Falsification is much stronger than confirmation.

Popper says that any theory must be falsifiable: if X is evidence for A, ¬X must be evidence against A. 
However, Popper also says that we can always refute a theory. 
That is not true: falsification is still probabilistic, we can never rule out a very low P(A|¬X).
