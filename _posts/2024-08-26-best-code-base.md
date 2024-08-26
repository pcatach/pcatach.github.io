---
layout: post
title: "What is the best code base you've ever worked on?"
date: 2024-08-26 12:00:00 +0000
categories: tech
---

A couple months ago I asked on [Hacker News](https://news.ycombinator.com/item?id=40818809):

> Ask HN: What is the best code base you ever worked on?
> 
> And what made it so good?
>
> Was there someone enforcing good practices top down? Just being in a group of great engineers? Or something else?

I asked the question on a Friday morning during my commute and didn't expect much. To my surprise, it got quite popular, hit the front page of HN and at the moment of writing has 454 comments. This was a bit awkward as I realised there was a mistake in the title (should have been "you've" and not "you"), but hey.

I could barely keep up with the initial ~100 answers when (presumably) the US woke up and I got a few hundred more at once. No one has time to read all the comments on a front page HN post. Right?

## What makes a good code base?

_Good_ is obviously subjective, and I kept the question intentionally vague as I was also curious to know what people considered to be good code.

Scrolling through everyone's thoughts I started to notice some patterns, and decided that I would write down whatever I could learn from this, if anything.
And no, I won't use an LLM or whatever NLP technique to identify clusters in idea-space. Just good old sit down and read one by one.

Here are the main ideas I could identify.

## Great engineers

> Ultimately, the reason it was good was because the engineers had zero ego on top of having excellent skills. [...] every time some new requirement came up, these senior / principal engineers would discuss it in the most civilized matter I have ever seen.
> 
> E.g, "we need to come up with a way to implement X". Person A gives their idea, person B gives another idea and so on until everybody shared their thoughts. Then someone would say "I think what person C said makes the most sense" and everybody would agree and that was it. 30 minutes to hear everybody out, 3 minutes to discuss who will do it and when and the meeting was over.

[source](https://news.ycombinator.com/item?id=40819222)

## Good process or tooling

Very little mention of training, interestingly.

### Consistency matters

> Worked on a codebase for a large safety-critical system where everything was 100% documented, and the development guide for the project was followed so closely that you couldn't tell, across millions of lines of code, that the whole thing wasn't written by one person. Absolutely impressive levels of attention to detail everywhere, down to not even being able to find typographical errors in comments or documentation (a typo in a comment was treated just as seriously as any other bug).

[source](https://news.ycombinator.com/item?id=40819140)

### Consistency doesn't matter

Ownership and familiarity are more important:

> I've found that familiarity with the codebase is more important than having it be perfectly engineered. Once you're really familiar with the codebase, you know where dragons be, and you can make changes more easily. And God (PM) forbid, if you ever find yourself with some extra free time you might even reduce the size of dragons over time.
>
> This brings me to my final point. Any codebase that I really enjoyed working with was the one that was constantly evolving

[source](https://news.ycombinator.com/item?id=40819057)

> I now work for an organization that discourages code ownership, and it struggles on many fronts:
>
> 1.  core teams are dysfunctional
> 2.  people find niches and stick to them
> 3.  top talent is leaving, although pay is good and business creates real value for citizens
> 4.  there is virtually no horizontal communication
> 5.  mediocre ones rise to the level of their incompetence and infest the lives of others
> 6.  and so on and so forth...

[source](https://news.ycombinator.com/item?id=40819086)

## Monorepo vs small repos

Consensus seems to be: if systems are almost 100% independent, split, if not, keep monorepo to avoid dependency hell. And that monorepo needs good tooling.

## Google and Facebook

The most often mentioned project was "google3", which is Google's monorepo.
It got often compared to Facebook's code base and led to a lot of discussion on whether it still is what it used to be, what tooling is available and how it has affected code bases in several other projects touched by the Xoogler diaspora.

A few alleged features:

> - Creating a mutable snapshot of the entire codebase takes a second or two.
> - Builds are perfectly reproducible, and happen on build clusters. Entire C++ servers with hundreds of thousands of lines of code can be built from scratch in a minute or two tops.
> - The build config language is really simple and concise.
> - Code search across the entire codebase is instant.
> - File history loads in an instant.
> - Line-by-line blame loads in a few seconds.
> - Nearly all files in supported languages have instant symbol lookup.
> - There's a consistent style enforced by a shared culture, auto-linters, and presubmits.
> - Shortcuts for deep-linking to a file/version/line make sharing code easy-peasy.
> - A ton of presubmit checks ensure uniform code/test quality.
> - Code reviews are required, and so is pairing tests with code changes.

[source](https://news.ycombinator.com/item?id=40823142)

## Specific mentions

These projects received more than a couple mentions as examples of great code bases:

- [PostgreSQL](https://github.com/postgres/postgres)
- [Kubernetes](https://github.com/kubernetes/kubernetes)
- [NetBSD](https://github.com/NetBSD/src)
- [Redis](https://github.com/redis/redis)

I also enjoyed this cute interaction: https://news.ycombinator.com/item?id=40824087
