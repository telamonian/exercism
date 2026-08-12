import math

class bucket:
    def __init__(self, name, size, _contents=0, _actions=0):
        self.name = name
        self.size = size
        self.contents = _contents
        self.actions = _actions

    @property
    def capacity(self):
        return self.size - self.contents

    @property
    def isempty(self):
        return self.contents == 0

    @property
    def isfull(self):
        return self.contents == self.size
    
    def _empty(self):
        self.contents = 0

    def empty(self):
        self._empty()
        self.actions += 1
    
    def _fill(self):
        self.contents = self.size

    def fill(self):
        self._fill()
        self.actions += 1

    def pourin(self, other):
        if self.contents >= other.capacity:
            self.contents -= other.capacity
            other._fill()
        else:
            other.contents += self.contents
            self._empty()
        self.actions += 1

    def copy(self):
        return bucket(self.name, self.size, _contents=self.contents, _actions=self.actions)

def empty(a, b, rev=False):
    a, b = a.copy(), b.copy()
    if rev:
        b.empty()
    else:
        a.empty()
    return a, b

def fill(a, b, rev=False):
    a, b = a.copy(), b.copy()
    if rev:
        b.fill()
    else:
        a.fill()
    return a, b

def pourin(a, b, rev=False):
    a, b = a.copy(), b.copy()
    if rev:
        b.pourin(a)
    else:
        a.pourin(b)
    return a, b

actions = [
    empty,
    fill,
    pourin,
]

def measure(bucket_one, bucket_two, goal, start_bucket):
    # sanity check
    if goal > bucket_one and goal > bucket_two:
        raise ValueError("goal too large")
    if goal % math.gcd(bucket_one, bucket_two) != 0:
        raise ValueError("goal not a multiple of bucket size gcd")

    one = bucket("one", bucket_one)
    two = bucket("two", bucket_two)

    pairs = {}
    if start_bucket == "one":
        one.fill()
        pairs[(one.contents, two.contents)] = (one, two)
    else:
        two.fill()
        pairs[(two.contents, one.contents)] = (two, one)

    start, other = _measure(pairs, goal)
    
    target = start.name if start.contents == goal else other.name
    remainder = other.contents if start.contents == goal else start.contents

    return start.actions + other.actions, target, remainder

def _measure(pairs, goal):
    while True:
        newpairs = {}
        for pair in pairs.values():
            start, other = pair
            if start.contents == goal or other.contents == goal:
                return pair
                
            for action, rev in ((action, rev) for action in actions for rev in (True, False)):
                newstart, newother = action(start, other, rev=rev)
                if not (newstart.isempty and newother.isfull):
                    # follows rule 3
                    newcontents = (newstart.contents, newother.contents)
                    if newcontents not in newpairs:
                        # is a unique state for the two buckets that we haven't seen before
                        newpairs[newcontents] = (newstart, newother)
                        
        pairs = newpairs
