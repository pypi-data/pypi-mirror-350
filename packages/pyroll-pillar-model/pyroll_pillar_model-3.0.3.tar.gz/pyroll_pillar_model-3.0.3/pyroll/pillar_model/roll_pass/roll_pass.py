import pyroll
import numpy as np

from pyroll.core import RollPass, Hook

RollPass.total_pillar_elongations = Hook[np.ndarray]()
"""Array of total elongation for each pillar for a roll pass."""

RollPass.total_pillar_spreads = Hook[np.ndarray]()
"""Array of total spread for each pillar for a roll pass."""

RollPass.total_pillar_draughts = Hook[np.ndarray]()
"""Array of total drought for each pillar for a roll pass."""

RollPass.total_pillar_log_elongations = Hook[np.ndarray]()
"""Array of total logarithmic elongation for each pillar for a roll pass."""

RollPass.total_pillar_log_spreads = Hook[np.ndarray]()
"""Array of total logarithmic spread for each pillar for a roll pass."""

RollPass.total_pillar_log_draughts = Hook[np.ndarray]()
"""Array of total logarithmic drought for each pillar for a roll pass."""

RollPass.total_pillar_strains = Hook[np.ndarray]()
"""Array of total strains for each pillar for a roll pass."""

RollPass.total_pillar_strain_rates = Hook[np.ndarray]()
"""Array of total strain rates for each pillar for a roll pass."""

RollPass.Roll.total_pillar_contact_lengths = Hook[np.ndarray]()
"""Array of total contact length of each pillar in contact."""

RollPass.Roll.total_pillar_contact_areas = Hook[np.ndarray]()
"""Array of total contact area of each pillar in contact."""

RollPass.Roll.pillar_entry_angles = Hook[np.ndarray]()
"""Array of entry angles of each pillar in contact."""

RollPass.mean_elongation = Hook[float]()
"""Mean elongation of the profile in the roll pass."""

RollPass.pillar_spread_correction_coefficients = Hook[np.ndarray]()
"""Array of correction coefficients for pillar spreads of a roll pass."""

RollPass.pillar_corner_correction_strains = Hook[np.ndarray]()
"""Strain of the pillars due to shearing while entering the roll gap."""

pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_elongations)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_spreads)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_draughts)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_log_elongations)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_log_spreads)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_log_draughts)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_strains)
pyroll.core.root_hooks.add(pyroll.core.RollPass.total_pillar_strain_rates)
pyroll.core.root_hooks.add(pyroll.core.DeformationUnit.OutProfile.velocity)
pyroll.core.root_hooks.add(pyroll.core.RollPass.InProfile.velocity)
