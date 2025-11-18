import itertools
import pandas as pd

# Define the propositional logic sentences
variables = ['P', 'Q', 'R']

def q_implies_p(p, q, r):
  return not q or p

def p_implies_not_q(p, q, r):
  return not p or not q

def q_or_r(p, q, r):
  return q or r

sentences = {
    'Q implies P': q_implies_p,
    'P implies not(Q)': p_implies_not_q,
    'Q or R': q_or_r
}

# Generate a truth table
truth_values = [True, False]
combinations = list(itertools.product(truth_values, repeat=len(variables)))

truth_table_data = []
for combination in combinations:
  p, q, r = combination
  row = {'P': p, 'Q': q, 'R': r}
  for sentence_name, sentence_func in sentences.items():
    row[sentence_name] = sentence_func(p, q, r)
  truth_table_data.append(row)

# Convert the list of dictionaries to a pandas DataFrame for better visualization
truth_table_df = pd.DataFrame(truth_table_data)

# Evaluate the knowledge base (KB)
sentence_columns = list(sentences.keys())
truth_table_df['KB is True'] = truth_table_df[sentence_columns].all(axis=1)

models = truth_table_df[truth_table_df['KB is True']]

# Check for entailment
kb_entails_r = models['R'].all()
kb_entails_r_implies_p = (models['R'].apply(lambda x: not x) | models['P']).all()
kb_entails_q_implies_r = (models['Q'].apply(lambda x: not x) | models['R']).all()


# Display the results
print("Truth Table:")
display(truth_table_df)

print("\nModels where KB is True:")
display(models)

print("\nEntailment Results:")
print(f"KB entails R: {kb_entails_r}")
print(f"KB entails R implies P: {kb_entails_r_implies_p}")
print(f"KB entails Q implies R: {kb_entails_q_implies_r}")
