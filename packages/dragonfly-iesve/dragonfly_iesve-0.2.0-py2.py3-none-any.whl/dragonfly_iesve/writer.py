# coding: utf-8
"""Write a gem file from a Dragonfly model."""
from __future__ import division

from honeybee_ies.writer import model_to_gem as hb_model_to_gem


def model_to_gem(model, use_multiplier=True, exclude_plenums=False):
    """Generate an IES GEM string from a Dragonfly Model.

    Args:
        model: A dragonfly Model.
        use_multiplier: Boolean to note whether the multipliers on each Building
            story will be passed along to the Room objects or if full geometry
            objects should be written for each repeated story in the
            building. (Default: True).
        exclude_plenums: Boolean to indicate whether ceiling/floor plenum depths
            assigned to Room2Ds should generate distinct 3D Rooms in the
            translation. (Default: False).

    Returns:
        Path to exported GEM file.
    """
    hb_model = model.to_honeybee(
        'District', use_multiplier=use_multiplier, exclude_plenums=exclude_plenums,
        solve_ceiling_adjacencies=False, enforce_adj=False, enforce_solid=True)[0]
    return hb_model_to_gem(hb_model)
