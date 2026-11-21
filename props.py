# SPDX-License-Identifier: GPL-3.0-or-later
"""Settings. Per-light settings are views onto the rig (custom properties and
material nodes), so nothing here has to be kept in sync."""

import bpy

from . import patterns, presets, rig, thumbs

PATTERN_ITEMS = [(p.id, p.label, p.description, p.icon, i)
                 for i, p in enumerate(patterns.PATTERNS)]
PATTERN_ITEMS.append((patterns.IMAGE, "Image", "Use your own black and white image",
                      "IMAGE_DATA", len(PATTERN_ITEMS)))
PATTERN_IDS = [it[0] for it in PATTERN_ITEMS]

_preset_items = []  # Blender needs references to dynamic enum items kept alive


def preset_items(self, context):
    cat = self.category if self else "ALL"
    _preset_items.clear()
    # "Custom Image" is always the first thing in the browser, in every category
    _preset_items.append((presets.CUSTOM_ID, presets.CUSTOM_LABEL, presets.CUSTOM_DESC,
                          thumbs.icon(presets.CUSTOM_ID), len(presets.PRESETS)))
    for i, (pid, label, pcat, pattern, _) in presets.preset_order():
        if cat != "ALL" and pcat != cat:
            continue
        desc = patterns.PATTERN_BY_ID[pattern].description
        _preset_items.append((pid, label, desc, thumbs.icon(pid), i))
    return _preset_items


def _active_shadow(context):
    return rig.light_of(context.active_object) if context else None


def _preset_changed(self, context):
    if _active_shadow(context) is not None:
        bpy.ops.wilma_gobo.apply_preset(preset=self.preset)


def _category_changed(self, context):
    items = preset_items(self, context)
    ids = {it[0] for it in items}
    if items and self.get("preset") not in ids:
        # current preset is not in the new category: fall back to the first
        # real preset (items[0] is the custom image). Dict assignment skips
        # the update callback so browsing does not apply the preset.
        self["preset"] = (items[1] if len(items) > 1 else items[0])[0]


def _image_path_changed(self, context):
    """Typing or browsing a path reloads the image of the active light when it
    is using the custom image."""
    ob = _active_shadow(context)
    if ob is not None and rig.current_pattern(ob) == patterns.IMAGE:
        rig.set_image(ob, self.image_path)


def _target_poll(self, ob):
    return not ob.get(rig.PLANE_TAG)  # not the hidden gobo planes


_clearing = False


def _light_target_changed(self, context):
    """Picking a target on a light that has none yet adds the Track To
    constraint at once. From then on the field shows the constraint's own
    target, so this pointer only ever carries the pick."""
    global _clearing
    ob = rig.light_of(self.id_data)
    if _clearing or ob is None or self.target is None:
        return
    rig.set_target(ob, self.target)
    _clearing = True
    try:
        self.target = None
    finally:
        _clearing = False


def _get_haze(self):
    return rig.haze_node(self.id_data.world) is not None


def _set_haze(self, value):
    rig.set_haze(self.id_data, value)


def _get_haze_density(self):
    n = rig.haze_node(self.id_data.world)
    return n.inputs["Density"].default_value if n else 0.03


def _set_haze_density(self, value):
    n = rig.haze_node(self.id_data.world)
    if n:
        n.inputs["Density"].default_value = value


class WG_SceneSettings(bpy.types.PropertyGroup):
    category: bpy.props.EnumProperty(
        name="Category", items=presets.CATEGORIES, update=_category_changed)
    preset: bpy.props.EnumProperty(
        name="Preset", items=preset_items, update=_preset_changed,
        description="Shadow pattern. Picking one changes the active shadow light")
    image_path: bpy.props.StringProperty(
        name="Image", subtype="FILE_PATH", update=_image_path_changed,
        description="Path of your own image. White lets light through, black blocks it")
    target: bpy.props.PointerProperty(
        name="Target", type=bpy.types.Object, poll=_target_poll,
        description="Object new Wilma Gobos lights follow with a Track To constraint "
                    "(they are aimed at the 3D cursor if empty)")
    haze: bpy.props.BoolProperty(
        name="Haze", get=_get_haze, set=_set_haze,
        description="Fill the world with a thin volume so the light draws visible beams "
                    "(slower to render)")
    haze_density: bpy.props.FloatProperty(
        name="Density", min=0.0, soft_max=0.5, precision=3, step=0.1,
        get=_get_haze_density, set=_set_haze_density)


def _light(self):
    return rig.light_of(self.id_data)


def _get_pattern(self):
    pid = rig.current_pattern(_light(self))
    return PATTERN_IDS.index(pid) if pid in PATTERN_IDS else 0


def _set_pattern(self, value):
    ob = _light(self)
    if ob is not None:
        rig.set_pattern(ob, PATTERN_IDS[value])


def _custom_getter(key, default):
    def get(self):
        ob = _light(self)
        return float(ob.get(key, default)) if ob else default

    def set(self, value):
        ob = _light(self)
        if ob is not None:
            ob[key] = value
            ob.update_tag()  # re-evaluate the plane drivers

    return get, set


def _look_getter(node_name, socket, default, boolean=False):
    """Property view onto an input of the Transform / Finish node of the active
    light's material. Toggles are stored as 0/1 floats in the node."""
    def get(self):
        n = rig.node(_light(self), node_name)
        if n is None:
            return default
        v = n.inputs[socket].default_value
        return v > 0.5 if boolean else float(v)

    def set(self, value):
        n = rig.node(_light(self), node_name)
        if n is not None:
            n.inputs[socket].default_value = (1.0 if value else 0.0) if boolean else value

    return get, set


_get_dist, _set_dist = _custom_getter(rig.DISTANCE, 1.0)
_get_size, _set_size = _custom_getter(rig.SIZE, 2.0)
_get_pscale, _set_pscale = _look_getter(rig.N_TRANSFORM, "Scale", 1.0)
_get_flip, _set_flip = _look_getter(rig.N_TRANSFORM, "Flip", False, boolean=True)
_get_invert, _set_invert = _look_getter(rig.N_FINISH, "Invert", False, boolean=True)


class WG_ObjectSettings(bpy.types.PropertyGroup):
    target: bpy.props.PointerProperty(
        name="Target", type=bpy.types.Object, poll=_target_poll, update=_light_target_changed,
        description="Object this light follows, using a Track To constraint")
    pattern_scale: bpy.props.FloatProperty(
        name="Scale", min=0.01, soft_max=10.0, precision=3, step=10,
        get=_get_pscale, set=_set_pscale,
        description="Scale the whole pattern. Above 1 enlarges it, below 1 shrinks it")
    flip: bpy.props.BoolProperty(
        name="Flip", get=_get_flip, set=_set_flip,
        description="Mirror the pattern left to right")
    invert: bpy.props.BoolProperty(
        name="Invert", get=_get_invert, set=_set_invert,
        description="Swap light and shadow: what was open becomes blocked and the other way round")
    pattern: bpy.props.EnumProperty(
        name="Pattern", items=PATTERN_ITEMS, get=_get_pattern, set=_set_pattern,
        description="Procedural pattern (resets its settings)")
    distance: bpy.props.FloatProperty(
        name="Focus Distance", subtype="DISTANCE", min=0.001, soft_max=10.0,
        get=_get_dist, set=_set_dist,
        description="Distance from the lamp to the pattern. Further away gives sharper "
                    "shadows (and, for Sun and Area lamps, moves the pattern)")
    size: bpy.props.FloatProperty(
        name="Pattern Size", subtype="DISTANCE", min=0.001, soft_max=50.0,
        get=_get_size, set=_set_size,
        description="Width of the pattern plane (Sun, Area and Point lamps; Spot "
                    "lamps fit the cone automatically)")


def register():
    bpy.utils.register_class(WG_SceneSettings)
    bpy.utils.register_class(WG_ObjectSettings)
    bpy.types.Scene.wilma_gobo = bpy.props.PointerProperty(type=WG_SceneSettings)
    bpy.types.Object.wilma_gobo = bpy.props.PointerProperty(type=WG_ObjectSettings)


def unregister():
    del bpy.types.Object.wilma_gobo
    del bpy.types.Scene.wilma_gobo
    bpy.utils.unregister_class(WG_ObjectSettings)
    bpy.utils.unregister_class(WG_SceneSettings)
