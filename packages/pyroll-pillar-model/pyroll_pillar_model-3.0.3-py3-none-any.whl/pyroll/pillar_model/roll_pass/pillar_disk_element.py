import pyroll
import numpy as np

from pyroll.core import RollPass, Hook


@RollPass.DiskElement.extension_class
class PillarDiskElement(RollPass.DiskElement):
    pillars_in_contact = Hook[np.ndarray]()
    """Array of booleans indicating if a pillar has contact to the rolls."""

    pillar_spreads = Hook[np.ndarray]()
    """Array of spread values for each pillar."""

    pillar_draughts = Hook[np.ndarray]()
    """Array of draught values for each pillar."""

    pillar_elongations = Hook[np.ndarray]()
    """Array of elongation values for each pillar."""

    pillar_log_spreads = Hook[np.ndarray]()
    """Array of log spread values for each pillar."""

    pillar_log_draughts = Hook[np.ndarray]()
    """Array of log draught values for each pillar."""

    pillar_log_elongations = Hook[np.ndarray]()
    """Array of log elongation values for each pillar."""

    pillar_strains = Hook[np.ndarray]()
    """Array of strain values for each pillar."""

    pillar_strain_rates = Hook[np.ndarray]()
    """Array of strain rate values for each pillar."""

    pillar_velocities = Hook[np.ndarray]()
    """Array of velocity values for each pillar."""

    pillar_longitudinal_angles = Hook[np.ndarray]()
    """Array of pillars' angles between pillar and tooling (roll) in rolling (x) direction."""

    pillar_longitudinal_height_derivatives = Hook[np.ndarray]()
    """Arrays of pillar height derivatives in rolling (x) direction."""


pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillars)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillar_heights)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillar_widths)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillar_areas)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.pillar_strains)

pyroll.core.root_hooks.add(pyroll.core.RollPass.OutProfile.pillars)
pyroll.core.root_hooks.add(pyroll.core.Rotator.OutProfile.pillars)
pyroll.core.root_hooks.add(pyroll.core.Rotator.OutProfile.pillar_heights)
pyroll.core.root_hooks.add(pyroll.core.Rotator.OutProfile.pillar_widths)
pyroll.core.root_hooks.add(pyroll.core.Rotator.OutProfile.pillar_areas)
