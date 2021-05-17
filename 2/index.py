# 10 (v2)
# Критерии F_1 => max, F_3 => min.

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, minimize

bounds = Bounds([0, 0], [np.inf, np.inf])
linear_constraint = LinearConstraint(
    [[-1, 3], [2, 5], [3, 2], [1, -3], [2, 5], [5, 1]],
    [-np.inf, -np.inf, -np.inf, -np.inf, 10, 5],
    [12, 30, 22, 0, np.inf, np.inf],
)
x1 = np.arange(1 / 6, 10 / 7 + (0.01), 0.01)
g1 = [(12 + 3 * i) / 3 for i in x1]

x2 = np.arange(10 / 7, 50 / 11 + (0.01), 0.01)
g2 = [(30 - 2 * i) / 5 for i in x2]

x3 = np.arange(50 / 11, 6 + (0.01), 0.01)
g3 = [(22 - 3 * i) / 2 for i in x3]

x4 = np.arange(30 / 11, 6 + (0.01), 0.01)
g4 = [i / 3 for i in x4]

x5 = np.arange(15 / 23, 30 / 11 + (0.01), 0.01)
g5 = [(10 - 2 * i) / 5 for i in x5]

x6 = np.arange(1 / 6, 15 / 23 + (0.01), 0.01)
g6 = [(5 - 5 * i) / 1 for i in x6]

# Поиск компромиссного решения:
def benchmark(fun_1, fun_2, a, direct, f1_extr, f2_extr):
    def decorator(func):
        def wrapped(x):
            if direct[0] == direct[1] == "min":
                return a * (
                    (fun_1(x) - f1_extr["min"]) / (f1_extr["max"] - f1_extr["min"])
                ) + (1 - a) * (
                    (fun_2(x) - f2_extr["min"]) / (f2_extr["max"] - f2_extr["min"])
                )
            elif direct[0] == direct[1] == "max":
                return -a * (
                    (fun_1(x) - f1_extr["min"]) / (f1_extr["max"] - f1_extr["min"])
                ) - (1 - a) * (
                    (fun_2(x) - f2_extr["min"]) / (f2_extr["max"] - f2_extr["min"])
                )
            elif direct[0] != direct[1]:
                if direct[0] == "min":
                    return a * (
                        (fun_1(x) - f1_extr["min"]) / (f1_extr["max"] - f1_extr["min"])
                    ) - (1 - a) * (
                        (fun_2(x) - f2_extr["min"]) / (f2_extr["max"] - f2_extr["min"])
                    )
                else:
                    return -a * (
                        (fun_1(x) - f1_extr["min"]) / (f1_extr["max"] - f1_extr["min"])
                    ) + (1 - a) * (
                        (fun_2(x) - f2_extr["min"]) / (f2_extr["max"] - f2_extr["min"])
                    )

        return wrapped

    return decorator


# Функции линейного вида:
def F1_linear(x):
    return -20000 * x[0] - 9000000 * x[1]


def F3_linear(x):
    return x[0] - 2 * x[1]


x0_opt = []
F_glob_opt = []
a = np.arange(0.05, 1, 0.05)

f2_extr = {
    "max": -1
    * minimize(
        lambda x: -F1_linear(x),
        [1, 1],
        constraints=linear_constraint,
        bounds=bounds,
        method="trust-constr",
    ).fun,
    "min": minimize(
        F1_linear,
        [0, 0],
        constraints=linear_constraint,
        bounds=bounds,
        method="trust-constr",
    ).fun,
}
f3_extr = {
    "max": -1
    * minimize(
        lambda x: -F3_linear(x), [0, 0], constraints=linear_constraint, bounds=bounds
    ).fun,
    "min": minimize(
        F3_linear, [0, 0], constraints=linear_constraint, bounds=bounds
    ).fun,
}

for i in a:

    @benchmark(
        fun_1=F1_linear,
        fun_2=F3_linear,
        a=i,
        direct=["min", "min"],
        f1_extr=f2_extr,
        f2_extr=f3_extr,
    )
    def F_glob(x):
        pass

    res = minimize(F_glob, [0, 0], constraints=linear_constraint, bounds=bounds)
    x0_opt.append(res.x)
    F_glob_opt.append(res.fun)

f1_komp = [F1_linear(i) for i in x0_opt]
f2_komp = [F3_linear(i) for i in x0_opt]

from plotly import graph_objs as go
from plotly.offline import init_notebook_mode, iplot

trace = go.Scatter(
    x=a,
    y=F_glob_opt,
    name="F glob",
    line=dict(color="#000080", width=4),
    marker=dict(color="#FF00FF", size=10),
)
layout = dict(title="<b>F global of α plot (minimization)</b>")
fig = dict(data=trace, layout=layout)
iplot(fig, show_link=True)


trace = go.Scatter(
    x=a,
    y=f1_komp,
    name="F2",
    line=dict(color="#48D1CC", width=4),
    marker=dict(color="#4682B4", size=10),
)
layout = dict(title="<b>F1 of α plot  (minimization)</b>")
fig = dict(data=trace, layout=layout)
iplot(fig, show_link=True)

trace = go.Scatter(
    x=a,
    y=f2_komp,
    name="F3",
    line=dict(color="#F0E68C", width=4),
    marker=dict(color="#FF4500", size=10),
)
layout = dict(title="<b>F2 of α plot  (minimization)</b>")
fig = dict(data=trace, layout=layout)
iplot(fig, show_link=True)
F1_g1 = [F1_linear([x1[i], g1[i]]) for i in range(0, len(x1))]
F1_g2 = [F1_linear([x2[i], g2[i]]) for i in range(0, len(x2))]
F1_g3 = [F1_linear([x3[i], g3[i]]) for i in range(0, len(x3))]
F1_g4 = [F1_linear([x4[i], g4[i]]) for i in range(0, len(x4))]
F1_g5 = [F1_linear([x5[i], g5[i]]) for i in range(0, len(x5))]
F1_g6 = [F1_linear([x6[i], g6[i]]) for i in range(0, len(x6))]
F2_g1 = [F3_linear([x1[i], g1[i]]) for i in range(0, len(x1))]
F2_g2 = [F3_linear([x2[i], g2[i]]) for i in range(0, len(x2))]
F2_g3 = [F3_linear([x3[i], g3[i]]) for i in range(0, len(x3))]
F2_g4 = [F3_linear([x4[i], g4[i]]) for i in range(0, len(x4))]
F2_g5 = [F3_linear([x5[i], g5[i]]) for i in range(0, len(x5))]
F2_g6 = [F3_linear([x6[i], g6[i]]) for i in range(0, len(x6))]
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=F1_g1, y=F2_g1, name="g1", mode="lines", fillcolor="rgba(237, 17, 17, 0.1)"
    )
)
fig.add_trace(
    go.Scatter(
        x=F1_g2, y=F2_g2, name="g2", mode="lines", fillcolor="rgba(217, 52, 250, 0.1)"
    )
)
fig.add_trace(
    go.Scatter(
        x=F1_g3, y=F2_g3, name="g3", mode="lines", fillcolor="rgba(82, 52, 250, 0.1)"
    )
)
fig.add_trace(
    go.Scatter(
        x=F1_g4,
        y=F2_g4,
        name="g4",
        mode="lines",
        fillcolor="rgb(0, 0, 0)",
        line=dict(width=8),
    )
)
fig.add_trace(
    go.Scatter(x=F1_g5, y=F2_g5, name="g5", mode="lines", fillcolor="rgb(52, 250, 52)")
)
fig.add_trace(
    go.Scatter(x=F1_g6, y=F2_g6, name="g6", mode="lines", fillcolor="rgb(237, 250, 52)")
)

fig.update_xaxes(range=[-60_000_000, 0], title="F1")
fig.update_yaxes(range=[-10, 2.1], title="F2")
fig.update_layout(
    title="<b>Область Парето</b>",
)

# Функции нелинейного вида:
def F1_nonlinear(x):
    return 100 * (x[0] ** 2) + (x[1] - 3) ** 2


def F3_nonlinear(x):
    return (x[0] - 10) ** 2 + (x[1] - 10) ** 2


x0_opt = []
F_glob_opt = []
a = np.arange(0.05, 1, 0.05)

f2_extr = {
    "max": -1
    * minimize(
        lambda x: -1 * F1_nonlinear(x),
        [0, 0],
        constraints=linear_constraint,
        bounds=bounds,
    ).fun,
    "min": minimize(
        F1_nonlinear, [0, 0], constraints=linear_constraint, bounds=bounds
    ).fun,
}
f3_extr = {
    "max": -1
    * minimize(
        lambda x: -F3_nonlinear(x), [0, 0], constraints=linear_constraint, bounds=bounds
    ).fun,
    "min": minimize(
        F3_nonlinear, [0, 0], constraints=linear_constraint, bounds=bounds
    ).fun,
}

for i in a:

    @benchmark(
        fun_1=F1_nonlinear,
        fun_2=F3_nonlinear,
        a=i,
        direct=["min", "min"],
        f1_extr=f2_extr,
        f2_extr=f3_extr,
    )
    def F_glob(x):
        pass

    res = minimize(F_glob, [0, 0], constraints=linear_constraint, bounds=bounds)
    x0_opt.append(res.x)
    F_glob_opt.append(res.fun)

f1_komp = [F1_nonlinear(i) for i in x0_opt]
f2_komp = [F3_nonlinear(i) for i in x0_opt]
from plotly import graph_objs as go
from plotly.offline import init_notebook_mode, iplot

init_notebook_mode(connected=True)

trace = go.Scatter(
    x=a,
    y=F_glob_opt,
    name="F glob",
    line=dict(color="#000080", width=4),
    marker=dict(color="#FF00FF", size=10),
)
layout = dict(title="<b>F global of α plot (minimization)</b>")
fig = dict(data=trace, layout=layout)
iplot(fig, show_link=True)


trace = go.Scatter(
    x=a,
    y=f1_komp,
    name="F2",
    line=dict(color="#48D1CC", width=4),
    marker=dict(color="#4682B4", size=10),
)
layout = dict(title="<b>F1 of α plot  (minimization)</b>")
fig = dict(data=trace, layout=layout)
iplot(fig, show_link=True)

trace = go.Scatter(
    x=a,
    y=f2_komp,
    name="F3",
    line=dict(color="#F0E68C", width=4),
    marker=dict(color="#FF4500", size=10),
)
layout = dict(title="<b>F2 of α plot  (miniimization)</b>")
fig = dict(data=trace, layout=layout)
iplot(fig, show_link=True)
fig = go.Figure()
fig.add_trace(go.Scatter(x=F1_g1, y=F2_g1, name="g1", mode="lines"))
fig.add_trace(go.Scatter(x=F1_g2, y=F2_g2, name="g2", mode="lines"))
fig.add_trace(go.Scatter(x=F1_g3, y=F2_g3, name="g3", mode="lines"))
fig.add_trace(go.Scatter(x=F1_g4, y=F2_g4, name="g4", mode="lines"))
fig.add_trace(go.Scatter(x=F1_g5, y=F2_g5, name="g5", mode="lines"))
fig.add_trace(go.Scatter(x=F1_g6, y=F2_g6, name="g6", mode="lines", line=dict(width=8)))

fig.update_xaxes(range=[-20, 3600], title="F1")
fig.update_yaxes(title="F2")
fig.update_layout(title="<b>Область Парето</b>")
