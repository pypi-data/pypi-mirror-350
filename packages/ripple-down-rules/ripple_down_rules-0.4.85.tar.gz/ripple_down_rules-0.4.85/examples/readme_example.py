from ripple_down_rules.datastructures.dataclasses import CaseQuery
from ripple_down_rules.rdr import SingleClassRDR
from ripple_down_rules.datasets import load_zoo_dataset
from ripple_down_rules.utils import render_tree

all_cases, targets = load_zoo_dataset()

scrdr = SingleClassRDR()

# Fit the SCRDR to the data
case_queries = [CaseQuery(case, 'species', type(target), True, _target=target)
                for case, target in zip(all_cases[:10], targets[:10])]
scrdr.fit(case_queries, animate_tree=True)

# Render the tree to a file
render_tree(scrdr.start_rule, use_dot_exporter=True, filename="scrdr")

cat = scrdr.classify(all_cases[50])
assert cat == targets[50]