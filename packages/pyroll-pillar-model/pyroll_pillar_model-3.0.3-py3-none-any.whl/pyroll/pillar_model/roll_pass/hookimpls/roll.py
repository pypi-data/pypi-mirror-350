import numpy as np
from scipy.optimize import root_scalar

from pyroll.core import RollPass


@RollPass.Roll.total_pillar_contact_lengths
def total_pillar_contact_lengths(self: RollPass.Roll):
    contact_lengths = np.zeros_like(self.roll_pass.in_profile.pillars)

    for de in self.roll_pass.disk_elements:
        for i, pillars in enumerate(de.in_profile.pillars):
            if de.pillars_in_contact[i]:
                contact_lengths[i] += de.length

    return contact_lengths


@RollPass.Roll.total_pillar_contact_areas
def roll_contact_area(self: RollPass.Roll):
    contact_areas = np.zeros_like(self.roll_pass.in_profile.pillars)

    for de in self.roll_pass.disk_elements:
        for i, pillars in enumerate(de.in_profile.pillars):
            if de.pillars_in_contact[i]:
                area = (de.in_profile.pillar_widths[i] + de.out_profile.pillar_widths[i]) / 2 * de.length
                contact_areas[i] += area

    return contact_areas


@RollPass.Roll.contact_area
def roll_contact_area(self: RollPass.Roll):
    return self.roll_pass.contact_area / 2


@RollPass.Roll.pillar_entry_angles
def pillar_entry_angles(self: RollPass.Roll):
    rp = self.roll_pass

    entry_points_sol = []
    for center, height in zip(rp.in_profile.pillars, rp.in_profile.pillar_heights):
        try:
            sol = root_scalar(lambda x: height - rp.gap - 2 * self.surface_interpolation(x, center),
                              x0=rp.entry_point * 0.9,
                              x1=rp.entry_point * 1.1)

            entry_points_sol.append(sol.root)

        except ValueError:
            entry_points_sol.append(0)

    entry_points = []
    for points in entry_points_sol:
        if isinstance(points, np.ndarray):
            entry_points.append(points.flatten()[0])
        else:
            entry_points.append(points)

    local_roll_radii = np.concatenate(
        [self.max_radius - self.surface_interpolation(0, center)
         for center in rp.in_profile.pillars],
        axis=0).flatten()

    entry_angles = np.asarray([np.arcsin(entry_point / local_radius) for entry_point, local_radius in
                    zip(entry_points, local_roll_radii)])

    return entry_angles
