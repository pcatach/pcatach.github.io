---
layout: post
title: "Coroutines (and dog breeds)"
date: 2024-07-24 22:00:00 +0000
categories: tech
---

_(I am using Python 3.12 for this.)_

Hopefully you'll learn something about coroutines, but at the very least you'll learn how many dog breeds I know without googling.

Let's start with a simple iterable, that is, a class that implements the `__iter__` method:

```python
class Kennel:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        return DogIterator(self.dogs)
```

The `__iter__` method must return an iterator, a class that implements `__next__`. We usually make the iterator implement an `__iter__` too but that just returns `self`.
An iterator is meant to traverse the contents of an iterable _once_ and then die.

```python
class DogIterator:
    def __init__(self, dogs):
        self.dogs = dogs
        self.i = None

    def __iter__(self):
        return self

    def __next__(self):
        self.i = 0 if self.i is None else self.i + 1
        try:
            dog = self.dogs[self.i]
        except IndexError:
            raise StopIteration
        return dog
```

Let's see how this works. The `for` syntax calls `iter()` on `kennel` which calls the `__iter__` method, and then it calls `next()` on the resulting iterator
until it raises `StopIteration`.
The `for` also handles the `StopIteration` for us.

```python
kennel = Kennel(["chihuahua", "german shepherd", "beagle", "boxer"])
for dog in kennel:
    print(dog)
```

Prints:

```
chihuahua
german shepherd
beagle
boxer
```

That's equivalent to:

```python
kennel_iterator = iter(kennel)
while True:
    try:
        dog = next(kennel_iterator)
    except StopIteration:
        break
    print(dog)
```

Cool. There's a simpler way to write the iterable above using `yield`:

```python
class Kennel2:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        for dog in self.dogs:
            yield dog
```

This is a bit subtle, but `__iter__` does _not_ return dogs one by one.
Because of the `yield` statement, it actually returns a _generator_, which is an object that implements the iterator protocol (with `__iter__` and `__next__`).
That will return dogs to the caller until it's over, and then raise `StopIteration`:

```python
kennel = Kennel2(["bulldog", "terrier", "corgi", "mastiff"])
for dog in kennel:
    print(dog)
```

Prints:

```
bulldog
terrier
corgi
mastiff
```

I'll just mention here that what we did with `yield` we can make even shorter using `yield from`. `yield from` returns a generator that yields elements from another iterator or generator.
In the case below `yield from` returns a generator that yields values provided by the iterator `iter(self.dogs)`.
This is _not_ the only thing that `yield from` is capable of, as we'll see later on.

```python
class Kennel3:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        yield from self.dogs

kennel = Kennel3(["dalmatian", "irish setter"])
for dog in kennel:
    print(dog)
```

Prints:

```
dalmatian
irish setter
```

In fact, we don't need a class like this to have an iterator.
We can just use a generator function, which is any function with `yield` in its body - it will return an object that implements the iterator protocol:

```python
def kennel_generator_factory(dogs):
    for dog in dogs:
        yield dog

kennel_generator = kennel_generator_factory(["maltese", "golden retriever"])
for dog in kennel_generator:
    print(dog)
```

Prints:

```
maltese
golden retriever
```

Imagine that we don't want to just print dogs.
We'd like to make them bark too.
That requires us to be able to "send" a "command" to our generator as we're iterating on it.
Let's review the `DogIterator` class:

```python
class Kennel4:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        return DogIterator4(self.dogs)


class DogIterator4:
    def __init__(self, dogs):
        self.dogs = dogs
        self.i = None

    def __iter__(self):
        return self

    def __next__(self):
        self.i = 0 if self.i is None else self.i + 1
        try:
            dog = self.dogs[self.i]
        except IndexError:
            raise StopIteration
        return dog

    def send(self, command):
        print(command)
        # we could do something with command
        # but let's say our dogs are not well trained
        # so they'll just respond with a bark to any commmand
        print(f"The {self.dogs[self.i]} has barked!")
        return next(self)
```

Now we can use the `send()` interface to make these dogs bark:

```python
kennel = Kennel4(["labrador", "greyhound"])
kennel_iterator = iter(kennel)
dog = next(kennel_iterator)
while True:
    print(dog)
    try:
        dog = kennel_iterator.send(">>> sit!")
    except StopIteration:
        break
```

Prints:

```
labrador
>>> sit!
The labrador has barked!
greyhound
>>> sit!
The greyhound has barked!
```

Now the fun thing is, there's also a way to make this shorter:

```python
def kennel_generator_factory2(dogs):
    for dog in dogs:
        command = yield dog
        print(command)
        if command is not None:
            print(f"The {dog} has barked!")
```

The expression `command = yield dog` basically divides the generator in two phases:
the `next()` call will take the generator to the right hand side of `command = yield dog`, yield back a `dog` to the caller, and wait.

When `send()` is called, its value will be assigned to the left hand side of `command = yield dog` and the generator will run until the following `yield`.
If `next()` is called instead of `send()`, then the left hand side will be assigned `None`.

```python
kennel_generator = kennel_generator_factory2(["poodle", "afghan hound"])
dog = next(kennel_generator)
while True:
    print(dog)
    try:
        dog = kennel_generator.send(">>> sit!")
    except StopIteration:
        break
```

This prints:

```
poodle
>>> sit!
The poodle has barked!
afghan hound
>>> sit!
The afghan hound has barked!
```

`kennel_generator_factory2` and `Kennel4` are not entirely equivalent.
By using the expression `command = yield dog` I made `kennel_generator_factory2` into a _coroutine_.
A _coroutine_ is a generator that "collaborates" with the caller, yielding and receiving values (`Kennel4` is an approximation of a coroutine).

To really be a coroutine, `Kennel4` would need to implement other coroutine methods like `close()`, `throw()` (which I won't get into) and a more complicated form of state management.
For example, coroutines are also capable of returning values (in addition to yielding them):

```python
def kennel_generator_factory3(dogs):
    barking_dogs = 0
    for dog in dogs:
        command = yield dog
        print(command)
        if command is not None:
            print(f"The {dog} has barked!")
            barking_dogs += 1
    return barking_dogs

kennel_generator = kennel_generator_factory3(["basset hound", "shih tzu"])
dog = next(kennel_generator)
while True:
    print(dog)
    try:
        dog = kennel_generator.send(">>> sit!")
    except StopIteration as exc:
        barking_dogs = exc.value
        print(f"{barking_dogs} dogs barked.")
        break
```

The return value is carried by the `StopIteration` exception instance, which is a bit awkward but hold that thought.
This prints:

```
basset hound
>>> sit!
The basset hound has barked!
shih tzu
>>> sit!
The shih tzu has barked!
2 dogs barked.
```

Now get ready for the magic.
Remember `yield from`?
It not only delegates control to a subgenerator, it also allows values to be sent "through" it all the way to the subgenerator.
Let's write a delegating generator:

```python
def kennel_controller(dogs):
    barking_dogs = yield from kennel_generator_factory3(dogs)
    print(f"{barking_dogs} dogs barked in total.")
```

Note that `yield from` handles the return value for us and assigns it to the left hand side of the `yield from` expression.

Now we can send commands through the controller to each one of the dogs:

```python
kennel_generator = kennel_controller(["great dane", "pug"])
dog = next(kennel_generator)
while True:
    print(dog)
    try:
        dog = kennel_generator.send(">>> roll over!")
    except StopIteration:
        break
```

This prints:

```
great dane
>>> roll over!
The great dane has barked!
pug
>>> roll over!
The pug has barked!
2 dogs barked in total.
```

To learn more, you can read _Fluent Python_ by Luciano Ramalho.
