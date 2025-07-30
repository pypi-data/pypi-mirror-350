import numpy as np
import matplotlib.pyplot as plt

X_BORDER = 0.5
Y_BORDER = 0.5
Y_MAX_BUCKET = 0.0
Y_LEVEL = 1.0
TICK_HEIGHT = 0.2
AXIS_TEXT_OFFSET = 0.1
AXIS_TEXT_SIZE = 8
TEXT_COLOR = "black"
TEXT_HEIGHT = 1.0

BUCKET_COLOR = "black"
BUCKET_SIZE = 20
BUCKET_MARKER = "o"
AXIS_COLOR = "black"
AXIS_LINEWIDTH = 3.0
LINK_COLOR = "black"
LINK_LINEWIDTH = 0.5
TICK_LINEWIDTH = 1.0


def view(tree):
    fig = plt.figure()
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))

    y_min = 0
    x_min = 1e10
    x_max = -1e10

    for bucket in tree.buckets[: tree.n_buckets]:
        y = Y_MAX_BUCKET - bucket.level * Y_LEVEL
        if bucket.is_leaf:
            x = np.median(bucket.observations[: bucket.n_observations])
        else:
            x = bucket.split_value

            lo_child = bucket.lo_child
            y_lo = Y_MAX_BUCKET - lo_child.level * Y_LEVEL

            if lo_child.is_leaf:
                x_lo = np.median(lo_child.observations[: lo_child.n_observations])
            else:
                x_lo = lo_child.split_value

            hi_child = bucket.hi_child
            y_hi = Y_MAX_BUCKET - hi_child.level * Y_LEVEL
            if hi_child.is_leaf:
                x_hi = np.median(hi_child.observations[: hi_child.n_observations])
            else:
                x_hi = hi_child.split_value

            ax.plot([x, x_lo], [y, y_lo], color=LINK_COLOR, linewidth=LINK_LINEWIDTH)
            ax.plot([x, x_hi], [y, y_hi], color=LINK_COLOR, linewidth=LINK_LINEWIDTH)

        y_min = np.minimum(y_min, y)
        x_min = np.minimum(x_min, x)
        x_max = np.maximum(x_max, x)

        ax.scatter(x, y, c=BUCKET_COLOR, s=BUCKET_SIZE, marker=BUCKET_MARKER)

    y_axis = y_min - Y_LEVEL
    ax.plot(
        [x_min, x_max],
        [y_axis, y_axis],
        color=AXIS_COLOR,
        linewidth=AXIS_LINEWIDTH,
        solid_capstyle="round",
    )

    x_ticks = np.linspace(x_min, x_max, 10)
    for x_tick in x_ticks:
        ax.plot(
            [x_tick, x_tick],
            [y_axis, y_axis + TICK_HEIGHT],
            color=AXIS_COLOR,
            linewidth=TICK_LINEWIDTH,
        )
        ax.text(
            x_tick,
            y_axis - AXIS_TEXT_OFFSET,
            f"{x_tick:.03}",
            color=TEXT_COLOR,
            fontsize=AXIS_TEXT_SIZE,
            horizontalalignment="center",
            verticalalignment="top",
            rotation=-90,
        )

    # ax.set_xlim(x_min - X_BORDER, x_max + X_BORDER)
    ax.set_ylim(y_axis - TEXT_HEIGHT - Y_BORDER, Y_BORDER)

    plt.show()
