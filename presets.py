# SPDX-License-Identifier: GPL-3.0-or-later
"""Built-in looks: a pattern plus input values.

Values are node input names. Plain names are looked up in the pattern,
then the placement ("Transform") and finish groups; use "Transform.Scale"
or "Finish.Invert" to be explicit. Angles are in degrees here.
"""

import math

from . import patterns

# The preset browser reads as tidy folders: presets are shown grouped by
# category (Frames, Meshwork, Botanical, Atmosphere, Graphic, Lines & Shapes)
# in the order the categories are declared. Keep the folder list at ten or
# fewer so the browser never becomes an endless tree. The original index is
# still carried as the enum number, keeping identifiers stable.

# (id, label, category, pattern id, values)
PRESETS = [
    # -- frames and glass --------------------------------------------
    ('QUAD_PANE', 'Quad Pane', 'FRAMES', 'PANES', {'Columns': 2.0, 'Rows': 2.0}),
    ('SIX_LIGHT', 'Six-Light Frame', 'FRAMES', 'PANES', {}),
    ('DIAMOND_CASEMENT', 'Diamond Casement', 'FRAMES', 'PANES', {'Columns': 4.0, 'Rows': 4.0, 'Diagonals': 1.0, 'Width': 0.9, 'Height': 0.95, 'Bars': 0.03}),
    ('TALL_SASH', 'Tall Sash', 'FRAMES', 'PANES', {'Columns': 3.0, 'Rows': 5.0, 'Width': 0.62, 'Height': 0.96, 'Bars': 0.015}),
    ('PANE_FOLIAGE', 'Pane and Foliage', 'FRAMES', 'PANES', {'Leaves': 0.7}),
    ('LOUVERS', 'Louvers', 'FRAMES', 'SLATS', {}),
    ('LOUVER_PALM', 'Louvers and Palm', 'FRAMES', 'SLATS', {'Plants': 0.85, 'Openness': 0.6}),
    ('SLIT_LOUVERS', 'Slit Louvers', 'FRAMES', 'SLATS', {'Slats': 24.0, 'Openness': 0.3, 'Mullion': 0.0, 'Width': 0.95}),
    ('ROSETTE', 'Rosette', 'FRAMES', 'ROSETTE', {}),
    ('ROSETTE_JEWEL', 'Jewel Rosette', 'FRAMES', 'ROSETTE', {'Segments': 16.0, 'Colour': 0.9, 'Leading': 0.4}),
    ('OCTO_BLOOM', 'Octo Bloom', 'FRAMES', 'ROSETTE', {'Segments': 8.0, 'Hub': 0.24, 'Petal': 1.1, 'Leading': 0.0}),
    ('LANCET_TRIO', 'Lancet Arches', 'FRAMES', 'LANCET', {}),
    ('LANCET_JEWEL', 'Jewel Lancets', 'FRAMES', 'LANCET', {'Lancets': 4.0, 'Colour': 0.9, 'Quarries': 12.0}),
    ('FRACTURE', 'Fracture', 'FRAMES', 'FRACTURE', {}),
    ('IMPACT_PANE', 'Impact Pane', 'FRAMES', 'FRACTURE', {'Missing': 0.35, 'Shards': 22.0, 'Fine Cracks': 1.0, 'Impact X': -0.15}),
    # -- meshwork and metal ------------------------------------------
    ('DIAMOND_TRELLIS', 'Diamond Trellis', 'MESHWORK', 'MESH', {'Angle': 45.0, 'Cells': 7.0, 'Hole Size': 0.72}),
    ('FINE_MESH', 'Fine Mesh', 'MESHWORK', 'MESH', {'Angle': 45.0, 'Cells': 12.0, 'Hole Size': 0.62, 'Aspect': 1.5}),
    ('SLOT_GRATE', 'Slot Grate', 'MESHWORK', 'MESH', {'Cells': 9.0, 'Aspect': 0.7, 'Hole Size': 0.62, 'Roundness': 0.35}),
    ('PUNCH_PLATE', 'Punch Plate', 'MESHWORK', 'MESH', {'Cells': 12.0, 'Hole Size': 0.62, 'Roundness': 1.0, 'Stagger': 1.0}),
    ('HIVE', 'Hive', 'MESHWORK', 'CELLS', {}),
    ('HEX_MOSAIC', 'Hex Mosaic', 'MESHWORK', 'CELLS', {'Cells': 5.0, 'Closed': 0.45, 'Bar': 0.12}),
    ('ARABESQUE', 'Arabesque Screen', 'MESHWORK', 'ARABESQUE', {}),
    ('STAR_NET', 'Star Net', 'MESHWORK', 'ARABESQUE', {'Cells': 6.0, 'Star': 0.27, 'Bar': 0.09, 'Rosette': 0.0}),
    ('FILIGREE_CAGE', 'Filigree Cage', 'MESHWORK', 'WROUGHT', {'Leaves': 0.85}),
    ('BAR_GATE', 'Bar Gate', 'MESHWORK', 'WROUGHT', {'Bars': 12.0}),
    ('DUCTWORK', 'Ductwork', 'MESHWORK', 'DUCTS', {}),
    ('WIRE_COILS', 'Wire Coils', 'MESHWORK', 'WIRE', {}),
    ('CRACKLE_LINES', 'Crackle Lines', 'MESHWORK', 'CRACKLE', {}),
    ('DRY_EARTH', 'Dry Earth', 'MESHWORK', 'CRACKLE', {'Scale': 3.0, 'Line Width': 0.12, 'Distortion': 0.8}),
    ('FINE_CRACKS', 'Fine Cracks', 'MESHWORK', 'CRACKLE', {'Scale': 8.0, 'Line Width': 0.05, 'Distortion': 0.4}),
    # -- botanical ---------------------------------------------------
    ('LEAF_SCATTER', 'Leaf Scatter', 'BOTANICAL', 'LEAFY', {}),
    ('THICK_FOLIAGE', 'Thick Foliage', 'BOTANICAL', 'LEAFY', {'Density': 9.0, 'Coverage': 1.0, 'Depth': 0.8}),
    ('CREEPER', 'Creeper', 'BOTANICAL', 'LEAFY', {'Leaf Width': 0.75, 'Leaf Size': 0.7, 'Stems': 1.0, 'Density': 8.0}),
    ('LEAF_BORDER', 'Leaf Border', 'BOTANICAL', 'LEAFY', {'Frame': 1.0, 'Coverage': 1.0}),
    ('BLOSSOM_FALL', 'Blossom Fall', 'BOTANICAL', 'LEAFY', {'Density': 3.5, 'Leaf Size': 1.2, 'Leaf Width': 0.55, 'Stems': 0.0, 'Depth': 0.0, 'Coverage': 0.9}),
    ('FROND_CLUSTER', 'Frond Cluster', 'BOTANICAL', 'FRONDS', {}),
    ('FROND_THICKET', 'Frond Thicket', 'BOTANICAL', 'FRONDS', {'Count': 11.0, 'Length': 0.85}),
    ('FAN_PALM', 'Fan Palm', 'BOTANICAL', 'FANPALM', {}),
    ('ARCHING_LEAVES', 'Arching Leaves', 'BOTANICAL', 'REEDS', {}),
    ('MEADOW_REEDS', 'Meadow Reeds', 'BOTANICAL', 'REEDS', {'Layout': 1.0, 'Origin Y': -0.75, 'Count': 14.0, 'Blade Width': 0.02, 'Length': 0.85, 'Spread': 100.0, 'Bend': 0.8}),
    ('CANE_GROVE', 'Cane Grove', 'BOTANICAL', 'CANE', {}),
    ('CANE_LEAVES', 'Cane and Leaves', 'BOTANICAL', 'CANE', {'Leaves': 1.0, 'Stalks': 3.0, 'Leaf Density': 5.0}),
    ('LIMBS', 'Limbs', 'BOTANICAL', 'LIMBS', {}),
    ('WINTER_TREE', 'Winter Tree', 'BOTANICAL', 'LIMBS', {'Layout': 1.0, 'Count': 4.0, 'Twigs': 14.0, 'Thickness': 0.03, 'Length': 1.3, 'Network': 0.2}),
    ('TWIG_KNOT', 'Twig Knot', 'BOTANICAL', 'LIMBS', {'Count': 2.0, 'Network': 1.0, 'Scale': 3.0, 'Twig Width': 0.006}),
    ('TREETOP', 'Treetop Cover', 'BOTANICAL', 'LIMBS', {'Leaves': 1.0, 'Frame': 0.6, 'Thickness': 0.025}),
    ('NEEDLE_SPRIG', 'Needle Sprig', 'BOTANICAL', 'NEEDLES', {}),
    ('RAINFOREST', 'Rainforest Curtain', 'BOTANICAL', 'TENDRILS', {'Frame': 1.0, 'Strands': 16.0, 'Length': 0.9, 'Leaf Size': 0.04}),
    ('DESERT_CACTI', 'Desert Cacti', 'BOTANICAL', 'DESERT', {}),
    ('DAPPLED_SUN', 'Dappled Sunlight', 'BOTANICAL', 'DAPPLE', {}),
    ('SOFT_DAPPLE', 'Soft Dapple', 'BOTANICAL', 'DAPPLE', {'Density': 4.0, 'Spot Size': 1.1, 'Softness': 0.45, 'Coverage': 0.8, 'Shade': 0.15}),
    ('CANOPY_SPECKS', 'Canopy Specks', 'BOTANICAL', 'DAPPLE', {'Density': 14.0, 'Spot Size': 0.6, 'Coverage': 0.55, 'Softness': 0.1, 'Variation': 0.9}),
    ('STRETCHED_DAPPLE', 'Stretched Dapple', 'BOTANICAL', 'DAPPLE', {'Elongate': 1.2, 'Angle': 30.0, 'Density': 7.0, 'Warp': 0.8}),
    # -- atmosphere --------------------------------------------------
    ('DUSTY_SILK', 'Dusty Silk', 'ATMOSPHERE', 'SILK', {}),
    ('FAINT_SILK', 'Faint Silk', 'ATMOSPHERE', 'SILK', {'Detail': 0.25, 'Clumps': 0.2, 'Haze': 0.0, 'Strands': 0.002}),
    ('NEON_SILK', 'Neon Silk', 'ATMOSPHERE', 'SILK', {'Finish.Invert': 1.0, 'Strands': 0.004}),
    ('ORB_WEB', 'Orb Web', 'ATMOSPHERE', 'ORB', {}),
    ('CORNER_ORB', 'Corner Orb', 'ATMOSPHERE', 'ORB', {'Center X': 0.35, 'Center Y': 0.35, 'Broken': 0.25}),
    ('VOILE', 'Voile', 'ATMOSPHERE', 'DRAPE', {}),
    ('SWAGGED_DRAPE', 'Swagged Drape', 'ATMOSPHERE', 'DRAPE', {'Swag': 1.0, 'Folds': 4.0}),
    ('LACE_NET', 'Lace Net', 'ATMOSPHERE', 'DRAPE', {'Lace': 0.9, 'Opacity': 0.35, 'Lace Scale': 3.0}),
    ('WATER_RIPPLE', 'Water Ripple', 'ATMOSPHERE', 'RIPPLE', {}),
    ('POOL_GLOW', 'Poolside Glow', 'ATMOSPHERE', 'RIPPLE', {'Scale': 7.0, 'Sharpness': 0.03, 'Darkness': 0.4, 'Finish.Tint': (0.75, 0.92, 1.0)}),
    ('MOTTLE', 'Mottle', 'ATMOSPHERE', 'MOTTLE', {}),
    ('SOFT_SPECKLE', 'Soft Speckle', 'ATMOSPHERE', 'MOTTLE', {'Scale': 6.0, 'Coverage': 0.45, 'Softness': 0.15}),
    # -- graphic ---------------------------------------------------------------------
    ('STRIPE_BARS', 'Stripe Bars', 'GRAPHIC', 'STRIPES', {'Count': 10.0}),
    ('RIPPLE_STRIPES', 'Ripple Stripes', 'GRAPHIC', 'STRIPES', {'Count': 14.0, 'Wave Amount': 0.35, 'Wave Frequency': 4.0}),
    ('DIAGONAL_RAKE', 'Diagonal Rake', 'GRAPHIC', 'STRIPES', {'Count': 18.0, 'Angle': 35.0, 'Width': 0.3}),
    ('FLOWING_LINES', 'Flowing Lines', 'GRAPHIC', 'STRIPES', {'Count': 24.0, 'Width': 0.35, 'Wave Amount': 0.8, 'Wave Frequency': 2.0}),
    ('POLKA', 'Polka Dots', 'GRAPHIC', 'DOTS', {'Cells': 8.0, 'Dot Size': 0.65}),
    ('HALFTONE_FADE', 'Halftone Fade', 'GRAPHIC', 'DOTS', {'Cells': 18.0, 'Dot Size': 0.95, 'Gradient': 1.0}),
    ('PIN_PRICKS', 'Pin Pricks', 'GRAPHIC', 'DOTS', {'Cells': 28.0, 'Dot Size': 0.28}),
    ('DOT_GRID', 'Square Dot Grid', 'GRAPHIC', 'DOTS', {'Cells': 10.0, 'Dot Size': 0.5, 'Stagger': 0.0}),
    ('SUN_RAYS', 'Sun Rays', 'GRAPHIC', 'SUNBURST', {'Ray Width': 0.4}),
    ('PINWHEEL', 'Pinwheel', 'GRAPHIC', 'SUNBURST', {'Rays': 10.0, 'Twist': 0.35, 'Ray Width': 0.5}),
    ('FAN_BEAM', 'Fan Beam', 'GRAPHIC', 'SUNBURST', {'Rays': 7.0, 'Ray Width': 0.25, 'Hub': 0.12}),
    ('TARGET_RINGS', 'Target Rings', 'GRAPHIC', 'RINGS', {}),
    ('BROKEN_HALO', 'Broken Halo', 'GRAPHIC', 'RINGS', {'Rings': 5.0, 'Ring Width': 0.3, 'Break': 0.35, 'Break Count': 14.0}),
    ('WOBBLE_RINGS', 'Wobble Rings', 'GRAPHIC', 'RINGS', {'Rings': 9.0, 'Wobble': 0.6, 'Lobes': 5.0, 'Ring Width': 0.4}),
    ('SPIRAL_ARMS', 'Spiral Arms', 'GRAPHIC', 'SPIRAL', {}),
    ('VORTEX', 'Vortex', 'GRAPHIC', 'SPIRAL', {'Arms': 5.0, 'Twist': 3.5, 'Arm Width': 0.35}),
    ('SNAIL_SPIRAL', 'Snail Spiral', 'GRAPHIC', 'SPIRAL', {'Arms': 1.0, 'Twist': 4.0, 'Arm Width': 0.5}),
    ('BASKET_WEAVE', 'Basket Weave', 'GRAPHIC', 'WEAVE', {}),
    ('FINE_WEAVE', 'Fine Weave', 'GRAPHIC', 'WEAVE', {'Cells': 14.0, 'Strips': 4.0, 'Gap': 0.2}),
    ('RATTAN_WEAVE', 'Rattan Weave', 'GRAPHIC', 'WEAVE', {'Cells': 5.0, 'Strips': 3.0, 'Gap': 0.35, 'Angle': 45.0}),
    ('BREEZE_BLOCK', 'Breeze Block', 'GRAPHIC', 'BRICKWORK', {}),
    ('RUBBLE_WALL', 'Rubble Wall', 'GRAPHIC', 'BRICKWORK', {'Solid': 0.3, 'Roundness': 0.6, 'Mortar': 0.2}),
    ('STACKED_BOND', 'Stacked Bond', 'GRAPHIC', 'BRICKWORK', {'Offset': 0.0, 'Aspect': 1.0, 'Rows': 7.0, 'Mortar': 0.18, 'Roundness': 0.5}),
    ('RAIN_ON_GLASS', 'Rain on Glass', 'GRAPHIC', 'RAINDROPS', {}),
    ('DRIZZLE', 'Drizzle', 'GRAPHIC', 'RAINDROPS', {'Density': 26.0, 'Drop Size': 0.35, 'Coverage': 0.8}),
    ('STREAKY_RAIN', 'Streaky Rain', 'GRAPHIC', 'RAINDROPS', {'Elongate': 1.6, 'Density': 12.0, 'Drop Size': 0.6}),
    ('STAR_FIELD', 'Star Scatter', 'GRAPHIC', 'STARS', {}),
    ('TWINKLE_FIELD', 'Twinkle Field', 'GRAPHIC', 'STARS', {'Density': 11.0, 'Star Size': 0.7, 'Points': 4.0, 'Sharpness': 0.8}),
    ('BIG_STARS', 'Big Stars', 'GRAPHIC', 'STARS', {'Density': 3.5, 'Star Size': 1.0, 'Points': 6.0, 'Sharpness': 0.5, 'Coverage': 1.0}),
    ('CIRRUS', 'Cirrus Streaks', 'GRAPHIC', 'STREAKS', {}),
    ('WIND_COMBED', 'Wind Combed', 'GRAPHIC', 'STREAKS', {'Stretch': 14.0, 'Scale': 6.0, 'Coverage': 0.56, 'Softness': 0.05}),
    ('STORM_BANDS', 'Storm Bands', 'GRAPHIC', 'STREAKS', {'Angle': 20.0, 'Coverage': 0.52, 'Softness': 0.12, 'Scale': 2.2, 'Stretch': 4.0}),
    # -- lines and shapes --------------------------------------------
    ('THIN_LINE', 'Thin Line of Light', 'LINES', 'SLIT', {'Width': 0.012}),
    ('HAIRLINE', 'Hairline', 'LINES', 'SLIT', {'Width': 0.004, 'Length': 2.0, 'Softness': 0.0}),
    ('CURTAIN_GAP', 'Curtain Gap', 'LINES', 'SLIT', {'Width': 0.06, 'Length': 2.0, 'Softness': 0.03}),
    ('DOOR_CRACK', 'Door Crack', 'LINES', 'SLIT', {'Width': 0.025, 'Length': 1.4, 'Angle': 90.0}),
    ('BLADE_OF_LIGHT', 'Blade of Light', 'LINES', 'SLIT', {'Width': 0.09, 'Length': 1.2, 'Taper': 1.0, 'Angle': 20.0}),
    ('DIAGONAL_BEAM', 'Diagonal Beam', 'LINES', 'SLIT', {'Width': 0.05, 'Length': 2.0, 'Angle': 35.0, 'Softness': 0.04}),
    ('FADING_STREAK', 'Fading Streak', 'LINES', 'SLIT', {'Width': 0.03, 'Length': 1.3, 'Fade': 1.0, 'Taper': 0.4, 'Softness': 0.03}),
    ('CURVED_SLIVER', 'Curved Sliver', 'LINES', 'SLIT', {'Width': 0.03, 'Bend': 1.2, 'Length': 1.6}),
    ('WAVY_LINE', 'Wavy Line', 'LINES', 'SLIT', {'Width': 0.02, 'Wave Amount': 1.0, 'Wave Frequency': 2.0, 'Length': 2.0}),
    ('TRIPLE_SLITS', 'Triple Slits', 'LINES', 'SLIT', {'Count': 3.0, 'Spacing': 0.14, 'Width': 0.025}),
    ('FINE_COMB', 'Fine Comb', 'LINES', 'SLIT', {'Count': 9.0, 'Spacing': 0.07, 'Width': 0.012, 'Length': 1.0, 'Fade': 0.6}),
    ('RIPPLING_THREADS', 'Rippling Threads', 'LINES', 'SLIT', {'Count': 5.0, 'Spacing': 0.1, 'Width': 0.012, 'Wave Amount': 0.8, 'Wave Frequency': 3.0, 'Length': 2.0}),
    ('DARK_LINE', 'Dark Line', 'LINES', 'SLIT', {'Width': 0.03, 'Length': 2.0, 'Finish.Invert': 1.0}),
    ('CROSSHAIR', 'Crosshair', 'LINES', 'GRIDLINES', {'Columns': 1.0, 'Rows': 1.0, 'Width': 0.03}),
    ('LINE_GRID', 'Line Grid', 'LINES', 'GRIDLINES', {}),
    ('FINE_GRID', 'Fine Grid', 'LINES', 'GRIDLINES', {'Columns': 14.0, 'Rows': 14.0, 'Width': 0.08}),
    ('TILTED_GRID', 'Tilted Grid', 'LINES', 'GRIDLINES', {'Columns': 5.0, 'Rows': 5.0, 'Width': 0.07, 'Angle': 30.0}),
    ('ROUND_SPOT', 'Round Spot', 'LINES', 'SHAPE', {'Width': 0.7, 'Height': 0.7, 'Softness': 0.02}),
    ('SOFT_POOL', 'Soft Pool', 'LINES', 'SHAPE', {'Width': 0.8, 'Height': 0.8, 'Softness': 0.5}),
    ('OVAL_BEAM', 'Oval Beam', 'LINES', 'SHAPE', {'Width': 0.9, 'Height': 0.45, 'Softness': 0.12}),
    ('CAPSULE_BEAM', 'Capsule Beam', 'LINES', 'SHAPE', {'Width': 0.25, 'Height': 0.9, 'Softness': 0.04, 'Angle': 25.0}),
    ('LETTERBOX', 'Letterbox', 'LINES', 'SHAPE', {'Width': 1.1, 'Height': 0.18, 'Roundness': 0.0, 'Softness': 0.01}),
    ('DOORWAY', 'Doorway', 'LINES', 'SHAPE', {'Width': 0.38, 'Height': 0.9, 'Roundness': 0.15, 'Softness': 0.02}),
    ('LIGHT_RING', 'Light Ring', 'LINES', 'SHAPE', {'Width': 0.8, 'Height': 0.8, 'Hollow': 0.06, 'Softness': 0.03}),
    ('LIGHT_FRAME', 'Light Frame', 'LINES', 'SHAPE', {'Width': 0.85, 'Height': 0.85, 'Roundness': 0.1, 'Hollow': 0.08, 'Softness': 0.05}),
    ('WINDOW_FALLOFF', 'Window Falloff', 'LINES', 'GRADIENT', {'Softness': 0.7}),
    ('HORIZON_FADE', 'Horizon Fade', 'LINES', 'GRADIENT', {'Softness': 0.25, 'Position': 0.1}),
    ('CORNER_WASH', 'Corner Wash', 'LINES', 'GRADIENT', {'Angle': 45.0, 'Softness': 0.6, 'Position': 0.2}),
    ('HALF_SHADE', 'Half Shade', 'LINES', 'GRADIENT', {'Softness': 0.04}),
    ('VIGNETTE', 'Vignette', 'LINES', 'GRADIENT', {'Radial': 1.0, 'Position': 0.6, 'Softness': 0.4}),
    ('TIGHT_SPOT', 'Tight Spot', 'LINES', 'GRADIENT', {'Radial': 1.0, 'Position': 0.35, 'Softness': 0.15}),
]

CATEGORIES = [
    ("ALL", "All", "Every preset"),
    ("FRAMES", "Frames", "Window frames, louvers, rosettes, lancets and broken glass"),
    ("MESHWORK", "Meshwork", "Lattices, grilles, screens and metalwork"),
    ("BOTANICAL", "Botanical", "Leaves, fronds, palms, branches and vines"),
    ("ATMOSPHERE", "Atmosphere", "Silk, drapes, water light and breakup"),
    ("GRAPHIC", "Graphic", "Stripes, dots, rays, rings, spirals and other geometric shapes"),
    ("LINES", "Lines & Shapes", "Thin lines of light, slits, spots, grids and gradients"),
]

PRESET_BY_ID = {p[0]: p for p in PRESETS}

# Original index of each preset, sorted into a stable category-grouped
# order. The browser always shows "Custom Image" first, then the presets
# grouped by category in the order declared above. The sort is stable, so
# presets keep their authored order inside each group.
_GROUP_ORDER = [c[0] for c in CATEGORIES if c[0] != "ALL"]
_GROUPED_ORDER = sorted(range(len(PRESETS)),
                        key=lambda i: (_GROUP_ORDER.index(PRESETS[i][2]), i))


def preset_order():
    """Yield (original_index, preset) in a stable, category-grouped order.

    The original index is kept so enum numbers stay constant; only the
    display order changes.
    """
    for i in _GROUPED_ORDER:
        yield i, PRESETS[i]


# The first entry of the browser: the user's own image instead of a procedural
# pattern. It is not part of PRESETS (it has no pattern values or category).
CUSTOM_ID = "CUSTOM_IMAGE"
CUSTOM_LABEL = "Custom Image"
CUSTOM_DESC = "Use your own black and white image (white lets light through, black blocks it)"


def pattern_of(preset_id):
    """Pattern id behind a preset id (patterns.IMAGE for the custom image)."""
    if preset_id == CUSTOM_ID:
        return patterns.IMAGE
    return PRESET_BY_ID[preset_id][3]


def converted(pid, values):
    """Degrees -> radians for ANGLE inputs."""
    angle_names = {spec[0] for spec in patterns.PATTERN_BY_ID[pid].inputs
                   if len(spec) > 5 and spec[5] == "ANGLE"}
    angle_names |= {"Transform.Rotation", "Rotation"} - {spec[0] for spec in
                                                        patterns.PATTERN_BY_ID[pid].inputs}
    out = {}
    for k, v in values.items():
        out[k] = math.radians(v) if k in angle_names else v
    return out
