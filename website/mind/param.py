import re

class Param:
    pass

class Numeric(Param):
    def __init__(self,_keywords=None, _value=0):
        self.keywords = [re.compile(kw.replace("$","(?P<value>[-+]?[0-9]*[.]?[0-9]+|[0-9]+)")) for kw in _keywords]
        self.value = _value

    def get(self):
        return int(self.value)

    def get_float(self):
        return float(self.value)

    def __str__(self):
        return str(self.value)

class NumArray(Param):
    def __init__(self,_keywords=None, _value = 1):
        self.keywords = [re.compile(kw.replace("$","(?P<value>([1-9][0-9]*,)*[1-9][0-9]*)")) for kw in _keywords]
        self.value = _value

    def get(self):
        return [int(x) for x in str(self.value).split(',')]

    def __str__(self):
        return str(self.value)

class Alias(Param):
    def __init__(self,_keywords=None):
        self.keywords = [re.compile(kw) for kw in _keywords]

    def get(self):
        return self.keywords
