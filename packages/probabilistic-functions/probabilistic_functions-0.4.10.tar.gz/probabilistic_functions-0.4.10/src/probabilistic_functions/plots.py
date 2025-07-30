from typing import Union, Callable
from sympy import symbols, sympify, lambdify, factorial, simplify
from sympy import exp, sqrt, pi, latex, integrate, S, summation, diff, limit
from sympy import oo
from sympy import pprint
import sympy
import matplotlib.pyplot as plt
import math
import numpy as np
from itertools import product


def plot_function(function: Union[str, Callable], *args, **kwargs):
    graph = kwargs.get("graph", False)
    FDA = kwargs.get("FDA", False)
    size = kwargs.get("size", (5, 5))
    x = symbols("x")
    assert isinstance(function, str) or callable(
        function
    ), "function must be a string or callable"
    distributions = {
        "bernulli": Bernulli(),
        "binomial": Binomial(),
        "geometry": Geometric(),
        "hyperGeometry": HyperGeometric(),
        "poisson": Poisson(),
        "uniform": Uniform(),
        "exponential": Exponential(),
        "norm": Norm(),
        "weibull": Weibull(),
    }
    distribution = (
        function()
        if not isinstance(function, str)
        else distributions[function.lower().strip()]
    )
    if graph:
        parameters = kwargs.get("parameters", None)
        if parameters is None:
            raise ValueError("parameters must be a dictionary")
        if not isinstance(parameters, dict):
            raise ValueError("parameters must be a dictionary")
        param_values = {
            k: v if isinstance(v, list) else [v] for k, v in parameters.items()
        }
        combinations = list(product(*param_values.values()))
        result = [dict(zip(param_values.keys(), combo)) for combo in combinations]
        if distribution.get_name == "Bernulli":
            if isinstance(parameters["p"], list):
                distribution._support = [np.arange(0, 2) for elem in result]
        if distribution.get_name == "Binomial":
            distribution._support = [np.arange(0, elem["n"] + 1) for elem in result]
            if len(distribution._support) == 1:
                distribution._support = distribution._support[0]
        if distribution.get_name == "Geometric":
            print("ENTRO")
            support_max = []
            for param in result:
                support = []
                i = 1
                while True:
                    prob = distribution.replace(param).subs(x, i).evalf()
                    if prob < 0.001:
                        break
                    support.append(i)
                    i += 1
                support_max.append(support)
            if len(support_max) == 1:
                distribution._support = support_max[0]
            else:
                max_index = max(
                    range(len(support_max)), key=lambda i: len(support_max[i])
                )
                longest_list = support_max[max_index]
                distribution._support = [longest_list[:] for _ in support_max]
        if distribution.get_name == "HyperGeometric":
            distribution._support = [np.arange(0, elem["N"] + 1) for elem in result]
            if len(distribution._support) == 1:
                distribution._support = distribution._support[0]
        if distribution.get_name == "Poisson":
            support_max = []
            for param in result:
                support = []
                i = 0
                while True:
                    prob = distributions[function].replace(param).subs(x, i).evalf()
                    if prob < 0.001:
                        break
                    support.append(i)
                    i += 1
                support_max.append(support)
            if len(support_max) == 1:
                distribution._support = support_max[0]
            else:
                max_index = max(
                    range(len(support_max)), key=lambda i: len(support_max[i])
                )
                longest_list = support_max[max_index]
                distribution._support = [longest_list[:] for _ in support_max]

        if distribution.get_name == "Uniform":
            distribution._support = [
                np.arange(elemt["a"], elemt["b"] + 1) for elemt in result
            ]
            if len(distribution._support) == 1:
                distribution._support = distribution._support[0]

        if distribution.get_name == "Exponential":
            support_max = []
            for param in result:

                i = 0
                max_num = 0
                while True:
                    prob = distribution.replace(param).subs(x, i).evalf()
                    if prob < 0.001:
                        max_num = i
                        break
                    i += 1
                support_max.append(np.linspace(0, max_num, 60))
            if len(support_max) == 1:
                distribution._support = support_max[0]
            else:
                max_index = max(
                    range(len(support_max)), key=lambda i: len(support_max[i])
                )
                longest_list = support_max[max_index]
                distribution._support = [longest_list[:] for _ in support_max]

        if distribution.get_name == "Norm":
            distribution._support = [
                np.linspace(
                    elemt["m"] - math.sqrt(elemt["v"]) * 3,
                    elemt["m"] + math.sqrt(elemt["v"]) * 3,
                    70,
                )
                for elemt in result
            ]
            if len(distribution._support) == 1:
                distribution._support = distribution._support[0]

        if distribution.get_name == "Weibull":
            support_max = []
            for param in result:

                i = 1
                max_num = 0
                while True:
                    prob = distribution.replace(param).subs(x, i).evalf()
                    if prob < 0.001:
                        max_num = i
                        break
                    i *= 2
                support_max.append(np.linspace(0.01, max_num, 80))
            if len(support_max) == 1:
                distribution._support = support_max[0]
            else:
                max_index = max(
                    range(len(support_max)), key=lambda i: len(support_max[i])
                )
                longest_list = support_max[max_index]
                distribution._support = [longest_list[:] for _ in support_max]

        plt.figure(figsize=size)
        colors = plt.cm.tab10.colors  # Lista de colores predefinidos en Matplotlib
        num_colors = len(colors)
        if len(result) > 1:
            for i, (params, color, support) in enumerate(
                zip(result, colors[: len(result)], distribution._support)
            ):
                dis = distribution.replace(params)
                probs = [dis.subs(x, i).evalf() for i in support]
                if distribution.get_mode == "Discrete":
                    if FDA:
                        fda = np.cumsum(probs)
                        for i in range(len(list(support)) - 1):
                            plt.hlines(
                                y=fda[i],
                                xmin=list(support)[i],
                                xmax=list(support)[i + 1],
                                color=color,
                                linestyle="-",
                            )
                        markerline, _, _ = plt.stem(
                            list(support),
                            fda,
                            linefmt="none",
                            markerfmt="o",
                            basefmt=" ",
                            label=str(params),
                        )
                        markerline.set_color(color)
                else:
                    markerline, _, _ = plt.stem(
                        list(support),
                        probs,
                        linefmt="none",
                        markerfmt="o",
                        basefmt=" ",
                        label=r"$" + latex(dis) + ", " + str(params) + r"$",
                    )
                    markerline.set_color(color)  # Aplicar color solo a los puntos
                if distribution.get_mode == "Continuous":
                    if FDA:
                        t = symbols("t")
                        density = dis.subs(x, t)
                        lower_bound = support[0]
                        cdf_expr = integrate(density, (t, lower_bound, x))
                        cdf_probs = [cdf_expr.subs(x, i).evalf() for i in support]
                        plt.plot(
                            support,
                            cdf_probs,
                            color=color,
                            label=r"$" + latex(cdf_expr) + ", " + str(params) + r"$",
                        )
                else:
                    plt.plot(
                        support,
                        probs,
                        color=color,
                        label=r"$" + latex(dis) + ", " + str(params) + r"$",
                    )
        else:
            dis = distribution.replace(result[0])
            probs = [dis.subs(x, i).evalf() for i in distribution._support]
            if distribution.get_mode == "Discrete":
                if FDA:
                    fda = np.cumsum(probs)
                    for i in range(len(list(distribution._support)) - 1):
                        plt.hlines(
                            y=fda[i],
                            xmin=list(distribution._support)[i],
                            xmax=list(distribution._support)[i + 1],
                            color="r",
                            linestyle="-",
                        )
                    plt.stem(
                        list(distribution._support),
                        fda,
                        linefmt="none",
                        markerfmt="ro",
                        basefmt=" ",
                        label=r"$" + latex(dis) + ", " + str(parameters) + r"$",
                    )
                else:
                    plt.stem(
                        list(distribution._support),
                        probs,
                        linefmt="r-",
                        markerfmt="ro",
                        basefmt=" ",
                        label=r"$" + latex(dis) + ", " + str(parameters) + r"$",
                    )
        if distribution.get_mode == "Continuous":
            if FDA:
                t = symbols("t")
                density = dis.subs(x, t)
                lower_bound = distribution._support[0]
                if function == "Weibull":
                    lower_bound = S(0)
                cdf_expr = integrate(density, (t, lower_bound, x))
                cdf_probs = [cdf_expr.subs(x, i).evalf() for i in distribution._support]
                plt.plot(
                    list(distribution._support),
                    cdf_probs,
                    label=r"$" + latex(cdf_expr) + ", " + str(parameters) + r"$",
                )
            else:
                plt.plot(
                    list(distribution._support),
                    probs,
                    label=r"$" + latex(dis) + ", " + str(parameters) + r"$",
                )
        plt.legend()
        plt.show()
    else:
        distribution = (
            function()
            if not isinstance(function, str)
            else distributions[function.lower().strip()]
        )
        dis = distribution.replace(parameters)
        return dis


if __name__ == "__main__":
    from probabilistic_functions.core import (
        Bernulli,
        Binomial,
        Geometric,
        HyperGeometric,
        Poisson,
        Uniform,
        Exponential,
        Norm,
        Weibull,
    )
else:
    from .core import (
        Bernulli,
        Binomial,
        Geometric,
        HyperGeometric,
        Poisson,
        Uniform,
        Exponential,
        Norm,
        Weibull,
    )
