import bpy
import math
import sys
import os
from mathutils import Vector


# =========================================================
# SETTINGS
# =========================================================

FPS = 24

DEFAULT_START_FRAME = 1
DEFAULT_END_FRAME = 120

WIDTH = 1280
HEIGHT = 720

OUTPUT = "/home/runner/work/rendered_video.mp4"


# =========================================================
# COMMAND LINE ARGUMENTS
# =========================================================

def read_arguments():

    args = sys.argv

    if "--" not in args:
        return

    args = args[args.index("--") + 1:]

    global OUTPUT

    i = 0

    while i < len(args):

        if args[i] == "--output" and i + 1 < len(args):
            OUTPUT = args[i + 1]
            i += 2
            continue

        i += 1


read_arguments()


# =========================================================
# CLEAN SCENE
# =========================================================

print("Cleaning Blender scene...")

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)


# =========================================================
# MATERIAL CREATION
# =========================================================

def create_material(name, color):

    mat = bpy.data.materials.get(name)

    if mat is None:
        mat = bpy.data.materials.new(name)

    mat.diffuse_color = (
        color[0],
        color[1],
        color[2],
        1.0
    )

    return mat


GROUND = create_material(
    "Ground",
    (0.12, 0.16, 0.12)
)

TREE_GREEN = create_material(
    "TreeGreen",
    (0.12, 0.42, 0.16)
)

TREE_DARK = create_material(
    "TreeDark",
    (0.07, 0.25, 0.10)
)

TRUNK = create_material(
    "Trunk",
    (0.30, 0.16, 0.07)
)

HOUSE = create_material(
    "House",
    (0.55, 0.32, 0.18)
)

ROOF = create_material(
    "Roof",
    (0.25, 0.08, 0.06)
)

CHARACTER = create_material(
    "Character",
    (0.15, 0.35, 0.65)
)

WHITE = create_material(
    "White",
    (0.9, 0.9, 0.85)
)


# =========================================================
# OBJECT HELPERS
# =========================================================

def create_cube(name, location, scale, mat):

    bpy.ops.mesh.primitive_cube_add(
        location=location
    )

    obj = bpy.context.object

    obj.name = name

    obj.scale = scale

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )

    if mat:
        obj.data.materials.append(mat)

    return obj


def create_ico_sphere(
    name,
    location,
    radius,
    mat
):

    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2,
        radius=radius,
        location=location
    )

    obj = bpy.context.object

    obj.name = name

    if mat:
        obj.data.materials.append(mat)

    return obj


def create_cylinder(
    name,
    location,
    radius,
    depth,
    mat
):

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8,
        radius=radius,
        depth=depth,
        location=location
    )

    obj = bpy.context.object

    obj.name = name

    if mat:
        obj.data.materials.append(mat)

    return obj


# =========================================================
# GROUND
# =========================================================

create_cube(
    "Ground",
    (0, 0, -0.5),
    (18, 18, 0.5),
    GROUND
)


# =========================================================
# HOUSE
# =========================================================

create_cube(
    "House",
    (5, 1, 1.5),
    (2.5, 2.0, 2.0),
    HOUSE
)


# =========================================================
# HOUSE ROOF
# =========================================================

bpy.ops.mesh.primitive_cone_add(
    vertices=4,
    radius1=3.2,
    radius2=0,
    depth=2.4,
    location=(5, 1, 5.7),
    rotation=(0, 0, math.radians(45))
)

roof = bpy.context.object

roof.name = "Roof"

roof.data.materials.append(ROOF)


# =========================================================
# DOOR
# =========================================================

create_cube(
    "Door",
    (5, -1.05, 1.2),
    (0.55, 0.08, 1.2),
    TRUNK
)


# =========================================================
# TREE
# =========================================================

def create_tree(x, y, size=1.0):

    create_cylinder(
        "TreeTrunk",
        (x, y, 1.2 * size),
        0.35 * size,
        2.4 * size,
        TRUNK
    )

    create_ico_sphere(
        "TreeLeaves",
        (x, y, 3.0 * size),
        1.5 * size,
        TREE_GREEN
    )

    create_ico_sphere(
        "TreeLeavesDark",
        (
            x + 0.5 * size,
            y,
            3.7 * size
        ),
        1.1 * size,
        TREE_DARK
    )


create_tree(-5, 3, 1.3)
create_tree(-8, -2, 1.0)
create_tree(0, 6, 1.2)
create_tree(9, 5, 1.4)
create_tree(10, -4, 1.1)


# =========================================================
# LOW-POLY CHARACTER
# =========================================================

body = create_cube(
    "CharacterBody",
    (-3, 0, 1.5),
    (0.65, 0.45, 1.0),
    CHARACTER
)

head = create_ico_sphere(
    "CharacterHead",
    (-3, 0, 3.0),
    0.75,
    WHITE
)


# =========================================================
# CHARACTER EYES
# =========================================================

eye_left = create_ico_sphere(
    "EyeLeft",
    (-3.25, -0.68, 3.15),
    0.08,
    ROOF
)

eye_right = create_ico_sphere(
    "EyeRight",
    (-2.75, -0.68, 3.15),
    0.08,
    ROOF
)


# =========================================================
# CHARACTER ANIMATION
# =========================================================

body.location.x = -3

body.keyframe_insert(
    data_path="location",
    frame=DEFAULT_START_FRAME
)

body.location.x = 3

body.keyframe_insert(
    data_path="location",
    frame=DEFAULT_END_FRAME
)


head.location.x = -3

head.keyframe_insert(
    data_path="location",
    frame=DEFAULT_START_FRAME
)

head.location.x = 3

head.keyframe_insert(
    data_path="location",
    frame=DEFAULT_END_FRAME
)


eye_left.location.x = -3.25

eye_left.keyframe_insert(
    data_path="location",
    frame=DEFAULT_START_FRAME
)

eye_left.location.x = 2.75

eye_left.keyframe_insert(
    data_path="location",
    frame=DEFAULT_END_FRAME
)


eye_right.location.x = -2.75

eye_right.keyframe_insert(
    data_path="location",
    frame=DEFAULT_START_FRAME
)

eye_right.location.x = 3.25

eye_right.keyframe_insert(
    data_path="location",
    frame=DEFAULT_END_FRAME
)


# =========================================================
# CAMERA
# =========================================================

bpy.ops.object.camera_add(
    location=(15, -22, 13)
)

camera = bpy.context.object

camera.name = "MainCamera"

bpy.context.scene.camera = camera


def point_camera(camera_object, target):

    direction = Vector(target) - camera_object.location

    camera_object.rotation_euler = (
        direction
        .to_track_quat("-Z", "Y")
        .to_euler()
    )


point_camera(
    camera,
    (0, 1, 2)
)


# =========================================================
# CAMERA ANIMATION
# =========================================================

camera.location = (15, -22, 13)

camera.keyframe_insert(
    data_path="location",
    frame=DEFAULT_START_FRAME
)

camera.location = (11, -17, 10)

camera.keyframe_insert(
    data_path="location",
    frame=DEFAULT_END_FRAME
)


# =========================================================
# SUN LIGHT
# =========================================================

bpy.ops.object.light_add(
    type="SUN",
    location=(4, -5, 12)
)

sun = bpy.context.object

sun.name = "Sun"

sun.data.energy = 3.0

sun.rotation_euler = (
    math.radians(25),
    math.radians(-20),
    math.radians(-25)
)


# =========================================================
# AREA LIGHT
# =========================================================

bpy.ops.object.light_add(
    type="AREA",
    location=(0, -8, 8)
)

area = bpy.context.object

area.name = "AreaLight"

area.data.energy = 700

area.data.shape = "DISK"

area.data.size = 8

point_camera(
    area,
    (0, 0, 2)
)


# =========================================================
# WORLD
# =========================================================

world = bpy.context.scene.world

if world:

    world.color = (
        0.05,
        0.08,
        0.12
    )


# =========================================================
# SCENE SETTINGS
# =========================================================

scene = bpy.context.scene

# Blender 4.0.2 compatible Eevee engine
scene.render.engine = "BLENDER_EEVEE"

scene.render.resolution_x = WIDTH
scene.render.resolution_y = HEIGHT
scene.render.resolution_percentage = 100

scene.render.fps = FPS

scene.frame_start = DEFAULT_START_FRAME
scene.frame_end = DEFAULT_END_FRAME


# =========================================================
# VIDEO OUTPUT
# =========================================================

scene.render.image_settings.file_format = "FFMPEG"

scene.render.ffmpeg.format = "MPEG4"

scene.render.ffmpeg.codec = "H264"

scene.render.ffmpeg.constant_rate_factor = "MEDIUM"

scene.render.ffmpeg.ffmpeg_preset = "GOOD"

scene.render.filepath = OUTPUT

scene.render.use_file_extension = True


# =========================================================
# COLOR MANAGEMENT
# =========================================================

try:

    scene.view_settings.look = "AgX - Medium High Contrast"

except Exception:

    pass


# =========================================================
# PERFORMANCE
# =========================================================

# Keep Blender from wasting resources on unnecessary
# scene updates.

scene.render.image_settings.color_mode = "RGB"


# =========================================================
# SAVE BLEND FILE
# =========================================================

blend_path = "/home/runner/work/low_poly_scene.blend"

print("")
print("=" * 60)
print("LOW-POLY VIDEO GENERATOR")
print("=" * 60)

print(f"Blender engine : {scene.render.engine}")
print(f"Resolution     : {WIDTH}x{HEIGHT}")
print(f"FPS            : {FPS}")
print(f"Frames         : {scene.frame_start}-{scene.frame_end}")
print(f"Output         : {OUTPUT}")
print("=" * 60)

bpy.ops.wm.save_as_mainfile(
    filepath=blend_path
)

print(f"Blend saved: {blend_path}")


# =========================================================
# RENDER
# =========================================================

print("")
print("STARTING VIDEO RENDER...")
print("")

bpy.ops.render.render(
    animation=True
)


# =========================================================
# VERIFY OUTPUT
# =========================================================

if os.path.exists(OUTPUT):

    size = os.path.getsize(OUTPUT)

    print("")
    print("=" * 60)
    print("RENDER COMPLETE")
    print(f"Video: {OUTPUT}")
    print(f"Size : {size / (1024 * 1024):.2f} MB")
    print("=" * 60)

else:

    print("")
    print("=" * 60)
    print("ERROR: VIDEO FILE WAS NOT CREATED")
    print("=" * 60)

    raise RuntimeError(
        "Blender finished but output video was not found."
    )
