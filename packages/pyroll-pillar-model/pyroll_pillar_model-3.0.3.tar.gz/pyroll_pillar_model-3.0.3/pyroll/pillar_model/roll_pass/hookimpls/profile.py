import numpy as np
from pyroll.core import RollPass
from more_itertools import first_true


@RollPass.OutProfile.cross_section
def rp_out_cross_section(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.roll_pass.disk_elements[-1].out_profile.cross_section


@RollPass.OutProfile.width
def rp_out_width(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.cross_section.width


@RollPass.OutProfile.pillar_boundaries
def rp_out_pillar_boundaries(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.roll_pass.disk_elements[-1].out_profile.pillar_boundaries


@RollPass.OutProfile.pillars
def rp_out_pillars(self: RollPass.OutProfile):
    if self.roll_pass.disk_elements:
        return self.roll_pass.disk_elements[-1].out_profile.pillars

@RollPass.InProfile.velocity
def rp_in_velocity(self: RollPass.InProfile):
    try:
        neutral_disk = first_true(
            self.roll_pass.disk_elements,
            pred=lambda de: de.out_profile.x > self.roll_pass.roll.neutral_point
        )
    except AttributeError:  # first iteration: disks are not solved
        return self.roll_pass.velocity * self.roll_pass.out_profile.cross_section.area / self.cross_section.area

    neutral_velocity = (
            2 * np.pi * self.roll_pass.roll.rotational_frequency * self.roll_pass.roll.working_radius * np.cos(
        self.roll_pass.roll.neutral_angle)
    )
    weight = (self.roll_pass.roll.neutral_point - neutral_disk.in_profile.x) / neutral_disk.length
    neutral_cross_section = weight * neutral_disk.out_profile.cross_section.area + (
            1 - weight) * neutral_disk.in_profile.cross_section.area

    return neutral_velocity * neutral_cross_section / self.cross_section.area


@RollPass.OutProfile.velocity
def rp_out_velocity(self: RollPass.OutProfile):
    return self.roll_pass.disk_elements[-1].out_profile.velocity
