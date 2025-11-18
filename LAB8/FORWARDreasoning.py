from collections import deque, namedtuple


def is_variable(x):
    return isinstance(x, str) and x and x[0].islower()

def atom_str(atom):
    pred, args = atom
    return f"{pred}({', '.join(args)})"

# Substitute according to a mapping (var->constant)
def substitute_atom(atom, subs):
    pred, args = atom
    new_args = []
    for a in args:
        if is_variable(a) and a in subs:
            new_args.append(subs[a])
        else:
            new_args.append(a)
    return (pred, tuple(new_args))

# Unification for single terms (simple: variable -> constant only needed here)
def unify_terms(t1, t2, subs):
    # t1, t2 are strings; subs is dict var->const
    t1_val = subs.get(t1, t1) if is_variable(t1) else t1
    t2_val = subs.get(t2, t2) if is_variable(t2) else t2
    if t1_val == t2_val:
        return subs
    # if t1 is variable, bind it
    if is_variable(t1):
        # don't allow binding variable to another variable in this simple scenario; we'll allow var->const only
        subs2 = dict(subs)
        subs2[t1] = t2_val
        return subs2
    if is_variable(t2):
        subs2 = dict(subs)
        subs2[t2] = t1_val
        return subs2
    return None

def unify_atoms(a1, a2):
    # a1,a2 are atoms with same predicate name and same arity
    p1, args1 = a1
    p2, args2 = a2
    if p1 != p2 or len(args1) != len(args2):
        return None
    subs = {}
    for x, y in zip(args1, args2):
        subs = unify_terms(x, y, subs)
        if subs is None:
            return None
    return subs

# Horn rule: head :- body1, body2, ...
Rule = namedtuple("Rule", ["head", "body"])  # head: atom, body: list of atoms (may contain variables)

def forward_chain(rules, facts, query):
    # rules: list of Rule where variables are lowercase strings like 'x'
    # facts: set of ground atoms (constants only)
    # query: atom (ground) to prove
    inferred = set(facts)
    agenda = deque(facts)  # facts to be used to try rules
    proof = {}  # store how each inferred fact was derived: fact -> (rule, substitutions, premises)
    
    while agenda:
        fact = agenda.popleft()
        # try every rule: for each rule, try to match a body literal with this fact, then check remaining body literals
        for rule in rules:
            # For each body literal in the rule, attempt to unify it with the current fact
            for i, body_lit in enumerate(rule.body):
                # rename variables in rule to avoid accidental capture (standardize-apart)
                # We'll append a unique suffix for this attempt
                suffix = f"__{id(fact)}_{i}"
                def rename_atom(atom):
                    pred, args = atom
                    new_args = []
                    for a in args:
                        if is_variable(a):
                            new_args.append(a + suffix)
                        else:
                            new_args.append(a)
                    return (pred, tuple(new_args))
                renamed_body = [rename_atom(b) for b in rule.body]
                renamed_head = rename_atom(rule.head)
                
                target = renamed_body[i]
                subs = unify_atoms(target, fact)
                if subs is None:
                    continue
                # Now we have a substitution for one body literal; check other body literals
                all_ok = True
                premises = [fact]  # start with matched fact
                # For each other literal, try to find a matching ground fact in inferred
                for j, other in enumerate(renamed_body):
                    if j == i:
                        continue
                    # we need to find some ground fact in inferred that unifies with 'other' under subs
                    matched = False
                    for candidate in inferred:
                        s2 = unify_atoms(other, candidate)
                        if s2 is None:
                            continue
                        # merge s2 with subs (simple merge; prefer earlier bindings)
                        merged = dict(subs)
                        conflict = False
                        for k,v in s2.items():
                            if k in merged and merged[k] != v:
                                conflict = True; break
                            merged[k] = v
                        if conflict:
                            continue
                        subs = merged
                        premises.append(candidate)
                        matched = True
                        break
                    if not matched:
                        all_ok = False
                        break
                if not all_ok:
                    continue
                # we can fire the rule with substitution 'subs' to produce head
                new_head = substitute_atom(renamed_head, subs)
                if new_head not in inferred:
                    inferred.add(new_head)
                    agenda.append(new_head)
                    proof[new_head] = (rule, subs, tuple(premises))
                    # check query
                    if new_head == query:
                        return True, inferred, proof
    return (query in inferred), inferred, proof

# Build KB for Marcus
facts = {
    ("Man", ("Marcus",)),
    ("Pompeian", ("Marcus",))
}

rules = [
    Rule(head=("Roman", ("x",)), body=[("Pompeian", ("x",))]),
    Rule(head=("Loyal", ("x",)), body=[("Roman", ("x",))]),
    Rule(head=("Person", ("x",)), body=[("Man", ("x",))]),
    Rule(head=("Mortal", ("x",)), body=[("Person", ("x",))])
]

query = ("Mortal", ("Marcus",))

proved, inferred, proof = forward_chain(rules, facts, query)

print("Forward chaining proof result for query Mortal(Marcus):", proved)
print("\nAll inferred facts:")
for f in sorted(inferred):
    print(" -", atom_str(f))

if proved:
    print("\nProof trace (derived facts and how):")
    # walk backwards from query using the proof dict
    def show_derivation(fact, depth=0):
        indent = "  " * depth
        if fact not in proof:
            print(indent + f"{atom_str(fact)}  (given)")
            return
        rule_used, subs_used, premises = proof[fact]
        head = rule_used.head
        print(indent + f"{atom_str(fact)}  (derived via {atom_str(head)} :- {', '.join(atom_str(b) for b in rule_used.body)})")
        print(indent + f"  substitution: {subs_used}")
        for p in premises:
            show_derivation(p, depth+1)
    show_derivation(query)