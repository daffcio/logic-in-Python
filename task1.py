def evaluate(expr_in_onp, log_map):
    stack = []
    operators = "|&~>=^"
    for sym in expr_in_onp:
        if sym in operators:
            if sym == "~":
                p = stack.pop()
                stack.append(1 - log_map[p])
                continue
            q = stack.pop()
            p = stack.pop()
            if sym == "|":
                stack.append(log_map[p] or log_map[q])
            elif sym == "&":
                stack.append(log_map[p] and log_map[q])
            elif sym == "~":
                stack.append(p)
                stack.append(1 - log_map[q])
            elif sym == ">":
                stack.append((1 - log_map[p]) or log_map[q])  # p=>q <=> ~p v q
            elif sym == "=":
                stack.append(((1 - log_map[p]) or log_map[q]) and ((1 - log_map[q]) or log_map[p]))  # p<=>q = [(p=>q) and (q=>p)]
            else:
                stack.append((log_map[p] and (1 - log_map[q])) or ((1 - log_map[p]) and log_map[q]))  # p xor q = (p and ~q) or (~p and q)
        else:
            stack.append(sym)
    return stack.pop()


def evaluate_all(variables, all_values, expr_in_onp):
    result = []
    for val in all_values:
        log_map = {var: int(log_val) for var in variables for log_val in val}
        log_map["0"] = 0
        log_map[0] = 0
        log_map["1"] = 1
        log_map[1] = 1
        if evaluate(expr_in_onp, log_map):
            result.append(val)
    return result


def get_priority(op):
    if op == "~":
        return 3
    elif op in ["|", "&", "^"]:
        return 2
    elif op in [">", "="]:
        return 1
    else:
        return 0


def convert_to_onp(expr):
    operators = "|&~>=^"
    stack = ["("]
    result = []
    for elem in expr:
        if elem == "(":
            stack.append(elem)
        elif elem == ")":
            top = stack.pop()
            while top != "(":
                result.append(top)
                top = stack.pop()
        elif elem in operators:
            while stack:
                op_priority = get_priority(elem)
                top = stack.pop()
                if op_priority > get_priority(top) or (op_priority == 2 and op_priority == get_priority(top)) :
                    stack.append(top)
                    stack.append(elem)
                    break
                result.append(top)
        else:
            result.append(elem)
    while stack:
        result.append(stack.pop())
    result.pop()
    return result


def validate(expr):
    logic_words = sorted((set(expr) - set("|&~>=^()")))
    # print(logic_words)
    two_args_operators = "|&>=^"

    step = "next"  # "next", "end", "neg"
    par_count = 0  # licznik nawiasów
    for s in expr:
        if step == "next":
            if s in logic_words:
                step = "end"
            elif s == "(":
                par_count += 1
            elif s == "~":
                step = "neg"
            else:
                return False
        elif step == "end":
            if s in two_args_operators:
                step = "next"
            elif s == ")":
                par_count -= 1
            else:
                return False
        else:
            if s in logic_words:
                step = "end"
            elif s == "(":
                par_count += 1
                step = "next"
            else:
                return False
        if par_count < 0: return False
    return par_count == 0 and step == "end"


def main():
    expr = "~p > q | ~r"
    expr_list = list(filter(lambda x: x not in ["", " "], re.split('([|&~>=^()\W])', expr)))
    expr_in_onp = convert_to_onp(expr_list)

    variables = sorted((set(expr_list) - set("|&~>=^()01")))
    amount_var = len(variables)
    all_values = [(bin(i).split('b')[1]).rjust(amount_var, '0') for i in range(0, int(math.pow(2, amount_var)))]

    true_values = evaluate_all(variables, all_values, expr_in_onp)
    print(true_values)

    # print(all_values)
    # print(amount_var)
    # print(expr_in_onp)
    # print(expr_list)
    # print(validate(expr_list))
    # print(variables)


if __name__ == "__main__":
    import re
    import math
    main()