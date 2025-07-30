import shapely
import numpy as np

from pyroll.core import RollPass
from ..pillar_disk_element import PillarDiskElement


@PillarDiskElement.pillars_in_contact
def pillars_in_contact(self: PillarDiskElement):
    rp = self.roll_pass
    contour = rp.roll.surface_interpolation(self.out_profile.x, self.out_profile.pillars).squeeze()
    contacts = self.in_profile.pillar_heights / 2 > contour + rp.gap / 2
    return contacts


@PillarDiskElement.OutProfile.pillar_heights
def pillar_heights(self: PillarDiskElement.OutProfile):
    de = self.disk_element
    rp = de.roll_pass
    heights = de.in_profile.pillar_heights.copy()
    heights[de.pillars_in_contact] = rp.roll.surface_interpolation(
        de.out_profile.x,
        de.out_profile.pillars[de.pillars_in_contact]
    ).squeeze() * 2 + rp.gap
    return heights


@PillarDiskElement.pillar_draughts
def pillar_draughts(self: PillarDiskElement):
    return self.out_profile.pillar_heights / self.in_profile.pillar_heights


@PillarDiskElement.pillar_spreads
def pillar_spreads(self: PillarDiskElement):
    return np.ones_like(self.in_profile.pillars)


@PillarDiskElement.pillar_spreads(wrapper=True)
def corrected_pillar_spreads(self: RollPass.DiskElement, cycle: bool):
    from ... import Config
    if Config.ELONGATION_CORRECTION:
        if cycle:
            return None

        spreads = (yield) * self.roll_pass.pillar_spread_correction_coefficients
        return spreads


@PillarDiskElement.pillar_elongations
def pillar_elongations(self: PillarDiskElement):
    return 1 / (self.pillar_draughts * self.pillar_spreads)


@PillarDiskElement.pillar_velocities
def pillar_velocities(self: PillarDiskElement):
    return self.in_profile.velocity * self.pillar_elongations


@PillarDiskElement.pillar_log_draughts
def pillar_log_draughts(self: PillarDiskElement):
    return np.log(self.pillar_draughts)


@PillarDiskElement.pillar_log_spreads
def pillar_log_spreads(self: PillarDiskElement):
    return np.log(self.pillar_spreads)


@PillarDiskElement.pillar_log_elongations
def pillar_log_elongations(self: PillarDiskElement):
    return np.log(self.pillar_elongations)


@PillarDiskElement.pillar_strains
def pillar_strains(self: PillarDiskElement):
    if self == self.roll_pass.disk_elements[0]:
        previous_contact = np.full_like(self.pillars_in_contact, False)
    else:
        previous_disk_element = self.prev_of(unit_type=type(self))
        previous_contact = previous_disk_element.pillars_in_contact

    strains = np.sqrt(
        2 / 3 * (self.pillar_log_elongations ** 2 + self.pillar_log_spreads ** 2 + self.pillar_log_draughts ** 2))

    for i in range(len(self.in_profile.pillars)):
        if self.pillars_in_contact[i] and not previous_contact[i]:
            strains[i] = strains[i] + self.roll_pass.pillar_corner_correction_strains[i]

    return strains


@PillarDiskElement.OutProfile.pillar_strains
def pillar_strains(self: PillarDiskElement.OutProfile):
    return self.disk_element.in_profile.pillar_strains + self.disk_element.pillar_strains


@PillarDiskElement.pillar_strain_rates
def pillar_strain_rates(self: PillarDiskElement):
    p_strain_rates = np.zeros_like(self.in_profile.pillars)
    for i, pillar in enumerate(self.in_profile.pillars):
        if self.pillars_in_contact[i]:
            p_strain_rates[i] = self.pillar_velocities[i] * self.pillar_strains[i] / self.length

    return p_strain_rates


@PillarDiskElement.OutProfile.pillar_widths
def out_pillar_widths(self: PillarDiskElement.OutProfile):
    de = self.disk_element
    return de.in_profile.pillar_widths * de.pillar_spreads


@PillarDiskElement.OutProfile.pillar_boundaries
def out_pillar_boundaries(self: PillarDiskElement.OutProfile):
    a = np.zeros(len(self.pillar_widths) + 1)
    a[1:] = np.cumsum(self.pillar_widths) - self.pillar_widths[0] / 2
    return a


@PillarDiskElement.OutProfile.pillars
def out_pillars(self: PillarDiskElement.OutProfile):
    if not self.has_set_or_cached("pillars"):
        return self.disk_element.in_profile.pillars

    a = np.zeros(len(self.pillar_boundaries) - 1)
    a[1:] = (self.pillar_boundaries[2:] + self.pillar_boundaries[1:-1]) / 2
    return a


@PillarDiskElement.OutProfile.cross_section
def out_cross_section(self: PillarDiskElement.OutProfile):
    coords1 = np.column_stack([self.pillars, self.pillar_heights / 2])
    coords2 = coords1[::-1].copy()
    coords2[:, 1] *= -1
    coords3 = coords1[1:].copy()
    coords3 *= -1
    coords4 = coords2[:-1].copy()
    coords4 *= -1
    outer = self.pillar_boundaries[-1]

    cs = shapely.Polygon(np.vstack(
        [
            coords1,
            [(outer, 0)],
            coords2,
            coords3,
            [(-outer, 0)],
            coords4,
        ]
    )
    )
    return cs


@PillarDiskElement.pillar_longitudinal_angles
def pillar_longitudinal_angles(self: PillarDiskElement):
    dy = (self.out_profile.pillar_heights - self.in_profile.pillar_heights) / 2
    return np.arctan2(dy, self.length)


@PillarDiskElement.pillar_longitudinal_height_derivatives
def pillar_longitudinal_height_derivatives(self: PillarDiskElement):
    return (self.out_profile.pillar_heights - self.in_profile.pillar_heights) / self.length
