def replace_in_parenthesis(input_str: str, replace: str, replacement: str) -> str:
    """ Return a modified version of <input_str> such that all <replace> within parenthesis are replaced
    with <replacement>

    Precondition: Parenthesis are not nested more than once

    Args:
        input_str: The string to be modified on
        replace: The character to replace within parenthesis
        replacement: The character to replace with

    Returns:
        Modified version of <input_str> such that it follows guidelines set above

    Raises:
        ValueError: Length of <replace> > 1 (it's more than a character)
        ValueError: <Replace> is either '(' or ')'

    Examples:
        >>> replace_commas_in_parenthesis('((,))',",",'a')
        ValueError
        >>> replace_commas_in_parenthesis('(,)', ",", 'a')
        '(a)'
    """
    if len(replace) != 1 or replace == '(' or replace == ')':
        raise ValueError
    open_parenthesis = False
    final_str = str()

    for char in input_str:
        if char == '(' and open_parenthesis:
            raise ValueError
        elif open_parenthesis and char == replace:
            final_str += replacement
        else:
            if char == '(':
                open_parenthesis = True
            elif char == ')':
                open_parenthesis = False
            final_str += char

    return final_str
