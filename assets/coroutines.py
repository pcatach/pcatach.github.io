# I am using python 3.12 for this.
# Hopefully you'll learn something about coroutines,
# but at the very least you'll learn how many dog breeds
# I know without googling.

# Let's start with a simple iterable, that is,
# a class that implements the __iter__ method:

class Kennel:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        return DogIterator(self.dogs)

# The __iter__ method must return an iterator,
# a class that implements __next__.
# Usually, we make the iterator implement
# an __iter__ too but that just returns self.
# An iterator is meant to traverse an iterable *once*
# and then die

class DogIterator:
    def __init__(self, dogs):
        self.dogs = dogs
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            next_dog = self.dogs[self.i]
        except IndexError:
            raise StopIteration
        self.i += 1
        return next_dog

# Let's see how this works:

kennel = Kennel(["chihuahua", "german shepherd", "beagle", "boxer"])

# the for syntax calls iter() on kennel
# which calls the __iter__method
# and then it calls next() on the resulting iterator
# until it raises StopIteration. The "for" also handles
# the StopIteration for us.
for dog in kennel:
    print(dog)
# prints:
# chihuahua
# german shepherd
# beagle
# boxer

# That's equivalent to:

kennel_iterator = iter(kennel)
while True:
    try:
        dog = next(kennel_iterator)
    except StopIteration:
        break
    print(dog)

# Cool.There's a simpler way to write the iterable/iterator above using yield:

class Kennel2:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        for dog in self.dogs:
            yield dog

# This is a bit subtle, but __iter__ does *not* return dogs one by one.
# Because of the yield statement, it actually returns a *generator*
# (which is an object that implements the iterator interface with __iter__ and __next__)
# that will return dogs to the caller until it's over
# (and then raise StopIteration).

kennel = Kennel2(["bulldog", "terrier", "corgi", "mastiff"])
for dog in kennel:
    print(dog)
# prints:
# bulldog
# terrier
# corgi
# mastiff

# I'll just mention here that what we did with yield we make even
# shorter using yield from. Yield from returns a generator
# that yields elements from another generator or iterator.
# In the case below, yield from returns a generator
# that yields values produced by the iterator iter(self.dogs).
# This is *not* the only thing that yield from
# is capable of, as we'll see later on.

class Kennel3:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        yield from self.dogs

kennel = Kennel3(["dalmatian", "irish setter"])
for dog in kennel:
    print(dog)

# In fact, we don't need a class like this to have
# an iterator. We can just use a generator function
# (any function with yield in its body) - it will return
# an object that implements the iterator interface:

def kennel_generator_factory(dogs):
    for dog in dogs:
        yield dog

kennel_generator = kennel_generator_factory(["maltese", "golden retriever"])
for dog in kennel_generator:
    print(dog)

# Imagine that we don't want to just
# print dogs, we'd like to make some of them bark too. That
# requires us to be able to "send" a "command" to our generator
# as we're iterating on it. Let's review the KennelIterator class:

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
        # so they'll just respond with a bark to any command
        print(f"The {self.dogs[self.i]} has barked!")
        return next(self)

kennel = Kennel4(["labrador", "greyhound"])
kennel_iterator = iter(kennel)
dog = next(kennel_iterator)
while True:
    print(dog)
    try:
        dog = kennel_iterator.send(">>> sit!")
    except StopIteration:
        break

# Now, the fun thing is, there's also a way to make this shorter:

def kennel_generator_factory2(dogs):
    for dog in dogs:
        command = yield dog
        print(command)
        if command is not None:
            print(f"The {dog} has barked!")

kennel_generator = kennel_generator_factory2(["poodle", "afghan hound"])
dog = next(kennel_generator)
while True:
    print(dog)
    try:
        dog = kennel_generator.send(">>> sit!")
    except StopIteration:
        break


# the expression "command = yield dog" basically divides the
# generator in two: the next() call will take the generator to the
# right hand side of "command = yield dog", yield back a dog
# to the caller, and wait in suspention.
# When .send() is called, its value will be assigned to the left
# hand side of "command = yield dog", and the generator runs until
# the following yield. If a next() is called instead of a send(),
# then the left hand side is assigned None.

# kennel_generator_factory2 and Kennel4 are
# not entirely equivalent.
# By using command = yield dog, I made kennel_generator_factory2 into
# a *coroutine*.
# A coroutine is a generator that "collaborates" with the caller, yielding
# and receiving values (Kennel4 is an approximation of a coroutine)

# to really be a coroutine, Kennel4 would need to implement
# other coroutine methods like close(), throw(), and a more complicated form
# of state management. For example, coroutines are also capable of returning values
# (in addition to yielding them)

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

# The return value is carried by the StopIteration exception instance,
# which is a bit awkward but hold that thought.

# Now get ready for the magic. Remember yield from?
# It not only delegates control to a subgenerator, it also
# allows values to send "through" it all the way to the subgenerator:

def kennel_controller(dogs):
    barking_dogs = yield from kennel_generator_factory3(dogs)
    print(f"{barking_dogs} dogs barked in total.")

# note that yield from handles the return value for us
# and assigns it to the left hand side of the yield from expression

kennel_generator = kennel_controller(["great dane", "pug"])
dog = next(kennel_generator)
while True:
    print(dog)
    try:
        dog = kennel_generator.send(">>> roll over!")
    except StopIteration:
        break

# To learn more see Fluent Python by Luciano Ramalho.