import pythonmonkey as pm

wollok = pm.require("./wollok.js")

def execute_repl(expression: str) -> str:
    """Call Wollok REPL with the given value.

    Args:
        expression: executable code in Wollok.

    Returns:
        str: Wollok interpreter output.
    """
    try:
        return wollok.repl(expression)
    except (ValueError, TypeError):
        return "Invalid input"
