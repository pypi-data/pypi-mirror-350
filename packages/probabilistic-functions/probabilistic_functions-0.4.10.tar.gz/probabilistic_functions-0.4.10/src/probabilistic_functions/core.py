from sympy import (
    symbols,
    sympify,
    lambdify,
    factorial,
    simplify,
    factor,
    UnevaluatedExpr,
)
import warnings
from sympy import pretty
from sympy import (
    exp,
    sqrt,
    pi,
    latex,
    integrate,
    S,
    summation,
    diff,
    limit,
    Max,
    Min,
    binomial,
    gamma,
    beta,
    log,
    uppergamma,
    erf,
    Piecewise,
)
from sympy import oo
from sympy import pprint
import sympy
import matplotlib.pyplot as plt
import math
import numpy as np
from itertools import product
from typing import Callable, Dict, List, Tuple, Optional, Union
from IPython.display import display, Math


class Bernulli:
    def __init__(self):
        self.p, self.x = symbols("p x")
        self._mode = "Discrete"
        self.t = symbols("t")
        self._support = {0, 1}

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Bernoulli distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def get_mode(self) -> str:
        return self._mode

    @property
    def is_fuction(self) -> bool:
        return True

    @property
    def get_soport(self) -> set:
        return self._support

    @property
    def get_name(self) -> str:
        return "Bernoulli"

    def fp(self):
        return pow(self.p, self.x) * pow(1 - self.p, 1 - self.x)

    def replace(self, parameters, fuction: str = "fp"):
        if parameters["p"] < 0 or parameters["p"] > 1:
            raise ValueError("p must be between 0 and 1")
        if fuction == "fp":
            return self.fp().subs(parameters)
        elif fuction == "fda":
            return self.fda().subs(parameters)
        elif fuction == "fgm":
            return self.FGM().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        return self.p * exp(self.t) + 1 - self.p

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")

        return diff(self.FGM(), self.t, n).subs(self.t, 0).simplify()


class Binomial:
    def __init__(self):
        self.p, self.x, self.n = symbols("p x n")
        self.t = symbols("t")
        self._mode = "Discrete"
        self._support = None

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Binomial distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Binomial"

    def fp(self):
        return (
            (binomial(self.n, self.x))
            * pow(self.p, self.x)
            * pow(1 - self.p, self.n - self.x)
        )

    def replace(self, parameters, fuction: str = "fp"):
        if parameters["p"] < 0 or parameters["p"] > 1:
            raise ValueError("p must be between 0 and 1")
        if parameters["n"] <= 0:
            raise ValueError("n must be greater than 0")
        if fuction == "fp":
            return self.fp().subs(parameters)
        elif fuction == "fda":
            return self.fda().subs(parameters)
        elif fuction == "fgm":
            return self.FGM().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        return pow(((self.p * exp(self.t)) + 1 - self.p), self.n)

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        return diff(self.FGM(), self.t, n).subs(self.t, 0).simplify()


class Geometric:
    def __init__(self):

        self.p, self.x = symbols("p x")
        self.t = symbols("t")
        self._mode = "Discrete"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Geometric distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Geometric"

    def fp(self):
        return pow(1 - self.p, self.x - 1) * self.p

    def replace(
        self,
        parameters,
        fuction: str = "fp",
    ):
        if parameters["p"] < 0 or parameters["p"] > 1:
            raise ValueError("p must be between 0 and 1")
        if fuction == "fp":
            return self.fp().subs(parameters)
        elif fuction == "fda":
            return self.fda().subs(parameters)
        elif fuction == "fgm":
            return self.FGM().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        return (self.p * exp(self.t)) / (1 - (1 - self.p) * exp(self.t))

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        return diff(self.FGM(), self.t, n).subs(self.t, 0).simplify()


class HyperGeometric:
    def __init__(self):
        self.N, self.n, self.K, self.x = symbols("N n K x")
        self.t = symbols("t")
        self._mode = "Discrete"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large HyperGeometric distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(UnevaluatedExpr(self.n * self.K / self.N))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.n * self.K / self.N) * ((self.N - self.K) / self.N) * ((self.N - self.n) / (self.N - 1)))}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Hypergeometric"

    def fp(self):
        return (
            binomial(self.K, self.x) * binomial(self.N - self.K, self.n - self.x)
        ) / (binomial(self.N, self.n))

    def replace(self, parameters, fuction: str = "fp"):
        if parameters["N"] < 0:
            raise ValueError("N must be greater than 0")
        if parameters["n"] < 0:
            raise ValueError("n must be greater than 0")
        if parameters["n"] > parameters["N"]:
            raise ValueError("n must be less than N")
        if fuction == "fp":
            return self.fp().subs(parameters)
        elif fuction == "fda":
            return self.fda().subs(parameters)
        elif fuction == "fgm":
            return self.FGM().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        print("warning: It does not have a simple closed-form expression.")
        return summation(
            exp(self.t * self.x) * self.fp(),
            (self.x, Max(0, self.n - (self.N - self.K)), Min(self.n, self.K)),
        )

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        return diff(self.FGM(), self.t, n).subs(self.t, 0).simplify()


class Poisson:
    def __init__(self):
        self.l, self.x = symbols("l x")
        self._mode = "Discrete"
        self.t = symbols("t")

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Poisson distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Poisson"

    def fp(self):
        return pow(self.l, self.x) * exp(-self.l) / factorial(self.x)

    def replace(self, parameters, fuction: str = "fp"):
        if parameters["l"] < 0:
            raise ValueError("l must be greater than 0")
        if fuction == "fp":
            return self.fp().subs(parameters)
        elif fuction == "fda":
            return self.fda().subs(parameters)
        elif fuction == "fgm":
            return self.FGM().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        return exp(self.l * (exp(self.t) - 1))

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        return diff(self.FGM(), self.t, n).subs(self.t, 0).simplify()


class Uniform:
    def __init__(self):
        self.a, self.b = symbols("a b")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Uniform distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1).factor())} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).factor())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Uniform"

    def fdp(self):
        return 1 / (self.b - self.a)

    def replace(self, parameters, fuction: str = "fdp"):
        if parameters["a"] >= parameters["b"]:
            raise ValueError("a must be less than b")
        if fuction == "fdp":
            return self.fdp().subs(parameters)
        elif fuction == "fda":
            return self.fda().subs(parameters)
        elif fuction == "fgm":
            return self.FGM().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        return (exp(self.t * self.b) - exp(self.t * self.a)) / (
            self.t * (self.b - self.a)
        )

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.fdp(), (self.x, self.a, self.b))
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Exponential:
    def __init__(self, l: Optional[float] = None):
        if l is not None:
            self.l = l

        else:
            self.l = symbols("l", real=True, positive=True)
            self.l_dummy = symbols("l")
        self.x = symbols("x")
        self.t = symbols("t", positive=True)

        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Exponential distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Exponential"

    def fdp(self):
        return self.l * exp(-self.l * self.x)

    def replace(
        self,
        parameters,
        change_l: Optional[bool] = False,
        erase_l: Optional[bool] = False,
        fuction: str = "fdp",
    ):
        if parameters["l"] < 0:
            raise ValueError("l must be greater than 0")
        if fuction == "fdp":
            return self.fdp().subs(self.l, self.l_dummy).subs(parameters)
        elif fuction == "fda":
            return self.fda().subs(self.l, self.l_dummy).subs(parameters)
        elif fuction == "fgm":
            return self.FGM().subs(self.l, self.l_dummy).subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        return self.l / (self.l - self.t)

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.fdp(), (self.x, 0, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Norm:
    def __init__(self):
        self.x = symbols("x")
        self.v = symbols("v", real=True, positive=True)
        self.v_dummy = symbols("v")
        self.m = symbols("m", real=True)
        self.m_dummy = symbols("m")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Normal distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Normal"

    def fdp(self):
        return (1 / sqrt(2 * pi * self.v)) * exp(
            (-((self.x - self.m) ** 2)) / (2 * (self.v))
        )

    def replace(self, parameters, fuction: str = "fdp"):
        if parameters["v"] < 0:
            raise ValueError("v must be greater than 0")
        if fuction == "fdp":
            return (
                self.fdp()
                .subs({self.m: self.m_dummy, self.v: self.v_dummy})
                .subs(parameters)
            )
        elif fuction == "fda":
            return (
                self.fda()
                .subs({self.m: self.m_dummy, self.v: self.v_dummy})
                .subs(parameters)
            )
        elif fuction == "fgm":
            return (
                self.FGM()
                .subs({self.m: self.m_dummy, self.v: self.v_dummy})
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        return exp(self.m * self.t + 0.5 * (self.v) * (self.t**2))

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.fdp(), (self.x, -oo, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Weibull:
    def __init__(self):
        self.b, self.a = symbols("b a", real=True, positive=True)
        self.b_dummy = symbols("b")
        self.a_dummy = symbols("a")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Weibull distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).factor())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Weibull"

    def fdp(self):
        return (
            self.b
            * self.a
            * ((self.b * self.x) ** (self.a - 1))
            * exp(-((self.b * self.x) ** self.a))
        )

    def replace(self, parameters, function: str = "fdp"):
        if parameters["b"] < 0:
            raise ValueError("b must be greater than 0")
        if parameters["a"] < 0:
            raise ValueError("a must be greater than 0")

        if function == "fdp":
            return (
                self.fdp()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        elif function == "fda":
            return (
                self.fda()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        elif function == "fgm":
            return (
                self.FGM()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        integral_expr = integrate(exp(self.t * self.x) * self.fdp(), (self.x, 0, oo))
        return integral_expr.simplify()

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.fdp(), (self.x, 0, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Gamma:
    def __init__(self):
        self.a, self.b = symbols("a b", real=True, positive=True)
        self.a_dummy = symbols("a")
        self.b_dummy = symbols("b")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Gamma distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    def fdp(self):
        return (
            (self.b**self.a / gamma(self.a))
            * self.x ** (self.a - 1)
            * exp(-self.b * self.x)
        )

    def replace(self, parameters, function: str = "fdp"):
        if parameters["a"] < 0:
            raise ValueError("a must be greater than 0")
        if parameters["b"] < 0:
            raise ValueError("b must be greater than 0")
        if function == "fdp":
            return (
                self.fdp()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        elif function == "fda":
            return (
                self.fda()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        elif function == "fgm":
            return (
                self.FGM()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        return (self.b / (self.b - self.t)) ** self.a

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.fdp(), (self.x, 0, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Beta:
    def __init__(self):
        self.a, self.b = symbols("a b", real=True, positive=True)
        self.a_dummy = symbols("a")
        self.b_dummy = symbols("b")
        self.x = symbols("x")
        self.r = symbols("r")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Beta distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).factor())}
        """
        display(Math(expr))

    def fdp(self):
        return (
            (1 / beta(self.a, self.b))
            * (self.x ** (self.a - 1))
            * ((1 - self.x) ** (self.b - 1))
        )

    def replace(self, parameters, function: str = "fdp"):
        if parameters["a"] < 0:
            raise ValueError("a must be greater than 0")
        if parameters["b"] < 0:
            raise ValueError("b must be greater than 0")
        if function == "fdp":
            return (
                self.fdp()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        elif function == "fda":
            return (
                self.fda()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        elif function == "fgm":
            return (
                self.FGM()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        print(
            "warning: It does not have a simple closed-form expression. Then using the explicit form"
        )
        return (gamma(self.a + self.r) * gamma(self.a + self.b)) / (
            gamma(self.a) * gamma(self.a + self.b + self.r)
        )

    def calculate_moments(self, n: int, mode: str = "diff"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.fdp(), (self.x, 0, 1)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = self.FGM().subs(self.r, n).simplify()
        return E.simplify()


class LogNormal:
    def __init__(self):
        self.m, self.v = symbols("m v", real=True)
        self.m_dummy = symbols("m")
        self.v_dummy = symbols("v")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Log-Normal distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "LogNormal"

    def fdp(self):
        return (1 / (self.x * sqrt(2 * pi * self.v))) * exp(
            -((log(self.x) - self.m) ** 2) / (2 * self.v)
        )

    def replace(self, parameters, function: str = "fdp"):
        if parameters["sigma"] < 0:
            raise ValueError("sigma must be greater than 0")
        if function == "fdp":
            return (
                self.fdp()
                .subs({self.m: self.v_dummy, self.v: self.v_dummy})
                .subs(parameters)
            )
        elif function == "fda":
            return (
                self.fda()
                .subs({self.m: self.v_dummy, self.v: self.v_dummy})
                .subs(parameters)
            )
        elif function == "fgm":
            return (
                self.FGM()
                .subs({self.m: self.m_dummy, self.v: self.v_dummy})
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        print("warning: It does not have a simple closed-form expression.")
        return exp(self.t * self.m + 0.5 * self.t**2 * self.v)

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")

        return self.FGM().subs(self.t, n).simplify()


class Gumbel:
    def __init__(self):
        self.m, self.b = symbols("m", real=True), symbols("b", real=True, positive=True)
        self.m_dummy = symbols("m")
        self.b_dummy = symbols("b")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Gumbel distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Gumbel"

    def fdp(self):
        return (
            (1 / self.b)
            * exp((self.x - self.m) / self.b)
            * exp(-exp((self.x - self.m) / self.b))
        )

    def replace(self, parameters, function: str = "fdp"):
        if parameters["b"] < 0:
            raise ValueError("b must be greater than 0")
        if function == "fdp":
            return (
                self.fdp()
                .subs({self.m: self.m_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        elif function == "fda":
            return (
                self.fda()
                .subs({self.m: self.m_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        elif function == "fgm":
            return (
                self.FGM()
                .subs({self.m: self.m_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        return gamma(1 - self.b * self.t) * exp(self.m * self.t)

    def calculate_moments(self, n: int, mode: str = "diff"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            # z = (x-m)/b
            self.z = symbols("z", real=True)
            new_fdp = (self.b * self.z + self.m) ** n * exp(self.z - exp(self.z))
            E = integrate(new_fdp, (self.z, -oo, oo), meijerg=True)
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Pareto:
    def __init__(self, type: int = 1):
        self.type = type
        self.t = symbols("t")
        self._mode = "Continuous"
        self.x_m, self.a, self.b, self.l = symbols(
            "x_m a b l", real=True, positive=True
        )
        self.x_m_dummy = symbols("x_m")
        self.a_dummy = symbols("a")
        self.b_dummy = symbols("b")
        self.l_dummy = symbols("l")
        self.x = symbols("x")
        self.y = symbols("y", real=True, positive=True)
        self.m = symbols("m", real=True, positive=True)
        self.m_dummy = symbols("m")
        self.y_dummy = symbols("y")
        self.x_dummy = symbols("x")
        self.r = symbols("r", real=True, positive=True)
        if self.type not in [1, 2, 6]:
            raise ValueError("Invalid type. Type must be 1, 2 or 6")

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Pareto distribution}} \quad \textbf{{\Large {self.type}}}\\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return "Continuous"

    @property
    def get_name(self) -> str:
        return f"Pareto {self.type}"

    def fdp(self):
        if self.type == 1:
            return (self.a * self.x_m**self.a) / self.x ** (self.a + 1)

        elif self.type == 2:
            return (self.a / self.l) * (1 + self.x / self.l) ** -(self.a + 1)

        elif self.type == 6:
            return (1 / self.l) * (1 + self.y * ((self.x - self.m) / self.l)) ** (
                -1 / self.y - 1
            )

    def replace(self, parameters, function: str = "fdp"):
        if self.type == 1:
            if parameters["x_m"] <= 0:
                raise ValueError("x_m must be greater than 0")
            if parameters["a"] <= 0:
                raise ValueError("a must be greater than 0")

        elif self.type == 2:
            if parameters["l"] <= 0:
                raise ValueError("l must be greater than 0")
            if parameters["a"] <= 0:
                raise ValueError("a must be greater than 0")

        elif self.type == 6:
            if parameters["l"] <= 0:
                raise ValueError("l must be greater than 0")
            if parameters["y"] <= 0:
                raise ValueError("y must be greater than 0")

        if function == "fdp":
            return (
                self.fdp()
                .subs(
                    {self.x: self.x_dummy, self.a: self.a_dummy, self.l: self.l_dummy}
                )
                .subs(parameters)
            )
        elif function == "fda":
            return (
                self.fda()
                .subs(
                    {self.x: self.x_dummy, self.a: self.a_dummy, self.l: self.l_dummy}
                )
                .subs(parameters)
            )
        elif function == "fgm":
            return (
                self.FGM()
                .subs(
                    {self.x: self.x_dummy, self.a: self.a_dummy, self.l: self.l_dummy}
                )
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        if self.type == 1:

            warnings.warn(
                "It does not have a simple closed-form expression. Then using the explicit form"
            )
            self.r = symbols("r")
            return (self.a * self.x_m**self.r) / (self.a - self.r)
        elif self.type == 2:
            return self.l**self.r * (
                gamma(self.r + 1) * gamma(self.a - self.r) / gamma(self.a)
            )
        elif self.type == 6:
            return summation(
                binomial(self.r, self.x)
                * self.m ** (self.r - self.x)
                * self.l ** (self.x)
                * ((gamma(1 - self.x * self.y)) / ((-self.y) ** self.x)),
                (self.x, 1, self.r),
            )

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            if self.type == 1:
                E = Piecewise(
                    (
                        integrate(pow(self.x, n) * self.fdp(), (self.x, self.x_m, oo)),
                        self.a > n,
                    ),
                    (sympy.nan, True),
                )
            elif self.type == 2 or self.type == 6:
                E = Piecewise(
                    (
                        integrate(pow(self.x, n) * self.fdp(), (self.x, 0, oo)),
                        self.a > n,
                    ),
                    (sympy.nan, True),
                )

        elif mode == "diff":
            if self.type == 1 or self.type == 2:
                E = Piecewise(
                    (self.FGM().subs(self.r, n).simplify(), self.a > n),
                    (sympy.nan, True),
                )
            elif self.type == 6:
                E = Piecewise(
                    (
                        self.m**n + (self.FGM().subs(self.r, n)).doit().simplify(),
                        self.y < 1 / n,
                    ),
                    (sympy.nan, True),
                )

        return E.simplify()


class Birnbaum_Saunders:
    def __init__(self):
        self.m, self.a, self.b = symbols("m a b ", real=True)
        self.m_dummy = symbols("m")
        self.a_dummy = symbols("a")
        self.b_dummy = symbols("b")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Birnbaum-Saunders distribution}} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \text{{"Siendo Phi:"}} \quad {latex(self.Phi)} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Birnbaum-Saunders"

    def fdp(self):
        return (
            (1 / (2 * self.a * self.x * sqrt(2 * pi)))
            * (sqrt(self.b / self.x) + sqrt(self.x / self.b))
            * exp(
                -(1 / (2 * self.a**2))
                * (sqrt(self.x / self.b) - sqrt(self.b / self.x)) ** 2
            )
        )

    def replace(self, parameters, function: str = "fdp"):
        if parameters["a"] < 0:
            raise ValueError("a must be greater than 0")
        if parameters["b"] < 0:
            raise ValueError("b must be greater than 0")
        if function == "fdp":
            return (
                self.fdp()
                .subs(
                    {self.m: self.m_dummy, self.a: self.a_dummy, self.b: self.b_dummy}
                )
                .subs(parameters)
            )
        elif function == "fda":
            return (
                self.fda()
                .subs(
                    {self.m: self.m_dummy, self.a: self.a_dummy, self.b: self.b_dummy}
                )
                .subs(parameters)
            )
        elif function == "fgm":
            return (
                self.FGM()
                .subs(
                    {self.m: self.m_dummy, self.a: self.a_dummy, self.b: self.b_dummy}
                )
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        self.Phi = lambda y: (1 + erf(y / sqrt(2))) / 2
        inside_sqrt = sqrt(1 + (2 * self.a**2 * self.t) / beta)
        return exp(self.t * beta / 2) * self.Phi((inside_sqrt - 1) / self.a) + exp(
            -self.t * beta / 2
        ) * self.Phi(-(inside_sqrt + 1) / self.a)

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.fdp(), (self.x, 0, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Burr:
    def __init__(self, type: int = 7):
        self.type = type
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"
        if type == 1:
            self.a, self.b, self.l = symbols("a b l", real=True, positive=True)
            self.a_dummy = symbols("a")
            self.b_dummy = symbols("b")
            self.l_dummy = symbols("l")
        elif type == 7:
            self.a, self.b, self.c, self.l = symbols(
                "a b c l", real=True, positive=True
            )
            self.c_dummy = symbols("c")
            self.l_dummy = symbols("l")
            self.a_dummy = symbols("a")
            self.b_dummy = symbols("b")
        else:
            raise ValueError("Invalid type. Type only avilable 1 or 6")

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Burr distribution Type}} \quad {self.type} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).factor())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return f"Burr {self.type}"

    def fdp(self):
        if self.type == 1:
            return (
                (self.a * self.b / self.l)
                * ((self.x / self.l) ** (self.a * self.b - 1))
                * (1 + (self.x / self.l) ** self.a) ** (-self.b - 1)
            )
        elif self.type == 7:
            return (
                ((self.a * self.c) / self.l)
                * (self.x / self.l) ** (self.a - 1)
                * (1 + (self.x / self.l) ** self.a) ** (-self.c - 1)
            )

    def replace(self, parameters, function: str = "fdp"):
        if self.type == 1:
            if parameters["a"] < 0:
                raise ValueError("a must be greater than 0")
            if parameters["b"] < 0:
                raise ValueError("b must be greater than 0")
            if parameters["l"] < 0:
                raise ValueError("l must be greater than 0")
        elif self.type == 7:
            if parameters["c"] < 0:
                raise ValueError("c must be greater than 0")
            if parameters["l"] < 0:
                raise ValueError("l must be greater than 0")

        if function == "fdp":
            return (
                self.fdp()
                .subs(
                    {self.x: self.x_dummy, self.a: self.a_dummy, self.l: self.l_dummy}
                )
                .subs(parameters)
            )
        elif function == "fda":
            return (
                self.fda()
                .subs(
                    {self.x: self.x_dummy, self.a: self.a_dummy, self.l: self.l_dummy}
                )
                .subs(parameters)
            )
        elif function == "fgm":
            return (
                self.FGM()
                .subs(
                    {self.x: self.x_dummy, self.a: self.a_dummy, self.l: self.l_dummy}
                )
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        self.r = symbols("r")
        print(
            "warning: It does not have a simple closed-form expression. Then using the explicit form"
        )
        if self.type == 1:
            return (
                self.l**self.r
                * gamma(self.b - self.r / self.a)
                * gamma(1 + self.r / self.a)
                / gamma(self.b)
            )
        elif self.type == 7:
            return self.l**self.r * (
                (gamma(1 + (self.r / self.a)) * gamma(self.c - self.r / self.a))
                / (gamma(self.c))
            )

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.fdp(), (self.x, 0, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = self.FGM().subs(self.r, n).simplify()
        return E.simplify()


class Lindley:
    def __init__(self, type: int = 1):
        self.type = type
        if self.type not in [1, 2]:
            raise ValueError("Invalid type. Type only avilable 1 or 2")
        self.p = symbols("p", real=True, positive=True)
        self.p_dummy = symbols("p")
        self.t = symbols("t")
        self.x = symbols("x")
        self._mode = "Continuous"

        if self.type == 2:
            self.a = symbols("a", real=True, positive=True)
            self.a_dummy = symbols("a")
            self.y = symbols("y", real=True, positive=True)
            self.y_dummy = symbols("y")

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Lindley distribution}}\\[6pt]
        \text{{Function probability:}} \quad {latex(self.fdp())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).factor())}
        """
        display(Math(expr))

    @property
    def is_fuction(self):
        return True

    @property
    def get_mode(self):
        return self._mode

    @property
    def get_name(self) -> str:
        return "Lindley"

    def fdp(self):
        if self.type == 1:
            return (self.p**2 / (1 + self.p)) * exp(-self.p * self.x) * (1 + self.x)
        elif self.type == 2:
            return (
                self.p**2
                * (self.p * self.x) ** (self.a - 1)
                * (self.a + self.y * self.x)
                * exp(-self.p * self.x)
            ) / ((self.y + self.p) * gamma(self.a + 1))

    def replace(self, parameters, function: str = "fdp"):
        if parameters["p"] < 0:
            raise ValueError("p must be greater than 0")
        if self.type == 3:
            if parameters["l"] < 0:
                raise ValueError("l must be greater than 0")
        if function == "fdp":
            return self.fdp().subs({self.p: self.p_dummy}).subs(parameters)
        elif function == "fda":
            return self.fda().subs({self.p: self.p_dummy}).subs(parameters)
        elif function == "fgm":
            return self.FGM().subs({self.p: self.p_dummy}).subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def FGM(self):
        if self.type == 1:
            return (self.p**2 / (self.p + 1)) * (
                1 / (self.p - self.t) + 1 / (self.p - self.t) ** 2
            )
        elif self.type == 2:
            return (self.p ** (self.a + 1) / (self.y + self.p)) * (
                1 / (self.p - self.t) ** self.a
                + self.y / (self.p - self.t) ** (self.a + 1)
            )

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.fdp(), (self.x, 0, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


if __name__ == "__main__":
    from probabilistic_functions.utils import (
        binomial_coefficient,
        is_expr_nan,
        primera_expr_cond,
    )

    p = Pareto()
    p()
else:
    from .utils import binomial_coefficient, is_expr_nan, primera_expr_cond
