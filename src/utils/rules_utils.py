import operator


def string_to_operator(word):
    """
    Parses an English operator string into a numeric symbol.
    :param word: A word representing an English operator
    :return: The equivalent numeric symbol
    """
    operator_map = {
        "exact": "==",
        "equal": "==",
        "equals": "==",
        "greater": ">",
        "less": "<",
        "greater_equal": ">=",
        "less_equal": "<=",
        "not_equal": "!=",
    }

    return operator_map.get(word.lower())


def apply_operation(a, op_string, b):
    """
    Applies the operator `op_string` to `a` and `b`.
    :param a: Any value
    :param op_string: Operator string from which to apply `b`
    :param b: Any value
    :return: A boolean indicating whether the operation is True or False.
    """
    op_map = {
        "==": operator.eq,
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "!=": operator.ne,
    }

    op_word = string_to_operator(op_string)
    if op_word is None:
        raise ValueError(f"Unknown operator: {op_string}")

    operation = op_map.get(op_word)
    if operation is None:
        raise ValueError(f"Unsupported operation: {op_word}")

    return operation(a, b)
