from sympy import factorial, nan, Piecewise


def binomial_coefficient(n, x):
    return factorial(n) / (factorial(x) * factorial(n - x))


def is_expr_nan(expr):
    # Método para detectar si expr es nan
    # Aquí usamos expr.equals(nan) que devuelve True si expr es nan
    try:
        return expr.equals(nan)
    except:
        return False


def primera_expr_cond(pw):
    if isinstance(pw, Piecewise):
        return primera_expr_cond(pw.args[0][0]), pw.args[0][1]
    else:
        return pw, True  # True como condición trivial si ya no es Piecewise
