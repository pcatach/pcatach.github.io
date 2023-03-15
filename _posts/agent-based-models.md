---
layout: post
title:  "Agent-based Models in Economics"
date:   
categories: social-science
---

Equilibrio de walras: base de muito da teoria economica

Dadas algumas condicoes:

Numero finito de empresas:

buscam maximizar seus lucros

produzem bens e servicos de qualidade conhecida

Numero finito de consumidores:

buscam maximizar sua utilidade (definida exogenamente)

decidem comportamento baseados em preços e dividendos

Um “Leiloeiro Walrasiano”:

Determina preços tal que para cada mercado oferta = demanda

(First Welfare Theorem): em uma situação de equilibrio, bens e serviços serão  alocados de maneira “Pareto eficiente”.

Pareto eficiente significa que nenhuma troca adicional aumentaria a utilidade de um consumidor sem diminuir a utilidade de outro.

(Nao há garantia de que pareto eficiente = socialmente desejavel)

Walrasian equilibrium in modern-day form is a precisely formulated set of conditions under which feasible allocations of goods and services can be price-supported in an economic system organized on the basis of decentralized markets with private ownership of productive resources. These conditions postulate the existence of a finite number of price-taking profit-maximizing firms who produce goods and services of known type and quality, a finite number of consumers with exogenously determined preferences who maximize their utility of consumption taking prices and dividend payments as given, and a Walrasian Auctioneer (or equivalent clearinghouse construct) that determines prices to ensure each market clears. Assuming consumer nonsatiation, the First Welfare Theorem guarantees that every Walrasian equilibrium allocation is Pareto efficient.

Walrasian equilibrium: https://en.m.wikipedia.org/wiki/Competitive_equilibrium

https://en.wikipedia.org/wiki/Fundamental_theorems_of_welfare_economics#L%C3%A9on_Walras_(1870)

Walrasian equilibrium is an elegant affirmative answer to a logically posed issue: can efficient allocations be supported through decentralized market prices? It does not address, and was not meant to address, how production, pricing, and trade actually take place in real-world economies through various forms of procurement processes.

economists have not been able to find empirically compelling sufficient conditions guaranteeing existence of Walrasian equilibria, let alone uniqueness, stability, and rapid speed of convergence, even for relatively simple modelings of market economies

Esse framework (walrasiano) nao explica como produção, pricing e trade de fato funcionam num modelo do mundo real.

O livro disse que não existe uma demonstração nem evidência empirica de que tal equilibrio sempre exista, mesmo em modelos simples de economias de mercado.

A natural way to proceed is to examine what happens in a standard Walrasian model if the Walrasian Auctioneer pricing mechanism is removed and if prices and quantities are instead required to be set entirely through the procurement actions of the firms and consumers themselves

ABMs: substituir o leiloeiro de Walras por procurement entre as empresas e os consumidores. Determinar condicoes iniciais e as regras para cada a gente, assistir o sistema evoluir

One key departure of ACE modeling from more standard approaches is that events are driven solely by agent interactions once initial conditions have been specified. Thus, rather than focusing on the equilibrium states of a system, the idea is to watch and see if some form of equilibrium develops over time

Dificuldade: validar os outputs do modelo contra o mundo real. O que nos observamos no mundo real pode ser um evento de baixa probabilidade na distribuição de resultados do modelo

Another drawback is the difficulty of validating ACE model outcomes against empirical data.For example, an empirically observed outcome might be a low-probability event lying in a relatively small peak of the outcome distribution for this true data-generating process, or in a thin tail of this distribution.

ACE Trading World

agent-based computational economics simple model of two-sector economy, a walrasian equilibrium where the auctioneer is removed and replaced with procurement processes.

We consider a one-period economy with two production sectors: hash and beans. 

Profit seeking firms producing hash

Profit seeking firms producing beans

Consumers who derive utility from consuming hash and beans

Firms have a cost function expressing production costs as a function of output level.

Consumers have equal ownership share in each firm and exogenous money income.

In the beginning, each firm selects a supply level to maximise its profits, conditional on price expectations for hash and beans. At the end of the period, profits are distributed back to shareholders.

In the beginning, each consumer chooses hash and beans demand to maximise utility conditional on (i) dividends expectations and (ii) price expectations. The expected value of expenses must be limited by the expected total income.

Definition: A Walrasian equilibrium is a vector e* of demands, supplies, prices, expected prices and expected dividends such that

(individual optimality) at e*, all consumer demands are optimal conditional on expected prices and expected dividends, and all firm supplies are optimal conditional on expected prices

(correct expectations) at e*, expected prices and dividends are the same as actual prices and dividends

(market clearing) at e*, total supply is greater than or equal to total demand

(Walras’ law) at e*, the total value of excess supply is zero

The role of the Walrasian Auctioneer is to fulfill conditions 2 to 4. To replace this, the agent-based model requires the following methods:

- Terms of trade: firms must determine how to set their prices and supply

- Seller-buyer matching: firms and consumers must take part in a matching process

- Rationing: firms and consumers must handle excess demands or supplies coming from this matching

- Trade: carry out actual trades

- Settlement: settle payment obligations

- Shake-out: firms that become insolvent and consumers that fail to satisfy their subsistence means exit the economy (die)

The ACE trading world:

- at time T=0, each firm has a nonnegative amount of money and a positive production capacity
- Firms know about their cost function, other firms and consumers in the economy
- Firms don’t know the income and utility function of consumers or the cost function and capacity of other firms.
- Collusion is prohibited by antitrust laws
- at time T=0, consumers has an income (=exogenous + savings from previous periods + dividends), a utility function, and a share of each hash and bean firm.
- At each period, each firm selects a supply offer (supply level + unit price). 
- At each period, consumers know all firm offers as soon as they are posted, and attempt to ensure utility following a price discovery process consisting of several rounds:

-- on each round, if a consumer cannot meet their subsistence needs at the lowest posted prices, they exit the process
-- 
-- each consumer determines their demand conditional on their utility, income and current lowest prices posted
-- 
-- consumers submit their demands, firms satisfy applying if needed a rationing method
-- 
-- actual trades take place
-- 
-- firms with remaining supply and customers with unfulfilled subsistence needs proceed to a next round

- At the end of these rounds, consumers who exited or who finished with unmet subsistence needs die, with their unspent income lost and their shares redistributed

- Each firm computes it’s net worth at T (assets minus liabilities), and exit the economy if insolvent. Other companies allocate their profits (and losses) in (dis)savings, (dis)investment or (always nonegative) dividends.

Let X(T) be the state of the ACE Trading World at time T. Then X(T+1) = S(X(T)) for some S. A situation where all firms and consumers die could be regarded as an equilibrium as X(T+1) = X(T). But more interestingly we could define equilibrium in various ways:

- Unchanging carry capacity (number of solvent firms and viable consumers remains the same)
- Continual market clearing (demand = supply over time)
- Unchanging structure (capacity levels remain the same)
- Firms selection of supply offer remain the same
- Unchanging trade network (who trades with who remains the same)
- Steady-state growth path (constant growth rate for capacity and production and consumption levels)

“essential primacy of survival”: utility function must incorporate subsistence, which means that at subsistence levels the function must be non-concave: let u_k be the utility of a consumer such that below that level the function must be zero, and above it must increase. 
this invalidates many economics theorems that only work with concave functions - that makes it easier to prove uniqueness of equilibrium.

We could define a social welfere utility function W(u_1, …, u_k) with dW/du_k > 0. Then, given limited resources, this would imply that consumers with high subsistence needs x_k should die to improve social welfare for all, even if there were enough resources to guarantee subsistence for all. This points to imposing subsistence as an additional constraint to the social welfare maximization problem.

Opposing to that, subsistence is usually taken for granted, with an assumption that the economic system is near or at equilibrium points. In ACE, subsistence and solvency are not taken for granted, so economists need to build firms and consumers capable of surviving.

ch 16 section 4.3 Strategic rivalry and market power