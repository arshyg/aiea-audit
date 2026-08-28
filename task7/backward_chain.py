from production import AND, OR, NOT, PASS, FAIL, IF, THEN, match, populate, simplify, variables
from data import zookeeper_rules, zoo_data


def backchain_to_goal_tree(rules, hypothesis):
    tree = [hypothesis]

    for rule in rules:
        bindings = match(rule.consequent(), hypothesis)
        if bindings is not None:
            antecedent = populate(rule.antecedent(), bindings)

            if isinstance(antecedent, AND):
                goals = [backchain_to_goal_tree(rules, subgoal) for subgoal in antecedent]
                tree.append(AND(*goals))
            elif isinstance(antecedent, OR):
                goals = [backchain_to_goal_tree(rules, subgoal) for subgoal in antecedent]
                tree.append(OR(*goals))
            else:
                tree.append(backchain_to_goal_tree(rules, antecedent))

    return simplify(OR(*tree))


def evaluate_goal_tree(tree, facts):
    facts = set(facts)
    if isinstance(tree, AND):
        return all(evaluate_goal_tree(t, facts) for t in tree)
    elif isinstance(tree, OR):
        return any(evaluate_goal_tree(t, facts) for t in tree)
    elif isinstance(tree, NOT):
        return not evaluate_goal_tree(tree[0], facts)
    else:
        return tree in facts


if __name__ == "__main__":
    tree = backchain_to_goal_tree(zookeeper_rules, 'mark is a penguin')
    print(tree)
    print()
    result = evaluate_goal_tree(tree, zoo_data)
    print(f"Query result: {result}")

    from data import course_rules, course_data

    tree2 = backchain_to_goal_tree(course_rules, 'sluggy eligible-for cs201')
    print(tree2)
    print()
    result2 = evaluate_goal_tree(tree2, course_data)
    print(f"Query result: {result2}")

    print()

    tree3 = backchain_to_goal_tree(course_rules, 'bob eligible-for cs102')
    print(tree3)
    print()
    result3 = evaluate_goal_tree(tree3, course_data)
    print(f"Query result: {result3}")
