---
layout: post
title:  "Climate Change: Some Maths"
subtitle: "And: what does the IPCC Assessment Report 6 say?"
date:   2023-03-14 09:00:00 +0000
categories: science
---

One of the most urgent things that humanity has to do, we are told, is "solving" the climate crisis. 
So I want to know what is the climate crisis, get familiar with the data, and understand what would it mean to solve the climate crisis.

Every 6-7 years the Intergovernmental Panel on Climate Change (IPCC) publishes an Assessment Report with a review of all published
literature on climate change. 
That’s the most important authority on climate science. 
The 6th report (AR6) was published in 2021 and I gave a read to the Working Group I (WGI) contribution (Physical Science Basis).

I want to understand the basics of the models used to forecast climate change, what the most important findings are, 
what it means for us humans and what can we do about it.

> Disclaimer: I'm a mere software developer with a background in physics.

## Stefan-Boltzmann law (feel free to skip)

Let's start from the basics. I’ll assume some quantum mechanics background.
A black body is an opaque collection of particles in thermodynamic equilibrium with its environment.
It can be considered a gas of indistinguishable non-interacting bosons (photons) at a fixed temperature. 
The mean number of particles in state `s` with energy `ε_s = ℏ*ω_s` is

```
<n_s> = -1/β ∂log(Z) / ∂ε_s
```

The partition function `Z` is:

```
Z = Sum exp( -β * Sum_i n_i ε_i)
```

summing over all possible occupation states. If we re-write the partition function as a product of geometric series, we obtain Planck's distribution:

```
Z = [Sum (from n=0 to infinity) exp(-β * n * ε_1)] * [Sum (from n=0 to infinity) exp(-β * n * ε_2)] * ...
  = [ 1 / (1 - exp(-β * n * ε_1 )) ] * ...
<n_s> = 1 / (exp(-β * ε_s) - 1)
```

For a photon with frequency `ν`, `ε_ν = h * ν`. This allows us to compute the energy per unit volume per unit wavelength of this gas: it is the 
multiplication of the photon energy `ε_ν` by the mean number of particles in state `ν` 
by the [density of states](http://hyperphysics.phy-astr.gsu.edu/hbase/quantum/phodens.html):

```
I(λ ) = 8 * π * h * c / [λ^5 * (exp(β * h * c / λ) - 1)]
```

expressed in terms of wavelength (`λ = c / ν`). Or, per unit solid angle (dividing by `4 * π`):

```
I(λ ) = 2 * h * c / [λ^5 * (exp(β * h * c / λ) - 1)]
```

This can be [integrated](https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law#Derivation_from_Planck's_law) for 
all wavelenghts and for all solid angles to give

```
P / A = (2 * π * h / c^2) * (k_B * T / h)^4 * π^4 / 15 = σ * T^4
```

This is the Stefan-Boltzmann law. It describes the amount of power per unit area that a black body radiates. 
The Stefan-Boltzmann constant is `σ = 5.67 * 10**(-8)`.

## The Energy Balance model

