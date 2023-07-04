import itertools


class CachingIterable:
    def __init__(self, iterable):
        self.iterable = iterable
        self.iter = iter(iterable)
        self.done = False
        self.vals = []

    def __iter__(self):
        if self.done:
            return iter(self.vals)
        return itertools.chain(self.vals, self._gen_iter())

    def _gen_iter(self):
        for new_val in self.iter:
            self.vals.append(new_val)
            yield new_val
        self.done = True
