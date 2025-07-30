import matplotlib.pyplot as plt


def unit_circle(figsize=(1.5, 1.5)):
    fig, ax = plt.subplots(figsize=figsize)
    circle1 = plt.Circle((0, 0), 1, edgecolor='black', facecolor="white")
    ax.add_patch(circle1)
    plt.arrow(0, 0, 1.2, 0, color="black", head_width=0.04, head_length=0.05)
    plt.arrow(0, 0, 0, 1.2, color="black", head_width=0.04, head_length=0.05)
    plt.annotate("|0⟩", (1.2, 0.07))
    plt.annotate("|1⟩", (0.07, 1.2))
    plt.arrow(0, 0, -1.2, 0, color="black", head_width=0.04, head_length=0.05)
    plt.arrow(0, 0, 0, -1.2, color="black", head_width=0.04, head_length=0.05)
    return fig, ax

