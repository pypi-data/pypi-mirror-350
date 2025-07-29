import matplotlib.pyplot as plt

from pyroll.core import Unit, RollPass
from pyroll.report import hookimpl

@hookimpl
def unit_plot(unit: Unit):
    """Plot wear contour for one groove of roll pass contour."""
    if isinstance(unit, RollPass):
        fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(6, 4))
        ax: plt.Axes
        axl: plt.Axes
        ax, axl = fig.subplots(nrows=2, height_ratios=[1, 0.3])
        ax.set_title("Groove Wear Analysis")

        ax.set_aspect("equal", "datalim")
        ax.grid(lw=0.5)

        for i, contour_line in enumerate(unit.contour_lines.geoms):
            roll_surface = ax.plot(*unit.contour_lines.geoms[i].xy, color="k", label="roll surface")
            wear_contour = ax.plot(*unit.wear_contour_lines.geoms[i].xy, color='red', ls='--', label="wear contour")
        ax.fill(*unit.out_profile.cross_section.boundary.xy, color="C0", alpha=0.5, label="OutProfile")

        axl.axis("off")
        axl.legend(handles=roll_surface + wear_contour, ncols=3, loc="lower center")
        fig.set_layout_engine('constrained')

        return fig