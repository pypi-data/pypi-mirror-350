from .setup import *
from ..constants import *
from ..layers import *
from ..utils import *
import gdsfactory as gf
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

from gdsfactory.cross_section import Section
from gdsfactory.generic_tech import LAYER_STACK, LAYER


def make_prob(
    path,
    component=None,
    wavelengths=None,
    entries=None,
    keys=["2,1"],
    study="sparams",
    sources=None,
    monitors=None,
    frequencies=None,
    wl_1_f=None,
    modes=[],
    #
    layer_stack={},
    materials={},
    verbose=True,
    #
    targets=None,
    symmetries=[],
    # design_layer=DESIGN,
    init_holes=True,
    fill_material=None,
    void_material=None,
    iters=None,
    lmin=None,
    stoploss=None,
    path_length_multiple=0.85,
    **kwargs
):

    if targets is not None:
        study = "inverse_design"
        design_layer = layer_stack["design"].layer.layer
        materials["design"]["relative_mesh_density"] = math.sqrt(
            materials[fill_material]["epsilon"]
        )

        if "phase_shifter" in targets:
            keys = ["o2@0,o1@0"]
            wavelengths = [targets["phase_shifter"]]
        else:
            if "tparams" in targets:
                for center_wavelength in targets["tparams"]:
                    d = {}
                    # for k in targets["tparams"][center_wavelength]:
                    #     po, mo, pi, mi = unpack_sparam_key(k)
                    #     # if mo == 0:
                    #     #     _mo = 1
                    #     # elif mo == 1:
                    #     #     _mo = 0
                    #     # else:
                    #     #     mo = None

                    #     # if mo is not None:
                    #     #     _k = f"{po}@{_mo},{pi}@{mi}"
                    #     #     if _k not in targets["tparams"][center_wavelength]:
                    #     #         d[_k] = 0

                    #     _k = f"{pi}@{mi},{pi}@{mi}"
                    #     if _k not in targets["tparams"][center_wavelength]:
                    #         d[_k] = 0
                    #     # _k = f"o{pi}@1,o{pi}@{mi}"
                    #     # if _k not in targets["tparams"][center_wavelength]:
                    #     #     d[_k] = 0
                    # targets["tparams"][center_wavelength].update(d)

            keys = SortedSet()
            wavelengths = SortedSet()
            for d in targets:
                wavelengths.add(d["wavelength"])
                keys.add(d["key"])
            keys = list(keys)
            wavelengths = list(wavelengths)
        wavelengths = [[w] for w in wavelengths]

    if frequencies is not None:
        frequencies = wrap(frequencies)
        assert wl_1_f is not None
        assert wavelengths is None
        wavelengths = [[wl_1_f / f for f in v] for v in frequencies]
        ordering = "frequency"
    else:
        wavelengths = wrap(wavelengths)
        ordering = "wavelength"

    for mode in modes:
        if "frequency" in mode:
            if "wavelength" not in mode:
                mode["wavelength"] = wl_1_f / mode["frequency"]

    wavelengths = [sorted(w) for w in wavelengths]
    wavelengths = sorted(wavelengths, key=lambda x: x[0])
    center_wavelength = median(map(median, wavelengths))
    if not entries:
        entries = []

        for w in wavelengths:
            for k in keys:
                entries.append([w, *unpack_sparam_key(k)])
    l = []
    for w, po, mo, pi, mi in entries:
        k = [w, pi, mi, pi, mi]
        if k not in entries:
            l.append(k)
    entries.extend(l)

    imow = {}
    for w, po, mo, pi, mi in entries:
        if pi not in imow:
            imow[pi] = {}
        if mi not in imow[pi]:
            imow[pi][mi] = {}

        if po not in imow[pi][mi]:
            imow[pi][mi][po] = mo
        else:
            imow[pi][mi][po] = max(imow[pi][mi][po], mo)

    runs = []
    for _w in [1]:
        for i in imow:
            for mi in imow[i]:
                d = {
                    "sources": {
                        i: {
                            "wavelength_mode_numbers": [[w, [mi]] for w in wavelengths],
                        }
                    },
                    "monitors": {
                        o: {
                            "wavelength_mode_numbers": [
                                [w, list(range(imow[i][mi][o] + 1))]
                                for w in wavelengths
                            ],
                        }
                        for o in imow[i][mi]
                    },
                }
                d["sources"] = SortedDict(d["sources"])
                d["monitors"] = SortedDict(d["monitors"])
                if component is None:
                    0
                else:
                    runs.append(d)

    prob = setup(
        path,
        component=component,
        study=study,
        center_wavelength=center_wavelength,
        runs=runs,
        layer_stack=layer_stack,
        materials=materials,
        modes=modes,
        verbose=verbose,
        keys=keys,
        ordering=ordering,
        #  sources=sources, monitors=monitors,
        **kwargs
    )
    prob["wavelengths"] = wavelengths

    if targets:
        polys = component.extract([design_layer]).get_polygons()
        if not symmetries:
            symmetries = [[]] * len(polys)
        else:
            if type(symmetries[0]) is not list:
                symmetries = [symmetries] * len(polys)

        def _bbox(b):
            return [[b.left / 1e3, b.bottom / 1e3], [b.right / 1e3, b.top / 1e3]]

        ks = set(materials[fill_material].keys()).intersection(
            set(materials[void_material].keys())
        )
        swaps = {
            k: (materials[void_material][k], materials[fill_material][k]) for k in ks
        }
        prob = {
            **prob,
            **{
                "targets": targets,
                "designs": [
                    {
                        "swaps": swaps,
                        "bbox": _bbox(p.bbox()),
                        "symmetries": s,
                    }
                    for p, s in zip(list(polys.values())[0], symmetries)
                ],
                "init_holes": init_holes,
                "iters": iters,
                "lmin": lmin,
                "stoploss": stoploss,
                "path_length_multiple": path_length_multiple,
            },
        }
    save_problem(prob, path)
    return prob

    # l = [k for k in imow if port_number(k) == pi]
    # if not l:
    #     imow[f"o{pi}@{mi}"] = []
    # else:
    #     k = l[0]
    #     mn = max(mode_number(k), mi)
    #     if mn != mode_number(k):
    #         imow[i] = imow[k]
    #         del imow[k]

    # l = [k for k in imow[i] if port_number(k) == po]
    # if not l:
    #     imow[f"o{pi}@{mi}"]
    # else:
    #     k = l[0]
    #     mn = max(mode_number(k), mi)
    #     if mn != mode_number(k):
    #         imow[f"o{pi}@{mn}"] = imow[k]
    #         del imow[k]

    # if po not in imow[pi]:
    #     imow[pi]["o"][po] = mo
    # else:
    #     imow[pi]["o"][po] = max(imow[pi]["o"][po], mo)
