"naca_polarfits.py"

from builtins import range, zip

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update({"font.size": 15})


def text_to_df(filename):
    "parse XFOIL polars and concatente data in DataFrame"
    lines = list(open(filename))
    for i, l in enumerate(lines):
        lines[i] = l.split("\n")[0]
        for j in 10 - np.arange(9):
            if " " * j in lines[i]:
                lines[i] = lines[i].replace(" " * j, " ")
            if "---" in lines[i]:
                start = i
    data = {}
    titles = lines[start - 1].split(" ")[1:]
    for t in titles:
        data[t] = []

    for l in lines[start + 1 :]:
        for i, v in enumerate(l.split(" ")[1:]):
            data[titles[i]].append(v)

    df = pd.DataFrame(data)
    df = df.astype(float)
    return df


def fit_setup(naca_range, re_range):
    "set up x and y parameters for gp fitting"
    tau = [[float(n)] * len(re_range) for n in naca_range]
    re = [re_range] * len(naca_range)
    cd = []
    for n in naca_range:
        for r in re_range:
            dataf = text_to_df("naca%s.cl0.Re%dk.pol" % (n, r))
            cd.append(dataf["CD"])

    u1 = np.hstack(re)
    u2 = np.hstack(tau)
    w = np.hstack(cd)
    u1 = u1.astype(np.float)
    u2 = u2.astype(np.float)
    w = w.astype(np.float)
    u = [u1, u2]
    x = np.log(u)
    y = np.log(w)
    return x, y


def return_fit(u_1, u_2):
    "naca tau and reynolds fit"
    w = (
        7.42688e-90 * (u_1) ** -33.0637 * (u_2) ** 18.0419
        + 5.02826e-163 * (u_1) ** -18.7959 * (u_2) ** 53.1879
        + 4.22901e-77 * (u_1) ** -41.1704 * (u_2) ** 28.4609
    ) ** (1 / 70.5599)
    # SMA function, K=3, max RMS error = 0.0173
    return w


def plot_fits(naca_range, re_range):
    "plot fit compared to data"

    fig, ax = plt.subplots()
    colors = ["k", "m", "b", "g", "y", "r"]
    assert len(colors) == len(naca_range)
    res = np.linspace(re_range[0], re_range[-1], 50)
    for n, col in zip(naca_range, colors):
        cd = []
        for r in re_range:
            dataf = text_to_df("naca%s.cl0.Re%dk.pol" % (n, r))
            cd.append(dataf["CD"])
        if True in [c.empty for c in cd]:
            i = [c.empty for c in cd].index(True)
            cd[i] = (cd[i - 1] + cd[i + 1]) / 2
        ax.plot(re_range, cd, "o", mec=col, mfc="None", mew=1.5)
        w = return_fit(res, float(n))
        ax.plot(res, w, c=col, label="NACA %s" % n, lw=2)
    ax.legend(fontsize=15)
    labels = ["k" + item.get_text() for item in ax.get_xticklabels()]
    labels = ["%dk" % l for l in np.linspace(200, 900, len(labels))]
    ax.set_xticklabels(labels)
    ax.set_xlabel("$Re$")
    ax.set_ylabel("$c_{dp}$")
    ax.grid()
    return fig, ax


if __name__ == "__main__":
    Re = list(range(200, 950, 50))
    NACA = ["0005", "0008", "0009", "0010", "0015", "0020"]
    X, Y = fit_setup(NACA, Re)  # call fit(X, Y, 4, "SMA") to get fit
    F, A = plot_fits(NACA, Re)
    F.savefig("taildragpolar.pdf", bbox_inches="tight")
