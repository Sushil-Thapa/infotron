from pymining import itemmining, assocrules, perftesting
transactions = perftesting.get_default_transactions()
relim_input = itemmining.get_relim_input(transactions)
item_sets = itemmining.relim(relim_input, min_support=2)
rules = assocrules.mine_assoc_rules(item_sets, min_support=2, min_confidence=0.5)
print(rules)