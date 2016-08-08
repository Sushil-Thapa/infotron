from pymining import itemmining,assocrules

from mind.param import *
from mind.mind.mind import Mind

class Association(Mind):
    pass

class ItemMine(Association):
    # specify aliases
    name = Alias(['frequent itemset'])
    # EASY.... now declare fields and specify related keywords
    support = Numeric(['with support $'])
    # std_dev = Numeric(['standard deviation $','sd $','std dev $'])

    # write execute function, everything happens here
    def execute(self,data_source):
        import csv
        transactions = []
        with open(data_source, 'r') as f:
            reader = csv.reader(f)
            transactions = list(reader)
        # print(transactions)
        # transactions = [['a', 'b', 'c'], ['b'], ['a'], ['a', 'c', 'd'], ['b', 'c'], ['b', 'c']]
        # print(type(transactions))
        relim_input = itemmining.get_relim_input(transactions)
        report = itemmining.relim(relim_input, min_support = self.support.get())

        result = ""
        for itemset, count in report.items():
            result = result + ", ".join(itemset) + ": " + str(count) + "\n"
        # print(report)
        return result

class AssociationRules(Association):
    # specify aliases
    name = Alias(['find rules'])
    # EASY.... now declare fields and specify related keywords
    support = Numeric(['support $'])
    confidence = Numeric(['confidence $'])

    # write execute function, everything happens here
    def execute(self,data_source):
        import csv
        transactions = []
        with open(data_source, 'r') as f:
            reader = csv.reader(f)
            transactions = list(reader)
        # print(transactions)
        # transactions = [['a', 'b', 'c'], ['b'], ['a'], ['a', 'c', 'd'], ['b', 'c'], ['b', 'c']]
        # print(type(transactions))
        relim_input = itemmining.get_relim_input(transactions)
        item_sets = itemmining.relim(relim_input, min_support = self.support.get())
        rules = assocrules.mine_assoc_rules(item_sets, min_support=self.support.get(), min_confidence=self.confidence.get_float())
        result = ""
        for rule in rules:
            print(rule[0])
            result = result + ", ".join(rule[0]) + " => " + ", ".join(rule[1]) + "\n"
            # result = result + ", ".join(rule[0]) + " => " + ", ".join(rule[1]) + ": " + str(rule[2]) + ", " + str(rule[3]) + "\n"
        # print(report)
        return result