# SPDX-License-Identifier: GPL-3.0-or-later
import random

import bpy

from . import presets, rig

PRESET_ENUM = [(presets.CUSTOM_ID, presets.CUSTOM_LABEL, "")]
PRESET_ENUM += [(p[0], p[1], "") for p in presets.PRESETS]


def _shadow(context):
    return rig.light_of(context.active_object)


def _subject(context):
    """The object a quick setup should be built around: the active object if
    it is selected, otherwise the first selected object."""
    obs = context.selected_objects
    if not obs:
        return None
    act = context.active_object
    return act if act in obs else obs[0]


class WG_OT_add(bpy.types.Operator):
    bl_idname = "wilma_gobo.add"
    bl_label = "Add Wilma Gobos"
    bl_description = ("Add a spot light that casts the chosen pattern, aimed at the "
                      "Target object, which it then follows (or the 3D cursor if there is none)")
    bl_options = {"REGISTER", "UNDO"}

    preset: bpy.props.EnumProperty(name="Preset", items=PRESET_ENUM)

    def invoke(self, context, event):
        st = context.scene.wilma_gobo
        if st.preset:
            self.preset = st.preset
        return self.execute(context)

    def execute(self, context):
        if context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        st = context.scene.wilma_gobo
        target, reach = st.target, 1.0
        if target is not None:
            reach = max(target.dimensions) / 2.0
        ob = rig.create(context, presets.pattern_of(self.preset), target, reach)
        rig.apply_preset(ob, self.preset, st.image_path)
        self._check_image(context, ob)
        for o in context.selected_objects:
            o.select_set(False)
        ob.select_set(True)
        context.view_layer.objects.active = ob
        return {"FINISHED"}

    def _check_image(self, context, ob):
        if self.preset != presets.CUSTOM_ID:
            return
        path = context.scene.wilma_gobo.image_path
        if path and rig.node(ob, rig.N_IMAGE).image is None:
            self.report({"WARNING"}, f"Could not load image: {path}")


class WG_OT_three_point(bpy.types.Operator):
    bl_idname = "wilma_gobo.three_point"
    bl_label = "Add 3-Point Lights"
    bl_description = ("Quick three-point lighting around the selected object: Key, Fill "
                      "and Rim area lights that track it. Needs a selected object")
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)

    def execute(self, context):
        if context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        subject = _subject(context)
        if subject is None:
            self.report({"WARNING"}, "Select an object to light first")
            return {"CANCELLED"}
        dims = max(subject.dimensions) if len(subject.dimensions) else 0.0
        radius = max(dims * 0.5, 0.25)
        center = subject.matrix_world.translation.copy()
        coll = rig.wilma_collection(context)
        created = []
        for name, loc, energy, exposure, size in rig.three_point_layout(center, radius):
            lamp = bpy.data.lights.new(name, "AREA")
            lamp.energy = energy
            lamp.exposure = exposure
            lamp.size = size
            ob = bpy.data.objects.new(name, lamp)
            coll.objects.link(ob)
            ob.location = loc
            rig.set_target(ob, subject)
            created.append(ob)
        for o in context.selected_objects:
            o.select_set(False)
        for ob in created:
            ob.select_set(True)
        context.view_layer.objects.active = created[0]
        return {"FINISHED"}


class WG_OT_attach(bpy.types.Operator):
    bl_idname = "wilma_gobo.attach"
    bl_label = "Add Gobo to Spot Light"
    bl_description = "Give the selected spot lights a gobo pattern"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return any(o.type == "LIGHT" and o.data.type == "SPOT"
                   for o in context.selected_objects)

    def execute(self, context):
        preset = context.scene.wilma_gobo.preset or presets.PRESETS[0][0]
        for ob in context.selected_objects:
            if ob.type == "LIGHT" and ob.data.type == "SPOT" and rig.plane_of(ob) is None:
                rig.attach(ob)
                rig.apply_preset(ob, preset, context.scene.wilma_gobo.image_path)
                if context.scene.wilma_gobo.target is not None:
                    rig.set_target(ob, context.scene.wilma_gobo.target)
        return {"FINISHED"}


class WG_OT_apply_preset(bpy.types.Operator):
    bl_idname = "wilma_gobo.apply_preset"
    bl_label = "Apply Preset"
    bl_description = "Set the active shadow light's pattern and settings to a preset"
    bl_options = {"REGISTER", "UNDO"}

    preset: bpy.props.EnumProperty(name="Preset", items=PRESET_ENUM)

    @classmethod
    def poll(cls, context):
        return _shadow(context) is not None

    def execute(self, context):
        rig.apply_preset(_shadow(context), self.preset,
                         context.scene.wilma_gobo.image_path)
        return {"FINISHED"}


class WG_OT_remove(bpy.types.Operator):
    bl_idname = "wilma_gobo.remove"
    bl_label = "Remove Pattern"
    bl_description = "Delete the shadow pattern and keep the lamp"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _shadow(context) is not None

    def execute(self, context):
        ob = _shadow(context)
        rig.detach(ob)
        context.view_layer.objects.active = ob
        ob.select_set(True)
        return {"FINISHED"}


class WG_OT_random_seed(bpy.types.Operator):
    bl_idname = "wilma_gobo.random_seed"
    bl_label = "Random Seed"
    bl_description = "Pick a new random variation of the pattern"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        n = rig.node(_shadow(context), rig.N_PATTERN)
        return n is not None and not n.mute and "Seed" in n.inputs

    def execute(self, context):
        n = rig.node(_shadow(context), rig.N_PATTERN)
        n.inputs["Seed"].default_value = float(random.randint(0, 999))
        return {"FINISHED"}


class WG_OT_reset(bpy.types.Operator):
    bl_idname = "wilma_gobo.reset"
    bl_label = "Reset Pattern"
    bl_description = "Set the pattern, placement and look back to their defaults"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _shadow(context) is not None

    def execute(self, context):
        ob = _shadow(context)
        rig.set_pattern(ob, rig.current_pattern(ob))
        rig.reset_look(ob)
        return {"FINISHED"}


class WG_OT_make_unique(bpy.types.Operator):
    bl_idname = "wilma_gobo.make_unique"
    bl_label = "Make Unique"
    bl_description = ("This pattern is shared with other lights (e.g. after duplicating). "
                      "Give this light its own copy")
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return _shadow(context) is not None

    def execute(self, context):
        rig.make_unique(_shadow(context))
        return {"FINISHED"}


class WG_OT_select_light(bpy.types.Operator):
    bl_idname = "wilma_gobo.select_light"
    bl_label = "Select Light"
    bl_description = "Select a shadow light"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty()

    def execute(self, context):
        ob = context.scene.objects.get(self.name)
        if ob is None or context.view_layer.objects.get(ob.name) is None:
            return {"CANCELLED"}
        for o in context.selected_objects:
            o.select_set(False)
        ob.select_set(True)
        context.view_layer.objects.active = ob
        return {"FINISHED"}


CLASSES = (WG_OT_add, WG_OT_three_point, WG_OT_attach, WG_OT_apply_preset,
           WG_OT_remove, WG_OT_random_seed, WG_OT_reset, WG_OT_make_unique,
           WG_OT_select_light)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
