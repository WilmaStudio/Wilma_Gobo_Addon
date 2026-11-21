# SPDX-License-Identifier: GPL-3.0-or-later
"""Wilma Gobos panels (View3D > Sidebar > Wilma Gobos)."""

import bpy

from . import patterns, presets, rig

TAB = "Wilma Gobos"

# Icons are Blender built-ins; change them here.
ICON_ADD = "OUTLINER_OB_LIGHT"      # Add Wilma Gobo button and Add > Light entry
ICON_SETTINGS = "TOOL_SETTINGS"     # Wilma Gobo Settings panel


def _shadow(context):
    return rig.light_of(context.active_object)


def _prop(layout, data, name, **kw):
    """Draw a property only if this Blender build has it."""
    if data is not None and hasattr(data, name):
        layout.prop(data, name, **kw)


def draw_inputs(layout, node, skip=("Vector",)):
    """Draw only editable numeric/color controls from the selected pattern node."""
    if node is None:
        return
    col = layout.column(align=True)
    for socket in node.inputs:
        if socket.name in skip or socket.is_linked or not hasattr(socket, "default_value"):
            continue
        if socket.name == "Seed":
            row = col.row(align=True)
            row.prop(socket, "default_value", text="Seed")
            row.operator("wilma_gobo.random_seed", text="", icon="FILE_REFRESH")
        elif socket.type in {"VALUE", "INT"}:
            col.prop(socket, "default_value", text=socket.name)


class WILMA_PT_base:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = TAB


# -- main panel: preset browser -------------------------------------------------------


class WILMA_PT_library(WILMA_PT_base, bpy.types.Panel):
    bl_label = "Wilma Gobos"
    bl_idname = "WILMA_PT_library"

    def draw(self, context):
        st = context.scene.wilma_gobo
        layout = self.layout

        col = layout.column()
        col.prop(st, "category", text="")
        col.template_icon_view(st, "preset", show_labels=True, scale=7.0, scale_popup=5.0)
        preset = presets.PRESET_BY_ID.get(st.preset)
        if preset:
            col.label(text=preset[1], icon=patterns.PATTERN_BY_ID[preset[3]].icon)
        elif st.preset == presets.CUSTOM_ID:
            col.label(text=presets.CUSTOM_LABEL, icon="IMAGE_DATA")

        if st.preset == presets.CUSTOM_ID:
            col = layout.column(align=True)
            col.prop(st, "image_path", text="")
            if not st.image_path:
                col.label(text="Pick an image file (white = light)", icon="INFO")

        layout.separator()
        row = layout.row()
        row.scale_y = 1.35
        row.operator("wilma_gobo.add", text="Add Wilma Gobo", icon=ICON_ADD)

        # Target: edits the active shadow light (a Track To constraint, shown in
        # the Constraints tab), or the default for new lights if none is active.
        col = layout.column(align=True)
        light = _shadow(context)
        if light is None:
            col.prop(st, "target", text="Target", icon="OBJECT_DATA")
        else:
            con = rig.target_constraint(light)
            if con is not None:
                col.prop(con, "target", text="Target", icon="OBJECT_DATA")
            else:
                col.prop(light.wilma_gobo, "target", text="Target", icon="OBJECT_DATA")

        ob = context.active_object
        if (ob is not None and ob.type == "LIGHT" and ob.data.type == "SPOT"
                and rig.plane_of(ob) is None):
            layout.operator("wilma_gobo.attach", text="Add Gobo to Selected Light", icon="LIGHT")


# -- gobo / pattern controls ------------------------------------------------------------


class WILMA_PT_light(WILMA_PT_base, bpy.types.Panel):
    bl_label = "Wilma Gobo Settings"
    bl_idname = "WILMA_PT_light"

    @classmethod
    def poll(cls, context):
        return _shadow(context) is not None

    def draw_header(self, context):
        self.layout.label(text="", icon=ICON_SETTINGS)

    def draw(self, context):
        ob = _shadow(context)
        layout = self.layout
        plane = rig.plane_of(ob)
        layout.label(text=ob.name)

        if plane is None:
            layout.label(text="No Gobo attached", icon="INFO")
            return

        # Simple light / gobo switch. Disabling shadow visibility leaves the
        # light itself and all pattern settings untouched.
        row = layout.row(align=True)
        row.prop(plane, "visible_shadow", text="Gobo", toggle=True,
                 icon="SHADING_RENDERED" if plane.visible_shadow else "LIGHT")

        mat = rig.material_of(ob)
        if mat and mat.users > 1:
            box = layout.box()
            box.label(text="Pattern shared with other lights", icon="LINKED")
            box.operator("wilma_gobo.make_unique", text="Make Unique")

        pid = rig.current_pattern(ob)
        if pid == patterns.IMAGE:
            img = rig.node(ob, rig.N_IMAGE)
            layout.template_ID(img, "image", new="image.new", open="image.open")
            if img.image is not None and img.image.source == "FILE":
                layout.prop(img.image, "filepath", text="")
            layout.label(text="White lets light through, black blocks it", icon="INFO")
        else:
            draw_inputs(layout, rig.node(ob, rig.N_PATTERN))

        # More Settings: collapsible, right under the pattern's own controls
        header, body = layout.panel("wilma_more_settings", default_closed=True)
        header.label(text="More Settings")
        if body is not None:
            body.use_property_split = True
            body.use_property_decorate = False
            col = body.column()
            col.prop(ob.wilma_gobo, "pattern_scale", text="Scale")
            col.prop(ob.wilma_gobo, "flip", text="Flip")
            col.prop(ob.wilma_gobo, "invert", text="Invert")

        row = layout.row(align=True)
        row.operator("wilma_gobo.reset", text="Reset Values", icon="LOOP_BACK")
        row.operator("wilma_gobo.remove", text="Remove Gobo", icon="X")


# -- light settings (the same controls as the Light data tab) --------------------------


class WILMA_PT_lamp(WILMA_PT_base, bpy.types.Panel):
    bl_label = "Light"
    bl_idname = "WILMA_PT_lamp"

    @classmethod
    def poll(cls, context):
        return _shadow(context) is not None

    def draw_header(self, context):
        self.layout.label(text="", icon="OUTLINER_DATA_LIGHT")

    def draw(self, context):
        lamp = _shadow(context).data
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        if lamp.type != "SPOT":
            box = layout.box()
            box.label(text="Wilma Gobos works with Spot lights", icon="ERROR")
            box.prop(lamp, "type", text="Type")

        col = layout.column()
        if hasattr(lamp, "use_temperature"):
            if lamp.use_temperature:
                col.prop(lamp, "temperature", text="Temperature")
            else:
                col.prop(lamp, "color", text="Color")
            col.prop(lamp, "use_temperature", text="Use Temperature")
        else:
            col.prop(lamp, "color", text="Color")
        col.separator()
        col.prop(lamp, "energy", text="Power")
        _prop(col, lamp, "exposure", text="Exposure")
        col.separator()
        col.prop(lamp, "shadow_soft_size", text="Radius")
        _prop(col, lamp, "use_soft_falloff", text="Soft Falloff")
        col.separator()
        _prop(col, lamp, "normalize", text="Normalize")
        row = col.row(align=True)
        _prop(row, lamp, "use_custom_distance", text="Custom Distance")
        if getattr(lamp, "use_custom_distance", False):
            _prop(col, lamp, "cutoff_distance", text="Distance")


class WILMA_PT_lamp_beam(WILMA_PT_base, bpy.types.Panel):
    bl_label = "Beam Shape"
    bl_idname = "WILMA_PT_lamp_beam"
    bl_parent_id = "WILMA_PT_lamp"

    @classmethod
    def poll(cls, context):
        ob = _shadow(context)
        return ob is not None and ob.data.type == "SPOT"

    def draw(self, context):
        lamp = _shadow(context).data
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        col = layout.column()
        col.prop(lamp, "spot_size", text="Spot Size")
        col.prop(lamp, "spot_blend", text="Blend", slider=True)
        col.prop(lamp, "show_cone", text="Show Cone")


class WILMA_PT_website(WILMA_PT_base, bpy.types.Panel):
    bl_label = "Wilma Studio"
    bl_idname = "WILMA_PT_website"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        row = self.layout.row()
        op = row.operator("wm.url_open", text="wilmastudio.co", icon="URL")
        op.url = "https://wilmastudio.co"


CLASSES = (WILMA_PT_library, WILMA_PT_light, WILMA_PT_lamp, WILMA_PT_lamp_beam,
           WILMA_PT_website)


def draw_add_menu(self, context):
    self.layout.operator("wilma_gobo.add", text="Wilma Gobo", icon=ICON_ADD)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_light_add.append(draw_add_menu)


def unregister():
    bpy.types.VIEW3D_MT_light_add.remove(draw_add_menu)
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
