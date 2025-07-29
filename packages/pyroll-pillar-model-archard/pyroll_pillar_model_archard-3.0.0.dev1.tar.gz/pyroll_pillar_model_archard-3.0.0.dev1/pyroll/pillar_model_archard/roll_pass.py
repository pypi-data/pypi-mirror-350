import math
import numpy as np
from pyroll.core import RollPass, Roll, Hook, root_hooks
from pyroll.freiberg_flow_stress import flow_stress
from shapely import LineString, MultiLineString, Polygon, MultiPolygon, clip_by_rect
from shapely.affinity import translate, rotate

Roll.wear_coefficient = Hook[float]()
"""Wear coefficient for the roll."""

Roll.vickers_hardness = Hook[float]()
"""Vickers hardness of the roll material."""

RollPass.Roll.pillars_wear_length = Hook[np.ndarray]()
"""Length of the entry section until the neutral point for each pillar."""

RollPass.Roll.pillars_wear_depth = Hook[np.ndarray]()
"""Resulting wear depth for each pillar element on the roll surface for one revolution."""

RollPass.Roll.total_pillars_wear_depth = Hook[np.ndarray]()
"""Resulting wear depth for each pillar element on the roll surface for a number of rolled billets."""

RollPass.Roll.wear_contour_line = Hook[LineString]()
"""Contour line of the wear profile of the roll."""

RollPass.wear_contour_lines = Hook[LineString]()
"""Contour lines of the wear profile of the roll pass."""

RollPass.number_of_rolled_billets = Hook[float]()
"""Number of rolled billets in this roll pass."""

RollPass.OutProfile.pillars_deformation_resistance = Hook[np.ndarray]()
"""Deformation resistance for each pillar element."""

RollPass.DiskElement.pillars_relative_velocity = Hook[np.ndarray]()
"""Relative velocity for each pillar against the roll surface."""

RollPass.Roll.max_wear_depth = Hook[float]()
"""Max. depth of the wear contour."""

RollPass.Roll.wear_area = Hook[float]()
"""Worn area of the groove."""

RollPass.Roll.wear_cross_section = Hook[Polygon]()
"""Wear cross section of the groove."""


@RollPass.DiskElement.pillars_relative_velocity
def pillars_relative_velocity(self: RollPass.DiskElement) -> np.ndarray:
    roll = self.roll_pass.roll

    local_roll_radii = np.concatenate(
        [roll.max_radius - roll.surface_interpolation(0, center)
         for center in self.roll_pass.in_profile.pillars],
        axis=0).flatten()

    horizontal_roll_velocities = local_roll_radii * roll.rotational_frequency * 2 * np.pi * np.cos(
        self.pillar_longitudinal_angles)

    return self.pillar_velocities - horizontal_roll_velocities


@RollPass.Roll.pillars_wear_length
def pillars_wear_length(self: RollPass.Roll) -> np.ndarray:
    local_roll_radii = np.concatenate(
        [self.max_radius - self.surface_interpolation(0, center)
         for center in self.roll_pass.in_profile.pillars],
        axis=0).flatten()

    pillars_wear_length = np.zeros_like(self.roll_pass.in_profile.pillars)

    for de in self.roll_pass.disk_elements:
        horizontal_roll_velocities = local_roll_radii * self.rotational_frequency * 2 * np.pi * np.cos(
            de.pillar_longitudinal_angles)
        for i, pillars in enumerate(de.in_profile.pillars):
            if de.pillar_velocities[i] < horizontal_roll_velocities[i] and de.pillars_in_contact[i]:
                pillars_wear_length[i] += de.length

    return pillars_wear_length


@RollPass.OutProfile.pillars_flow_stress
def pillars_flow_stress(self: RollPass.OutProfile) -> np.ndarray:
    if hasattr(self, "freiberg_flow_stress_coefficients"):
        return flow_stress(
            self.freiberg_flow_stress_coefficients,
            self.roll_pass.total_pillar_strains,
            self.roll_pass.total_pillar_strain_rates,
            self.temperature
        )


@RollPass.OutProfile.pillars_deformation_resistance
def pillars_deformation_resistance(self: RollPass.OutProfile) -> np.ndarray:
    return self.pillars_flow_stress / self.roll_pass.rolling_efficiency


@RollPass.Roll.pillars_wear_depth
def pillars_wear_depth(self: RollPass.Roll) -> np.ndarray:
    return self.wear_coefficient * self.roll_pass.out_profile.pillars_deformation_resistance * self.pillars_wear_length / (
            3 * self.vickers_hardness)


@RollPass.Roll.total_pillars_wear_depth
def total_pillars_wear_depth(self: RollPass.Roll) -> np.ndarray:
    if hasattr(self.roll_pass.in_profile, "length"):
        return self.pillars_wear_depth * self.roll_pass.out_profile.length * self.roll_pass.number_of_rolled_billets


@RollPass.Roll.wear_contour_line
def wear_contour_line(self: RollPass.Roll) -> LineString:
    wear_depth_with_groove_contour = self.groove.local_depth(
        self.roll_pass.out_profile.pillars) + self.total_pillars_wear_depth

    right_side = list(zip(self.roll_pass.out_profile.pillars, wear_depth_with_groove_contour))
    left_side = list(zip(-self.roll_pass.out_profile.pillars[::-1], wear_depth_with_groove_contour[::-1]))

    combined_contour_list = left_side + right_side
    wear_contour = LineString(combined_contour_list)
    return wear_contour


@RollPass.wear_contour_lines
def wear_contour_lines(self: RollPass) -> LineString:
    upper = translate(self.roll.wear_contour_line, yoff=self.gap / 2)
    lower = rotate(upper, angle=180, origin=(0, 0))

    wear_contour_lines = MultiLineString([upper, lower])

    return wear_contour_lines


@RollPass.Roll.max_wear_depth
def max_wear_depth(self: RollPass.Roll) -> float:
    return self.contour_line.distance(self.wear_contour_line)


@RollPass.Roll.wear_cross_section
def wear_cross_section(self: RollPass.Roll):

    start_wcl = self.roll_pass.roll.wear_contour_line.coords[0][0]
    end_wcl = self.roll_pass.roll.wear_contour_line.coords[-1][0]
    boundary = list(self.roll_pass.roll.contour_line.coords) + list(reversed(self.roll_pass.roll.wear_contour_line.coords))
    _poly = Polygon(boundary)
    _clipped_poly = clip_by_rect(_poly, start_wcl, -math.inf, end_wcl, math.inf)

    return _clipped_poly


@RollPass.Roll.wear_area
def wear_area(self: RollPass.Roll):
    return self.wear_cross_section.area


root_hooks.add(RollPass.Roll.wear_contour_line)
root_hooks.add(RollPass.wear_contour_lines)
root_hooks.add(RollPass.Roll.max_wear_depth)
root_hooks.add(RollPass.Roll.wear_cross_section)
