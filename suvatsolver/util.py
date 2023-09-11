import math


def componentise_2d(magnitude: float, angle_xtodir_xy: float) -> dict[str, float]:
    return {
        "x": magnitude * math.cos(math.radians(angle_xtodir_xy)),
        "y": magnitude * math.sin(math.radians(angle_xtodir_xy)),
    }


def componentise_3d(
    magnitude: float, angle_xtodir_xy: float, angle_xtodir_xz: float
) -> dict[str, float]:
    def _get_x_and_z():
        _components = componentise_2d(
            magnitude * math.cos(math.radians(angle_xtodir_xy)), angle_xtodir_xz
        )
        return {"x": _components["x"], "z": _components["y"]}

    return {"y": magnitude * math.sin(math.radians(angle_xtodir_xy)), **_get_x_and_z()}
