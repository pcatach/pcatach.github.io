# Let's start with a simple iterable, that is,
# a class that implements the __iter__ method:

class Kennel:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        return KennelIterator(self.dogs)

# The __iter__ method must return an iterator,
# a class that implements __next__.
# Usually, we make the iterator implement
# a __iter__ too but that just returns self.
# An iterator is meant to traverse an iterable *once*
# and then die

class KennelIterator:
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

# Cool.There's a simpler way to write the iterable/iterator above using yield:

class Kennel2:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        for dog in self.dogs:
            yield dog

# This is a bit subtle, but __iter__ does *not* return dogs one by one.
# Because of the yield statement, it actually returns a *generator*
# (which is an iterator)
# that will return dogs to the caller until it's over
# (and then raise StopIteration)

kennel = Kennel2(["bulldog", "terrier", "corgi", "mastif"])
for dog in kennel:
    print(dog)
# prints:
# bulldog
# terrier
# corgi
# mastif

# I'll just mention here that what we did with yield we make even
# shorter using yield from. Yield from returns a generator
# that yields elements from another generator or iterator
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
# (any function with yield in its body):

def kennel_generator(dogs):
    for dog in dogs:
        yield dog

for dog in kennel_generator(["maltese", "golden retriever"]):
    print(dog)

# Now here's the fun thing. Imagine that we don't want to just
# print dogs, we'd like to make some of them bark too. That
# requires us to be able to "send" a "command" to our generator
# as we're iterating on it. Let's review the KennelIterator class:

class Kennel4:
    def __init__(self, dogs):
        self.dogs = dogs

    def __iter__(self):
        return KennelIterator4(self.dogs)

class KennelIterator4:
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

    def send(self, command):
        dog = self.__next__()
        print(f"As a response to {command}, the {dog} has barked!")
        return dog

kennel = Kennel4(["labrador", "greyhound"])
kennel_iterator = iter(kennel)
while True:
    try:
        dog = kennel_iterator.send("sit!")
    except StopIteration:
        break
    else:
        print(dog)

# Now, the fun thing is, there's also a way to make this shorter:

def kennel_generator2(dogs):
    for dog in dogs:
        command = yield
        if command is not None:
            print(f"As a response to {command}, the {dog} has barked!")

kennel = kennel_generator2(["alsatian", "afghan hound"])
next(kennel)
while True:
    # we first need to "prime" the generator
    try:
        kennel.send("sit!")
    except StopIteration:
        break

# Now get ready for the magic. Remember yield from?