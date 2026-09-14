import bpy
import math
import os
import sys
from mathutils import Vector

# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

FPS = 24
START_FRAME = 1
END_FRAME = 120

WIDTH = 1280
HEIGHT = 720

OUTPUT = "/home/runner/work/rendered_video.mp4"

# ---------------------------------------------------------
# CLEAN SCENE
# ---------------------------------------------------------

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

for datablocks in (
    bpy.data.meshes,
    bpy.data.curves,
    bpy.data.materials,
    bpy.data.cameras,
    bpy.data.lights,
):
    pass


# ---------------------------------------------------------
# MATERIAL
# ---------------------------------------------------------

def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    return mat


GROUND = material("Ground", (0.12, 0.16, 0.12))
TREE_GREEN = material("TreeGreen", (0.12, 0.42, 0.16))
TREE_DARK = material("TreeDark", (0.07, 0.25, 0.10))
TRUNK = material("Trunk", (0.30, 0.16, 0.07))
HOUSE = material("House", (0.55, 0.32, 0.18))
ROOF = material("Roof", (0.25, 0.08, 0.06))
CHARACTER = material("Character", (0.15, 0.35, 0.65))
WHITE = material("White", (0.9, 0.9, 0.85))


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def cube(name, location, scale, mat):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    if mat:
        obj.data.materials.append(mat)

    return obj


def sphere(name, location, radius, mat):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2,
        radius=radius,
        location=location,
    )

    obj = bpy.context.object
    obj.name = name

    if mat:
        obj.data.materials.append(mat)

    return obj


def cylinder(name, location, radius, depth, mat):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=radius,
        depth=depth,
        location=location,
    )

    obj = bpy.context.object
    obj.name = name

    if mat:
        obj.data.materials.append(mat)

    return obj


# ---------------------------------------------------------
# GROUND
# ---------------------------------------------------------

ground = cube(
    "Ground",
    (0, 0, -0.5),
    (18, 18, 0.5),
    GROUND,
)


# ---------------------------------------------------------
# HOUSE
# ---------------------------------------------------------

house = cube(
    "House",
    (5, 1, 1.5),
    (2.5, 2.0, 2.0),
    HOUSE,
)

# Roof
bpy.ops.mesh.primitive_cone_add(
    vertices=4,
    radius1=3.2,
    radius2=0,
    depth=2.4,
    location=(5, 1, 5.7),
    rotation=(0, 0, math.radians(45)),
)

roof = bpy.context.object
roof.name = "Roof"
roof.data.materials.append(ROOF)


# Door
cube(
    "Door",
    (5, -1.05, 1.2),
    (0.55, 0.08, 1.2),
    TRUNK,
)


# ---------------------------------------------------------
# TREES
# ---------------------------------------------------------

def tree(x, y, size=1.0):

    cylinder(
        "TreeTrunk",
        (x, y, 1.2 * size),
        0.35 * size,
        2.4 * size,
        TRUNK,
    )

    sphere(
        "TreeLeaves",
        (x, y, 3.0 * size),
        1.5 * size,
        TREE_GREEN,
    )

    sphere(
        "TreeLeavesDark",
        (x + 0.5 * size, y, 3.7 * size),
        1.1 * size,
        TREE_DARK,
    )


tree(-5, 3, 1.3)
tree(-8, -2, 1.0)
tree(0, 6, 1.2)
tree(9, 5, 1.4)
tree(10, -4, 1.1)


# ---------------------------------------------------------
# LOW-POLY CHARACTER
# ---------------------------------------------------------

# Body
cube(
    "CharacterBody",
    (0, 0, 1.5),
    (0.65, 0.45, 1.0),
    CHARACTER,
)

# Head
sphere(
    "CharacterHead",
    (0, 0, 3.0),
    0.75,
    WHITE,
)

# Eyes
sphere(
    "EyeLeft",
    (-0.25, -0.68, 3.15),
    0.08,
    ROOF,
)

sphere(
    "EyeRight",
    (0.25, -0.68, 3.15),
    0.08,
    ROOF,
)


# ---------------------------------------------------------
# CHARACTER ANIMATION
# ---------------------------------------------------------

body = bpy.data.objects.get("CharacterBody")
head = bpy.data.objects.get("CharacterHead")

if body:
    body.location.x = -3

    body.keyframe_insert(
        data_path="location",
        frame=1,
    )

    body.location.x = 3

    body.keyframe_insert(
        data_path="location",
        frame=END_FRAME,
    )

if head:
    head.location.x = -3

    head.keyframe_insert(
        data_path="location",
        frame=1,
    )

    head.location.x = 3

    head.keyframe_insert(
        data_path="location",
        frame=END_FRAME,
    )


# ---------------------------------------------------------
# CAMERA
# ---------------------------------------------------------

bpy.ops.object.camera_add(
    location=(15, -22, 13),
)

camera = bpy.context.object
camera.name = "MainCamera"

bpy.context.scene.camera = camera


def point_camera(cam, target):

    direction = Vector(target) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


point_camera(camera, (0, 1, 2))


# Camera movement
camera.location = (15, -22, 13)

camera.keyframe_insert(
    data_path="location",
    frame=1,
)

camera.location = (11, -17, 10)

camera.keyframe_insert(
    data_path="location",
    frame=END_FRAME,
)


# ---------------------------------------------------------
# LIGHTING
# ---------------------------------------------------------

bpy.ops.object.light_add(
    type="SUN",
    location=(4, -5, 12),
)

sun = bpy.context.object
sun.name = "Sun"
sun.data.energy = 3.0

sun.rotation_euler = (
    math.radians(25),
    math.radians(-20),
    math.radians(-25),
)


bpy.ops.object.light_add(
    type="AREA",
    location=(0, -8, 8),
)

area = bpy.context.object
area.data.energy = 700
area.data.shape = "DISK"
area.data.size = 8

point_camera(area, (0, 0, 2))


# ---------------------------------------------------------
# WORLD
# ---------------------------------------------------------

world = bpy.context.scene.world

if world:
    world.color = (0.05, 0.08, 0.12)


# ---------------------------------------------------------
# RENDER SETTINGS
# ---------------------------------------------------------

scene = bpy.context.scene

scene.render.engine = "BLENDER_EEVEE_NEXT"

scene.render.resolution_x = WIDTH
scene.render.resolution_y = HEIGHT
scene.render.resolution_percentage = 100

scene.render.fps = FPS

scene.frame_start = START_FRAME
scene.frame_end = END_FRAME

scene.render.image_settings.file_format = "FFMPEG"

scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "MEDIUM"

scene.render.filepath = OUTPUT

# Color management
scene.view_settings.look = "AgX - Medium High Contrast"


# ---------------------------------------------------------
# PERFORMANCE
# ---------------------------------------------------------

scene.render.use_file_extension = True

# Avoid unnecessary updates
scene.render.image_settings.color_mode = "RGB"

# ---------------------------------------------------------
# RENDER
# ---------------------------------------------------------

print("=" * 60)
print("STARTING LOW-POLY VIDEO RENDER")
print(f"Frames: {START_FRAME} -> {END_FRAME}")
print(f"Resolution: {WIDTH}x{HEIGHT}")
print(f"FPS: {FPS}")
print(f"Output: {OUTPUT}")
print("=" * 60)

bpy.ops.wm.save_as_mainfile(
    filepath="/home/runner/work/low_poly_scene.blend"
)

bpy.ops.render.render(
    animation=True,
)

print("=" * 60)
print("RENDER COMPLETE")
print(f"Output: {OUTPUT}")
print("=" * 60)
