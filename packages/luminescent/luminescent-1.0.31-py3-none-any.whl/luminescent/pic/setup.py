import platform
import subprocess
from ..constants import *
from ..layers import *
from ..utils import *
from ..materials import *
import json
import gdsfactory as gf
from copy import deepcopy

# from time import time
import datetime
from math import cos, pi, sin
import os
import numpy as np

from sortedcontainers import SortedDict, SortedSet
from gdsfactory.generic_tech import LAYER_STACK, LAYER


def setup(
    path,
    study,
    center_wavelength,
    boundaries=["PML", "PML", "PML"],
    nres=6,
    dx=None,
    dy=None,
    dz=None,
    component=None,
    z=None,
    # zmargin=None,
    zmin=None,
    zmax=None,
    zmargin_mode=None,
    xmargin_mode=None,
    port_margin="auto",
    runs=[],
    sources=[],
    layer_stack=SOI220,
    materials=dict(),
    core="core",
    exclude_layers=[],
    Courant=None,
    gpu=None,
    dtype=np.float32,
    saveat=10,
    magic="",
    name=None,
    source_port_margin=0.1,
    modes={},
    ports={},
    approx_2D_mode=False,
    show_field="Hz",
    T=None,
    field_decay_threshold=None,
    path_length_multiple=None,
    relpml=1,
    relcourant=0.9,
    hasmetal=None,
    keys=None,
    ordering="frequency",
    #
    field_slices=None,
    geometry_slices=None,
    force=False,
    verbose=False,
):
    if force:
        shutil.rmtree(path, ignore_errors=True)
    elif os.path.exists(path):
        raise FileExistsError(
            f"Path {path} already exists. Use force=True to overwrite."
        )

    os.makedirs(path, exist_ok=True)

    if approx_2D_mode:
        N = 2
    else:
        N = 3
        approx_2D_mode = None

    prob = {
        "nres": nres,
        "center_wavelength": center_wavelength,
        "name": name,
        "path": path,
        "keys": keys,
        "show_field": show_field,
        "dx": dx,
        "dy": dy,
        "dz": dz,
        "z": z,
        "T": T,
        "field_decay_threshold": field_decay_threshold,
        "path_length_multiple": path_length_multiple,
        "saveat": saveat,
        "verbose": verbose,
        "field_slices": field_slices,
        "geometry_slices": geometry_slices,
        "boundaries": boundaries[0:N],
        "approx_2D_mode": approx_2D_mode,
        "relpml": relpml,
        "relcourant": relcourant,
        "hasmetal": hasmetal,
        "ordering": ordering,
    }

    prob["class"] = "pic"
    prob["dtype"] = str(dtype)
    prob["timestamp"] = (
        datetime.datetime.now().isoformat(timespec="seconds").replace(":", "-")
    )
    prob["magic"] = magic

    gpu_backend = gpu
    # if gpu_backend:s
    prob["gpu_backend"] = gpu_backend

    if component is None:
        0
    else:
        c = component
        for k, v in ports.items():
            if "layer" in v:
                0
            else:
                bbox = c.bbox_np()
                l, w = bbox[1] - bbox[0]
                v["center"] = (sum(bbox) / 2).tolist() + [v["z"]]
                v["start"] = [-l / 2, -w / 2]
                v["stop"] = [l / 2, w / 2]
                if v["sign"] > 0:
                    frame = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
                else:
                    frame = [[-1, 0, 0], [0, 1, 0], [0, 0, -1]]
                v["frame"] = frame
                v["normal"] = frame[2]

        for p in c.get_ports_list(prefix="o"):
            v = {
                "center": (np.array(p.center) / 1e0).tolist(),
                "normal": [
                    cos(p.orientation / 180 * pi),
                    sin(p.orientation / 180 * pi),
                ],
                "tangent": [
                    -sin(p.orientation / 180 * pi),
                    cos(p.orientation / 180 * pi),
                ],
                "width": p.width / 1e0,
            }
            z, n = [0, 0, 1], [*v["normal"], 0]
            t = np.cross(z, n).tolist()
            v["frame"] = [t, z, n]
            ports[p.name] = v

        prob["ports"] = ports

        if c and c.get_ports_list():
            d = layer_stack.layers[core]
            hcore = d.thickness
            zcore = d.zmin

            if zmargin_mode is None:
                zmargin_mode = 3 * hcore
            if type(zmargin_mode) in [int, float]:
                zmargin_mode = [zmargin_mode, zmargin_mode]
            # if zmargin is None:
            #     zmargin = [1.1 * zmargin_mode[0], 1.1 * zmargin_mode[1]]
            # if type(zmargin) in [int, float]:
            #     zmargin = [zmargin, zmargin]

            port_width = max([p.width / 1e0 for p in c.ports])
            if xmargin_mode is None:
                xmargin_mode = port_width
            if type(xmargin_mode) in [int, float]:
                xmargin_mode = [xmargin_mode, xmargin_mode]
            print(f"xmargin_mode: {xmargin_mode}")

            if zmin is None:
                zmin = zcore - 3 * hcore
            if zmax is None:
                zmax = zcore + 4 * hcore

            # h = hcore + zmargin[0] + zmargin[1]
            # zmin = zcore - zmargin[0]
            # zmax = zmin + h
            #
            # xmargin = ymargin = 2*port_width

            wmode = port_width + xmargin_mode[0] + xmargin_mode[1]
            hmode = hcore + zmargin_mode[0] + zmargin_mode[1]
            zmode = zcore - zmargin_mode[0]
            zcenter = zmode + hmode / 2

        layers = set(c.layers) - set(exclude_layers)

        MODES = os.path.join(path, "modes")
        os.makedirs(MODES, exist_ok=True)
        GEOMETRY = os.path.join(path, "geometry")
        os.makedirs(GEOMETRY, exist_ok=True)

        layer_stack_info = material_voxelate(
            c, zmin, zmax, layers, layer_stack, materials, GEOMETRY
        )
        dir = os.path.dirname(os.path.realpath(__file__))

        for f in ["solvemodes.py"]:
            fn = os.path.join(dir, f)
            if platform.system() == "Windows":
                os.system(f"copy /Y {fn} {MODES}")
            else:
                subprocess.run(["cp", fn, MODES])
        prob["layer_stack"] = layer_stack_info
        prob["study"] = study
        prob["materials"] = materials

        prob["N"] = N

        for run in runs:
            for k, v in run["sources"].items():
                p = ports[k]
                ct = np.array(p["center"])
                n = np.array(p["normal"])
                v["center"] = (ct + n * source_port_margin).tolist()
            for k, v in run["monitors"].items():
                p = ports[k]
                v["center"] = copy.deepcopy(p["center"])
            for k, v in list(run["sources"].items()) + list(run["monitors"].items()):
                p = ports[k]
                v["frame"] = p["frame"]
                if len(v["center"]) == 2:
                    v["center"] += [zcenter]
                    v["start"] = [-wmode / 2, zmode - zcenter]
                    v["stop"] = [wmode / 2, zmode + hmode - zcenter]
                else:
                    v["start"] = p["start"]
                    v["stop"] = p["stop"]

        prob["runs"] = runs
        bbox = c.bbox_np().tolist()
        bbox[0].append(zmin)
        bbox[1].append(zmax)

        prob["bbox"] = bbox

    if not os.path.exists(path):
        os.makedirs(path)
    prob["modes"] = modes
    # prob["path_length"] = 2*(l+r+lwg)
    return prob


def port_name(port):
    s = str(port).split("@")[0]
    if s[0] == "o":
        return s
    return f"o{s}"


def port_number(port):
    s = str(port).split("@")[0]
    if s[0] == "o":
        s = s[1:]
    return int(s)


def mode_number(port):
    l = str(port).split("@")
    return 0 if len(l) == 1 else int(l[1])


def unpack_sparam_key(k):
    o, i = k.split(",")
    po, pi = port_name(o), port_name(i)
    mo, mi = mode_number(o), mode_number(i)
    return po, mo, pi, mi


def long_sparam_key(k):
    po, mo, pi, mi = unpack_sparam_key(k)
    return f"{po}@{mo},{pi}@{mi}"
