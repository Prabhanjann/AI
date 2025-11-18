import re

# Utility: parse the expression into function/operator and arguments
def parse(expr):
    expr = expr.strip()
    if '(' not in expr:
        return expr, []
    func = expr[:expr.index('(')].strip()
    args = expr[expr.index('(')+1:-1]
    args = [a.strip() for a in split_args(args)]
    return func, args

# Split arguments correctly (handles nested brackets)
def split_args(args_str):
    args, level, start = [], 0, 0
    for i, ch in enumerate(args_str):
        if ch == ',' and level == 0:
            args.append(args_str[start:i].strip())
            start = i + 1
        elif ch == '(':
            level += 1
        elif ch == ')':
            level -= 1
    args.append(args_str[start:].strip())
    return args

# Apply substitution to an expression
def substitute(expr, subs):
    for var, val in subs.items():
        expr = re.sub(rf'\b{var}\b', val, expr)
    return expr

# Check if variable occurs inside term (Occurs check)
def occurs_check(var, term):
    if var == term:
        return True
    if '(' not in term:
        return False
    _, args = parse(term)
    return any(occurs_check(var, arg) for arg in args)

# Unification algorithm
def unify(e1, e2, subs=None):
    if subs is None:
        subs = {}

    e1 = substitute(e1, subs)
    e2 = substitute(e2, subs)

    if e1 == e2:
        return subs

    f1, args1 = parse(e1)
    f2, args2 = parse(e2)

    # Case 1: Both are compound terms
    if args1 and args2:
        if f1 != f2 or len(args1) != len(args2):
            print(f"❌ Function symbols or arity mismatch: {f1} vs {f2}")
            return None
        for a1, a2 in zip(args1, args2):
            subs = unify(a1, a2, subs)
            if subs is None:
                return None
        return subs

    # Case 2: Variable binding
    elif e1.islower() and e1.isalpha(): # e1 is variable
        if occurs_check(e1, e2):
            print(f"❌ Occurs check failed: {e1} occurs in {e2}")
            return None
        subs[e1] = e2
        return subs
    elif e2.islower() and e2.isalpha(): # e2 is variable
        if occurs_check(e2, e1):
            print(f"❌ Occurs check failed: {e2} occurs in {e1}")
            return None
        subs[e2] = e1
        return subs

    # Otherwise mismatch
    else:
        print(f"❌ Cannot unify {e1} with {e2}")
        return None

# --- MAIN PROGRAM ---
print("=== Unification Algorithm ===")
expr1 = input("Enter first expression: ").strip()
expr2 = input("Enter second expression: ").strip()

result = unify(expr1, expr2)

if result:
    print("\n✅ Unification Successful!")
    print("Substitutions:")
    for k, v in result.items():
        print(f" {k} / {v}")
else:
    print("\n❌ Unification Failed.")
