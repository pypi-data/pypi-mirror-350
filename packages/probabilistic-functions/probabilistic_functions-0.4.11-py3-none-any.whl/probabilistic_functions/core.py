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
    log,
    uppergamma,
    erf,
    Piecewise,
    floor,
    Contains,
    FiniteSet,
    Naturals,
    Interval,
    Range,
)
from sympy.stats import Normal as Norm
from sympy.stats import E

from sympy import beta as beta_func

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
        self.p = symbols("theta", real=True, positive=True)
        self.x = symbols("x", integer=True, nonnegative=True)
        self._mode = "Discrete"
        self.t = symbols("t")
        self._support = {0, 1}

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Bernoulli distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x,FiniteSet(0,1)))} \\[6pt]
        \text{{Parameters support:}} \quad {latex(Contains(self.p, Interval(0,1)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PMF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PMF(self):
        return pow(self.p, self.x) * pow(1 - self.p, 1 - self.x)

    def FGM(self):
        return self.p * exp(self.t) + 1 - self.p

    def CDF(self):
        return (summation(self.PMF(), (self.x, 0, floor(self.x)))).simplify()

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PMF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PMF"):
        if parameters["p"] < 0 or parameters["p"] > 1:
            raise ValueError("p must be between 0 and 1")

        parameters = {self.p: parameters["p"]}

        functions_ = {
            "PMF": self.PMF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in functions_:
            return functions_[function.upper()]().subs(parameters)
        else:
            raise ValueError(
                "Invalid function type. Choose from 'PMF', 'CDF', 'SF', or 'HF'."
            )

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")

        return diff(self.FGM(), self.t, n).subs(self.t, 0).simplify()


class Binomial:
    def __init__(self):
        self.p = symbols("theta")
        self.x = symbols("x")
        self.n = symbols("n")
        self.t = symbols("t")
        self._mode = "Discrete"
        self._support = None

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Binomial distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x,Range(0,self.n)))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(self.p, Interval(0,1)))} \\[6pt]
        \quad {latex(Contains(self.n,Naturals))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PMF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PMF(self):
        return (
            (binomial(self.n, self.x))
            * pow(self.p, self.x)
            * pow(1 - self.p, self.n - self.x)
        )

    def FGM(self):
        return pow(((self.p * exp(self.t)) + 1 - self.p), self.n)

    def CDF(self):
        return (summation(self.PMF(), (self.x, 0, floor(self.x)))).simplify()

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PMF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PMF"):
        if "p" in parameters:
            if parameters["p"] < 0 or parameters["p"] > 1:
                raise ValueError("p must be between 0 and 1")
            parameters["theta"] = parameters.pop("p")
        if "n" in parameters:
            if parameters["n"] <= 0:
                raise ValueError("n must be greater than 0")

        functions_ = {
            "PMF": self.PMF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in functions_:
            return functions_[function.upper()]().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        return diff(self.FGM(), self.t, n).subs(self.t, 0).simplify()


class Geometric:
    def __init__(self):

        self.p = symbols("theta", real=True, positive=True)
        self.x = symbols("x", integer=True, nonnegative=True)
        self.t = symbols("t")
        self._mode = "Discrete"

    def __call__(self, *args, **kwds):
        Nplus = symbols(r"\mathbb{N}^{+}", real=True)
        expr = rf"""
        \textbf{{\Large Geometric distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PMF())} \\[6pt]
        \text{{Support:}} \quad {latex(self.x)} \in \mathbb{{N}}^+ \\[6pt]
        \text{{Parameters support:}} \quad {latex(Contains(self.p, Interval(0,1)))} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PMF(self):
        return pow(1 - self.p, self.x - 1) * self.p

    def FGM(self):
        return (self.p * exp(self.t)) / (1 - (1 - self.p) * exp(self.t))

    def CDF(self):
        return (summation(self.PMF(), (self.x, 1, floor(self.x)))).simplify()

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PMF() / self.SF()).simplify()

    def replace(
        self,
        parameters,
        function: str = "PMF",
    ):
        if parameters["p"] < 0 or parameters["p"] > 1:
            raise ValueError("p must be between 0 and 1")
        funcionts_ = {
            "PMF": self.PMF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in funcionts_:
            return funcionts_[function.upper()]().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        return diff(self.FGM(), self.t, n).subs(self.t, 0).simplify()


class HyperGeometric:
    def __init__(self):
        self.n = symbols("n")
        self.K = symbols("K")
        self.N = symbols("N")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Discrete"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large HyperGeometric distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, Range(Max(0, self.n - (self.N - self.K)), Min(self.n, self.K))))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(self.n, Naturals))} \\[6pt]
        \quad {latex(Contains(self.K, Range(0, self.N)))} \\[6pt]
        \quad {latex(Contains(self.n, Range(0, self.N)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PMF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PMF(self):
        return (
            binomial(self.K, self.x) * binomial(self.N - self.K, self.n - self.x)
        ) / (binomial(self.N, self.n))

    def FGM(self):
        warnings.warn("It does not have a simple closed-form expression.")
        return summation(
            exp(self.t * self.x) * self.PMF(),
            (self.x, Max(0, self.n - (self.N - self.K)), Min(self.n, self.K)),
        )

    def CDF(self):
        return (summation(self.PMF(), (self.x, 0, floor(self.x)))).simplify()

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PMF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PMF"):
        have_N = False
        if "N" in parameters:
            have_N = True
            if not isinstance(parameters["N"], int) or parameters["N"] < 1:
                raise ValueError("N must be and integer greater than or equal to 1")

        if "K" in parameters:
            if not have_N:
                raise ValueError("K must be defined only after N is defined")
            if not isinstance(parameters["K"], int) or parameters["K"] < 0:
                raise ValueError("K must be an integer greater than or equal to 0")
            if parameters["K"] > parameters["N"]:
                raise ValueError("K must be less than or equal to N")

        if "n" in parameters:
            if not have_N:
                raise ValueError("n must be defined only after N is defined")
            if not isinstance(parameters["n"], int) or parameters["n"] < 0:
                raise ValueError("K must be an integer greater than or equal to 0")
            if parameters["n"] > parameters["N"]:
                raise ValueError("n must be less than or equal to N")

        functions_ = {
            "PMF": self.PMF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in functions_:
            return functions_[function.upper()]().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        return diff(self.FGM(), self.t, n).subs(self.t, 0).simplify()


class Poisson:
    def __init__(self):
        self.l = symbols("lambda")
        self.x = symbols("x")
        self._mode = "Discrete"
        self.t = symbols("t")

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Poisson distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.l, Interval(0, oo)))} \\[6pt]
        \text{{Parameters support:}} \quad {latex(Contains(self.l, Interval(0, oo)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PMF())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PMF(self):
        return pow(self.l, self.x) * exp(-self.l) / factorial(self.x)

    def FGM(self):
        return exp(self.l * (exp(self.t) - 1))

    def CDF(self):
        return (summation(self.PMF(), (self.x, 0, floor(self.x)))).simplify()

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PMF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PMF"):
        if parameters["l"] < 0:
            raise ValueError("l must be greater than 0")

        parameters["lambda"] = parameters.pop("l")

        functions_ = {
            "PMF": self.PMF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in functions_:
            return functions_[function.upper()]().subs(parameters)
        else:
            raise ValueError("Invalid function type")

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
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, Interval(self.a, self.b)))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(self.a, sympy.Reals))} \\[6pt]
        \quad {latex(Contains(self.b, sympy.Reals))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PDF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PDF(self):
        return 1 / (self.b - self.a)

    def FGM(self):
        return (exp(self.t * self.b) - exp(self.t * self.a)) / (
            self.t * (self.b - self.a)
        )

    def CDF(self):
        return integrate(self.PDF(), (self.t, self.a, self.x)).simplify()

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PDF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PDF"):
        if "a" in parameters:
            if "b" not in parameters:
                raise ValueError("b must be defined only after a is defined")
            if parameters["a"] >= parameters["b"]:
                raise ValueError("a must be less than b")
        functions_ = {
            "PDF": self.PDF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }

        if function.upper() in functions_:
            return functions_[function.upper()]().subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.PDF(), (self.x, self.a, self.b))
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Exponential:
    def __init__(self):

        self.l = symbols("lambda", real=True, positive=True)
        self.l_dummy = symbols("l")
        self.x = symbols("x")
        self.t = symbols("t", positive=True)

        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Exponential distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, Interval(0, oo)))} \\[6pt]
        \text{{Parameters support:}} \quad {latex(Contains(symbols("lambda"), Interval(0, oo)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PDF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PDF(self):
        return self.l * exp(-self.l * self.x)

    def FGM(self):
        return self.l / (self.l - self.t)

    def CDF(self):
        return integrate(self.PDF(), (self.x, 0, self.x)).rewrite(sympy.Piecewise)

    def SF(self):
        return exp(-self.l * self.x)

    def HF(self):
        return self.PDF() / self.SF()

    def replace(
        self,
        parameters,
        function: str = "PDF",
    ):
        if parameters["l"] < 0:
            raise ValueError("l must be greater than 0")

        function_ = {
            "PDF": self.PDF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }

        if function.upper() in function_:
            return (
                function_[function.upper()]()
                .subs({self.l: self.l_dummy})
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.PDF(), (self.x, 0, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Normal:
    def __init__(self):
        self.x = symbols("x")
        self.v = symbols("sigma^2", real=True, positive=True)
        self.v_dummy = symbols("v")
        self.m = symbols("mu", real=True)
        self.m_dummy = symbols("m")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Normal distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, sympy.Reals))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(symbols("mu"), sympy.Reals))} \\[6pt]
        \quad {latex(Contains(symbols("sigma^2"), Interval(0, oo)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PDF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PDF(self):
        return (1 / sqrt(2 * pi * self.v)) * exp(
            (-((self.x - self.m) ** 2)) / (2 * (self.v))
        )

    def FGM(self):
        return exp(self.m * self.t + 0.5 * (self.v) * (self.t**2))

    def CDF(self):
        return integrate(self.PDF(), (self.x, -oo, self.x)).rewrite(sympy.Piecewise)

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PDF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PDF"):
        if "v" in parameters:
            if parameters["v"] < 0:
                raise ValueError("v must be greater than 0")

        functions_ = {
            "PDF": self.PDF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }

        if function.upper() in functions_:
            return (
                functions_[function.upper()]()
                .subs({self.v: self.v_dummy, self.m: self.m_dummy})
                .subs(parameters)
            )
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.PDF(), (self.x, -oo, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Weibull:
    def __init__(self):
        self.b, self.a = symbols("beta alpha", real=True, positive=True)
        self.b_dummy = symbols("b")
        self.a_dummy = symbols("a")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):

        expr = rf"""
        \textbf{{\Large Weibull distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, Interval(0, oo)))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(symbols("alpha"), Interval(0, oo)))} \\[6pt]
        \quad {latex(Contains(symbols("beta"), Interval(0, oo)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PDF())} \\[6pt]
        \text{{\tiny To view the PDF, CDF, SF, HF, or the moments, please use the corresponding function separately.}} \\[3pt]
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

    def PDF(self):
        return (
            self.b
            * self.a
            * ((self.b * self.x) ** (self.a - 1))
            * exp(-((self.b * self.x) ** self.a))
        )

    def FGM(self):
        integral_expr = integrate(exp(self.t * self.x) * self.PDF(), (self.x, 0, oo))
        return integral_expr.simplify()

    def CDF(self):
        return integrate(self.PDF(), (self.x, 0, self.x)).rewrite(sympy.Piecewise)

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PDF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PDF"):
        params = {}
        if "b" in parameters:
            if parameters["b"] < 0:
                raise ValueError("b must be greater than or equal to 0")
            params[self.b] = self.b_dummy
        if "a" in parameters:
            if parameters["a"] < 0:
                raise ValueError("a must be greater than or equal to 0")
            params[self.a] = self.a_dummy

        function_ = {
            "PDF": self.PDF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in function_:
            return function_[function.upper()]().subs(params).subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.PDF(), (self.x, 0, oo)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = limit(diff(self.FGM(), self.t, n).simplify(), self.t, 0)
        return E.simplify()


class Gamma:
    def __init__(self):
        self.a, self.b = symbols("alpha beta", real=True, positive=True)
        self.a_dummy = symbols("a")
        self.b_dummy = symbols("b")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Gamma distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, Interval(0, oo)))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(symbols("alpha"), Interval(0, oo)))} \\[6pt]
        \quad {latex(Contains(symbols("beta"), Interval(0, oo)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PDF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).simplify())}
        """
        display(Math(expr))

    def PDF(self):
        return (
            (self.b**self.a / gamma(self.a))
            * self.x ** (self.a - 1)
            * exp(-self.b * self.x)
        )

    def FGM(self):
        return (self.b / (self.b - self.t)) ** self.a

    def CDF(self):
        return integrate(self.PDF(), (self.x, 0, self.x)).rewrite(sympy.Piecewise)

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PDF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PDF"):
        params = {}
        if "a" in parameters:
            if parameters["a"] < 0:
                raise ValueError("a must be greater than 0")
            params[self.a] = self.a_dummy
        if "b" in parameters:
            if parameters["b"] < 0:
                raise ValueError("b must be greater than 0")
            params[self.b] = self.b_dummy

        function_ = {
            "PDF": self.PDF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in function_:
            return function_[function.upper()]().subs(params).subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int, mode: str = "integrate"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.PDF(), (self.x, 0, oo)).rewrite(
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
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, Interval(0, 1)))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(symbols("alpha"), Interval(0, oo)))} \\[6pt]
        \quad {latex(Contains(symbols("beta"), Interval(0, oo)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PDF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
        \text{{Expected value:}} \quad {latex(self.calculate_moments(1))} \\[6pt]
        \text{{Variance:}} \quad {latex((self.calculate_moments(2) - self.calculate_moments(1)**2).factor())}
        """
        display(Math(expr))

    def PDF(self):
        return (
            (1 / beta_func(self.a, self.b))
            * (self.x ** (self.a - 1))
            * ((1 - self.x) ** (self.b - 1))
        )

    def FGM(self):
        warnings.warn(
            "It does not have a simple closed-form expression. Then using the explicit form"
        )

        return (gamma(self.a + self.r) * gamma(self.a + self.b)) / (
            gamma(self.a) * gamma(self.a + self.b + self.r)
        )

    def CDF(self):
        return integrate(self.PDF(), (self.x, 0, self.x)).rewrite(sympy.Piecewise)

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PDF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PDF"):
        params = {}
        if "a" in parameters:
            if parameters["a"] < 0:
                raise ValueError("a must be greater than 0")
        if "b" in parameters:
            if parameters["b"] < 0:
                raise ValueError("b must be greater than 0")
        functions_ = {
            "PDF": self.PDF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in functions_:
            return (
                functions_[function.upper()]()
                .subs({self.a: self.a_dummy, self.b: self.b_dummy})
                .subs(parameters)
            )

        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int, mode: str = "diff"):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        if mode == "integrate":
            E = integrate(pow(self.x, n) * self.PDF(), (self.x, 0, 1)).rewrite(
                sympy.Piecewise
            )
        elif mode == "diff":
            E = self.FGM().subs(self.r, n).simplify()
        return E.simplify()


class LogNormal:
    def __init__(self):
        self.m, self.v = symbols("mu sigma^2", real=True)
        self.m_dummy = symbols("m")
        self.v_dummy = symbols("v")
        self.x = symbols("x")
        self.t = symbols("t")
        self.r = symbols("r")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Log-Normal distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, Interval(0, oo)))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(symbols("mu"), sympy.Reals))} \\[6pt]
        \quad {latex(Contains(symbols("sigma^2"), Interval(0, oo)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PDF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PDF(self):
        return (1 / (self.x * sqrt(2 * pi * self.v))) * exp(
            -((log(self.x) - self.m) ** 2) / (2 * self.v)
        )

    def FGM(self):
        warnings.warn(
            "It does not have a simple closed-form expression. Then using the explicit form"
        )
        return exp(self.r * self.m + ((self.r**2 * self.v) / (2)))

    def CDF(self):
        return integrate(self.PDF(), (self.x, 0, self.x)).rewrite(sympy.Piecewise)

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PDF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PDF"):
        params = {}
        if "v" in parameters:
            if parameters["v"] < 0:
                raise ValueError("v must be greater than 0")
            params[self.v] = self.v_dummy
        if "m" in parameters:
            params[self.m] = self.m_dummy
        functions_ = {
            "PDF": self.PDF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in functions_:
            return functions_[function.upper()]().subs(params).subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        return self.FGM().subs(self.r, n).simplify()


class Gumbel:
    def __init__(self):
        self.m, self.b = symbols("mu", real=True), symbols(
            "beta", real=True, positive=True
        )
        self.m_dummy = symbols("m")
        self.b_dummy = symbols("b")
        self.x = symbols("x")
        self.t = symbols("t")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Gumbel distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, sympy.Reals))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(self.m, sympy.Reals))} \\[6pt]
        \quad {latex(Contains(self.b, Interval(0, oo)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PDF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PDF(self):
        return (
            (1 / self.b)
            * exp((self.x - self.m) / self.b)
            * exp(-exp((self.x - self.m) / self.b))
        )

    def FGM(self):
        return gamma(1 - self.b * self.t) * exp(self.m * self.t)

    def CDF(self):
        return integrate(self.PDF(), (self.x, -oo, self.x)).rewrite(sympy.Piecewise)

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PDF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PDF"):
        params = {}
        if "b" in parameters:
            if parameters["b"] < 0:
                raise ValueError("b must be greater than 0")
            params[self.b] = self.b_dummy
        if "m" in parameters:
            params[self.m] = self.m_dummy

        function_ = {
            "PDF": self.PDF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in function_:
            return function_[function.upper()]().subs(params).subs(parameters)
        else:
            raise ValueError("Invalid function type")

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
        self.a, self.b = symbols("alpha beta", real=True, positive=True)
        self.a_dummy = symbols("a")
        self.b_dummy = symbols("b")
        self.x = symbols("x")
        self.t = symbols("t")
        self.r = symbols("r")
        self._mode = "Continuous"

    def __call__(self, *args, **kwds):
        expr = rf"""
        \textbf{{\Large Birnbaum-Saunders distribution}} \\[6pt]
        \text{{Distribution mode:}} \quad {self._mode} \\[6pt]
        \text{{Support:}} \quad {latex(Contains(self.x, Interval(0, oo)))} \\[6pt]
        \text{{Parameters support:}} \\[6pt]
        \quad {latex(Contains(symbols("alpha"), Interval(0, oo)))} \\[6pt]
        \quad {latex(Contains(symbols("beta"), Interval(0, oo)))} \\[6pt]
        \text{{Function probability:}} \quad {latex(self.PDF())} \\[6pt]
        \text{{Generating function moment:}} \quad {latex(self.FGM())} \\[6pt]
        \text{{Cumulative distribution function:}} \quad {latex(self.CDF())} \\[6pt]
        \text{{Survival function:}} \quad {latex(self.SF())} \\[6pt]
        \text{{Hazard function:}} \quad {latex(self.HF())} \\[6pt]
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

    def PDF(self):
        return (
            (1 / sqrt(2 * pi))
            * exp(
                (-1 / 2)
                * (1 / self.a * (sqrt(self.x / self.b) - sqrt(self.b / self.x)) ** 2)
            )
            * ((pow(self.x, -3 / 2) * (self.x + self.b)) / (2 * self.a * sqrt(self.b)))
        )

    def FGM(self):
        warnings.warn(
            "It does not have a simple closed-form expression. Then using the explicit form"
        )
        Z = Norm("Z", mean=0, std=1)
        return self.b * (self.a * Z / 2 + sqrt(1 + (self.a * Z / 2) ** 2)) ** (
            2 * self.r
        )

    def CDF(self):
        return integrate(self.PDF(), (self.x, 0, self.x)).rewrite(sympy.Piecewise)

    def SF(self):
        return (1 - self.CDF()).simplify()

    def HF(self):
        return (self.PDF() / self.SF()).simplify()

    def replace(self, parameters, function: str = "PDF"):
        params = {}
        if "a" in parameters:
            if parameters["a"] < 0:
                raise ValueError("a must be greater than 0")
            params[self.a] = self.a_dummy
        if "b" in parameters:
            if parameters["b"] < 0:
                raise ValueError("b must be greater than 0")
            params[self.b] = self.b_dummy

        functions_ = {
            "PDF": self.PDF,
            "CDF": self.CDF,
            "SF": self.SF,
            "HF": self.HF,
            "FGM": self.FGM,
        }
        if function.upper() in functions_:
            return functions_[function.upper()]().subs(params).subs(parameters)
        else:
            raise ValueError("Invalid function type")

    def calculate_moments(self, n: int):
        if n < 1:
            raise ValueError("n must be greater than or equal to 1")
        return E(self.FGM()).subs(self.r, n).simplify()


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
