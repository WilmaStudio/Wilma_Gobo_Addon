WILMA GOBOS
Wilma Studio | https://wilmastudio.co
Version 1.4.2 | Blender 5.2+

Procedural gobo (shadow-pattern) spot lights. Everything is built from shader
nodes, so there are no image files to manage and every pattern can be tuned.

WHAT'S NEW IN 1.4.2
- The preset browser is tidy again: presets are grouped by category, so
  every folder (Frames, Meshwork, Botanical, Atmosphere, Graphic, Lines &
  Shapes) stays together in the list instead of being mixed up. "Custom
  Image" still leads the list in every category.

WHAT'S NEW IN 1.4.1
- Three-point lighting rebalanced: all three lamps use a fixed, low power of
  10 W and the intensity is balanced through exposure instead — Key +5,
  Fill +3, Rim +2 stops. The rig no longer blows out the subject, no matter
  its size.
- The exposure (and power) stay editable per lamp in the Light panel, so you
  can push each light up or down as needed.

WHAT'S NEW IN 1.4.0
- New "Add 3-Point Lights" button under "Add Wilma Gobos". Select an object,
  press it and you get a quick three-point setup: three area lights named
  Key, Fill and Rim, sized and powered to the object and each following it
  with a Track To constraint.
- Lights created by the add-on are named W_Gobo_01, W_Gobo_02, ... and their
  hidden pattern planes W_Pattern_01, W_Pattern_02, ...
- All add-on lights live in one shared "Wilma Gobos" collection, created and
  linked to the scene automatically.

WHAT'S NEW IN 1.3.2
- The preset browser now shows the patterns in a varied, organic layout
  instead of a strict grouped run. "Custom Image" still always leads.
- Switching category keeps your current preset when it exists in the new
  category (it used to reset every time).
- Internal clean-ups and a wider static test pass; no user-facing workflow
  changes.

WHAT'S NEW IN 1.3.1
- New collapsible "More Settings" section under every pattern's settings in
  "Wilma Gobos Settings": Scale (size of the whole pattern), Flip (mirror) and
  Invert (swap light and shadow). It works for the Custom Image too.

WHAT'S NEW IN 1.3.0
- Target now follows live. Pick an object in the Target field and the light
  tracks it right away through a Track To constraint named "Wilma Target"
  (visible in the Object Constraints tab). With a Wilma Gobos light active the
  field edits that light; with none active it sets the target for the next
  lights you add. The "Aim Light at Target" button is gone.
- 6 new procedural patterns and 38 new presets:
  Light Slit (thin lines: width, length, count, spacing, angle, taper, fade,
  bend, wave), Soft Shape (circle, oval, slot, ring, frame), Light Gradient
  (linear or radial falloff), Line Grid, Crackle Lines and Dappled Light.
- New category "Lines & Shapes". Dappled presets are in Botanical, crackle
  presets in Meshwork.

WHAT'S NEW IN 1.2.0
- New "Custom Image" entry, always the first item of the preset browser. Pick
  it, choose an image file (white lets light through, black blocks it) and
  press "Add Wilma Gobos". Changing the path later updates the active light.
- New "Target" field under the Add button (see 1.3.0 for how it works now).
- New icons for the Add Wilma Gobos button and the settings panel.
- The panel under the Add button is now called "Wilma Gobos Settings".
- Removed the Tall Cacti and Dangling Vines presets.
- Removed the Influence and Shadow sub-panels from the Light panel.

WHAT'S NEW IN 1.1.0
- Sidebar tab and main panel are named "Wilma Gobos".
- Spot lights only. Point and Area lights were removed from the add workflow.
- New lights are named W_Gobo_01, W_Gobo_02, ... in the Outliner. The hidden
  pattern plane sits under it as W_Pattern_01, W_Pattern_02, ...
- New collapsible "Light" panel with the same controls as the Light data tab
  (color/temperature, power, exposure, radius, soft falloff, custom distance)
  plus a Beam Shape sub-panel (spot size, blend, show cone).
- Track To removed.
- Every pattern and preset has a new name, and the node groups are now named
  "Wilma ...".
- 10 new procedural patterns and 32 new presets in a new "Graphic" category:
  Wave Stripes, Halftone Dots, Sunburst Rays, Concentric Rings, Spiral Arms,
  Basket Weave, Brick Openwork, Rain Drops, Star Scatter, Cloud Streaks.
- Categories: Frames, Meshwork, Botanical, Atmosphere, Graphic.

USAGE
1. Open the 3D Viewport sidebar (N) > Wilma Gobos.
2. Pick a category and a preset (or "Custom Image" and your own file), then
   press "Add Wilma Gobos". Optionally set a Target object first.
3. Tune the pattern in "Wilma Gobos Settings" and the light itself in "Light".
4. The "Gobo" toggle turns the pattern on/off without deleting anything.
5. Select an object and press "Add 3-Point Lights" for a quick Key / Fill /
   Rim area-light setup around it.

INSTALL
Blender 5.2: Preferences > Get Extensions > drop-down menu > Install from
Disk, choose this ZIP, enable Wilma Gobos.

CREDITS AND LICENSE
This build is derived from the Open Shadow 0.1.0 source package. The original
project license is retained in LICENSE and this build continues under
GPL-3.0-or-later.
