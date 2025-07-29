import math
from IPython.display import Image
from PIL import Image as PILImage
import os

# import pymeshfix
import json
from statistics import median
from .constants import *
import gdsfactory as gf
from gdsfactory.cross_section import Section
from .constants import *
from .materials import *

try:
    from IPython.display import display
except ImportError:
    pass
# import pyvista as pv

# from .picToGDS import main

from math import ceil, cos, pi, sin, tan
import matplotlib.pyplot as plt
import numpy as np
from gdsfactory.generic_tech import LAYER_STACK, LAYER
import copy
import shutil
import trimesh

# from gdsfactory import LAYER_VIEWS

tol = 0.001


def get(c, i):
    try:
        return c[i]
    except:
        try:
            return getattr(c, i)
        except:
            return None


def arange(a, b, d):
    ret = np.linspace(a, b, round((b - a) / (d)) + 1).tolist()
    return ret


def trim(x, dx):
    return round(x / dx) * dx


def extend(endpoints, wm):
    v = endpoints[1] - endpoints[0]
    v = v / np.linalg.norm(v)
    return [(endpoints[0] - wm * v).tolist(), (endpoints[1] + wm * v).tolist()]


def portsides(c):
    ports = c.ports
    bbox = c.bbox_np()
    res = [[], [], [], []]
    xmin0, ymin0 = bbox[0]
    xmax0, ymax0 = bbox[1]
    for p in ports:
        x, y = np.array(p.center) / 1e0

        if abs(x - xmin0) < tol:
            res[2].append(p.name)
        if abs(x - xmax0) < tol:
            res[0].append(p.name)
        if abs(y - ymin0) < tol:
            res[3].append(p.name)
        if abs(y - ymax0) < tol:
            res[1].append(p.name)
    return res


def add_bbox(c, layer, nonport_margin=0):  # , dx=None):
    bbox = c.bbox_np()
    xmin0, ymin0 = bbox[0]
    xmax0, ymax0 = bbox[1]
    l = xmax0 - xmin0
    w = ymax0 - ymin0

    # l = dx*np.ceil((xmax0-xmin0)/dx)
    # w = dx*np.ceil((ymax0-ymin0)/dx)

    # if dx is not None:
    #     if nonport_margin is None:
    #         nonport_margin = dx
    # if nonport_margin is None:
    #     nonport_margin = 0
    margin = nonport_margin
    xmin, ymin, xmax, ymax = (
        xmin0 - margin,
        ymin0 - margin,
        xmin0 + l + margin,
        ymin0 + w + margin,
    )

    for p in c.ports:
        # p = c.ports[k]
        x, y = np.array(p.center) / 1e0
        if abs(x - xmin0) < tol:
            xmin = x
        if abs(x - xmax0) < tol:
            xmax = x
        if abs(y - ymin0) < tol:
            ymin = y
        if abs(y - ymax0) < tol:
            ymax = y
    p = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
    _c = gf.Component()
    _c << c

    if type(layer[0]) is int:
        layer = [layer]
    for layer in layer:
        layer = tuple(layer)
        _c.add_polygon(p, layer=layer)
    for port in c.ports:
        _c.add_port(name=port.name, port=port)
    return _c

    # def pic2gds(fileName, sizeOfTheCell, layerNum=1, isDither=False, scale=1):
    main(fileName, sizeOfTheCell, layerNum, isDither, scale)
    return "image.bmp", "image.gds"


def finish(c, name):
    c.add_label(name, position=c.bbox_np()[1])


def normal_from_orientation(orientation):
    return [cos(orientation / 180 * pi), sin(orientation / 180 * pi)]


def material_voxelate(c, zmin, zmax, layers, layer_stack, materials, path):
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)
    stacks = sum(
        [
            [
                [v.mesh_order, v.material, tuple(layer), k, v.info]
                for k, v in get_layers(layer_stack, layer, withkey=True)
            ]
            for layer in layers
        ],
        [],
    )
    c.flatten()
    stacks = sorted(stacks, key=lambda x: x[0])
    layer_stack_info = dict()
    # raise NotImplementedError("This is a stub")
    lb, ub = c.bbox_np()
    # bbox = [[**lb, zmin], [**ub, zmax]]
    bbox = [[lb[0], lb[1], zmin], [ub[0], ub[1], zmax]]
    layers = [x[2] for x in stacks]

    layer_views = copy.deepcopy(LAYER_VIEWS)

    i = 1
    for stack in stacks:
        order = stack[0]
        m = stack[1]
        l1, l2 = layer = stack[2]
        k = stack[3]

        layer_views.layer_views[k] = LayerView(layer=layer, color="blue", visible=True)
        _layer_stack = copy.deepcopy(layer_stack)
        get(_layer_stack, "layers").clear()

        d = copy.deepcopy(get(layer_stack, "layers")[k])
        if d.zmin <= zmax and d.bounds[1] >= zmin:
            get(_layer_stack, "layers")[k] = d
            # _d.bounds = (_d.zmin, _d.zmin+_d.thickness)
            # origin = (c.extract([layer]).bbox_np()-c.bbox_np())[0].tolist()

            meshes = c.to_3d(
                layer_stack=_layer_stack,
                layer_views=layer_views,
                exclude_layers=set(layers) - {layer},
            ).dump()
            for mesh in meshes:
                OBJ = os.path.join(path, f"{i}_{m}_unnamed{i}.obj")
                i += 1
                trimesh.exchange.export.export_mesh(mesh, OBJ, "obj")
            # pymeshfix.clean_from_file(OBJ, OBJ)
            # repair_obj_open3d(OBJ, OBJ)

            # STL = os.path.abspath(os.path.join(path, f"{k}.stl"))
            # gf.export.to_stl(c, STL, layer_stack=_layer_stack)

            # STL = os.path.join(path, f'{k}_{l1}_{l2}.stl')
            # pymeshfix.clean_from_file(STL, STL)
            # STL1 = os.path.join(path, f'{order}_{m}_{k}.stl')
            # os.replace(STL, STL1)

            # mesh = pv.read(STL)
            # im = stl_to_array(mesh, dl*unit, bbox)
            # np.save(os.path.join(path, f'{k}.npy'), im)

            layer_stack_info[k] = {
                "layer": (l1, l2),
                "zmin": d.zmin,
                "thickness": d.thickness,
                # "material": matname(m),
                "mesh_order": stack[0],
                # "origin": origin,
            }
    return layer_stack_info


def get_layers(layer_stack, layer, withkey=False):
    r = []
    d = get(layer_stack, "layers").items()

    for k, x in d:
        l = get(x, "layer")
        if l is not None:
            t = get(l, "layer")
            if t is not None and tuple(t) == tuple(layer):
                if withkey:
                    x = k, x
                r.append(x)
    if r:
        return r

    for k, x in d:
        l = get(x, "derived_layer")
        if l is not None:
            t = get(l, "layer")
            if t is not None and tuple(t) == tuple(layer):
                if withkey:
                    x = k, x
                r.append(x)
    return r


def wavelength_range(center, bandwidth, length=3):
    f1 = 1 / (center + bandwidth / 2)
    f2 = 1 / (center - bandwidth / 2)
    hw = (f2 - f1) / 2
    f1 = 1 / center - hw
    f2 = 1 / center + hw
    return sorted([1 / x for x in np.linspace(f1, f2, length).tolist()])


def wrap(wavelengths):
    if isinstance(wavelengths, float) or isinstance(wavelengths, int):
        wavelengths = [[wavelengths]]
    elif isinstance(wavelengths[0], float) or isinstance(wavelengths[0], int):
        wavelengths = [wavelengths]
    return wavelengths


def save_problem(prob, path):
    path = os.path.abspath(path)
    bson_data = json.dumps(prob)
    # prob["component"] = c0

    path = prob["path"]
    if not os.path.exists(path):
        os.makedirs(path)
        #   compiling julia code...
        #   """)
    prob_path = os.path.join(path, "problem.json")
    with open(prob_path, "w") as f:
        # Write the BSON data to the file
        f.write(bson_data)
    print("using simulation folder", path)


def load_prob(path):
    path = os.path.abspath(path)
    print(f"loading problem from {path}")
    return json.loads(open(os.path.join(path, "problem.json"), "rb").read())


def create_gif(image_path, output_path, duration):
    """
    Creates a GIF from a list of image paths.

    Args:
        image_paths: A list of file paths to the images.
        output_path: The output path for the generated GIF.
        duration: The duration of each frame in milliseconds (default: 200).
    """
    image_paths = os.listdir(image_path)
    image_paths = sorted(image_paths, key=lambda x: float(x[0:-4]))
    frames = [PILImage.open(os.path.join(image_path, f)) for f in image_paths]

    # Ensure all frames have the same palette if necessary
    for i in range(len(frames)):
        if frames[i].mode != "RGB":
            frames[i] = frames[i].convert("RGB")

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,  # 0 means infinite loop
    )


def make_movie(path):
    # framerate = 10 / load_prob(path)["saveat"]
    framerate = 2
    duration = 1000 / framerate
    FRAMES = os.path.join(path, "frames")
    MOVIE = os.path.join(path, "sim.mp4")
    # shutil.rmtree(MOVIE, ignore_errors=True)
    GIF = os.path.join(path, "sim.gif")
    create_gif(FRAMES, GIF, duration)
    return Image(open(GIF, "rb").read())
    # if saveat is None:
    #     saveat = load_prob(path)["saveat"]

    # g = np.load(os.path.join(path, "temp", 'g.npy')).T
    # gmax = np.max(np.abs(g))

    # dir = os.path.join(path, "temp", 'fields')
    # umax = 0
    # fns = sorted(os.listdir(dir), key=lambda x: float(x[0:-4]))
    # for fn in fns:
    #     a = np.load(os.path.join(dir, fn))
    #     v = np.max(np.abs(a))
    #     if umax < v:
    #         umax = v

    # for fn in fns:
    #     name = fn[0:-4]
    #     a = np.load(os.path.join(FIELDS, fn)).T
    #     fig, axs = plt.subplots(1, 2)
    #     axs[1].imshow(a, cmap='seismic', origin='lower',
    #                   vmin=-umax, vmax=umax)
    #     axs[0].imshow(-g, cmap='gray',
    #                   origin='lower', vmin=-gmax, vmax=0)
    #     plt.savefig(os.path.join(FRAMES, f"{name}.png"))
    #     plt.close(fig)

    # fns = sorted(os.listdir(FRAMES), key=lambda x: float(x[0:-4]))
    # frame = height = width = layers = video = None
    # for i, fn in enumerate(fns):
    #     frame = cv2.imread(os.path.join(FRAMES, fn))
    #     if i == 0:
    #         height, width, layers = frame.shape
    #         video = cv2.VideoWriter(
    #             MOVIE, 0x7634706d, saveat, (width, height))

    #     video.write(frame)

    # cv2.destroyAllWindows()
    # video.release()
