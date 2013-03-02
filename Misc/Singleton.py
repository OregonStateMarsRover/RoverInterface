class SingletonClass(object):
    _instance = None

    def __new__(self, arg):
        if self._instance is None:
            self.arg = arg
            self._instance = self
        return self._instance

s1 = SingletonClass(1)
print s1.arg

s2 = SingletonClass(2)
print s2.arg
s2.arg = 3

print s1.arg

print s1 == s2

print ""

class NotSingletonClass(object):
    def __init__(self, arg):
        self.arg = arg

n1 = NotSingletonClass(1)
print n1.arg

n2 = NotSingletonClass(2)
print n2.arg
n2.arg = 3

print n1.arg

print n1 == n2
