import argparse
from typing import Callable, NoReturn
from . import Suvat, componentise_2d, componentise_3d


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="SUVAT Solver",
        description="Solve SUVAT equations. Requires at least three known values.",
    )

    # TODO: Max 3
    parser.add_argument(
        "-d",
        "--dimensions",
        choices=range(1, 4),
        type=int,
        help="number of dimensions to calculate suvat for",
    )

    parser.add_argument(
        "--angle", type=float, nargs="*", help="angle between dimensions"
    )

    parser.add_argument(
        "-s",
        "--displacement",
        type=float,
        nargs="*",
        help="how far the projectile has moved (m) from its starting position",
    )
    parser.add_argument(
        "-u",
        "--initial-velocity",
        type=float,
        nargs="*",
        help="the projectile's starting velocity (m/s)",
    )
    parser.add_argument(
        "-v",
        "--final-velocity",
        type=float,
        nargs="*",
        help="the projectile's final velocity (m/s)",
    )
    parser.add_argument(
        "-a",
        "--acceleration",
        type=float,
        nargs="*",
        help="the projectile's acceleration (m/s^2)",
    )
    parser.add_argument(
        "-t",
        "--time",
        type=float,
        nargs="*",
        help="the duration (s) of the projectile's motion",
    )

    return parser


def pretty_format_uncertain_values(l: list | None) -> str:
    if l is None:
        return "None"

    out = ""
    for i, item in enumerate(l):
        if i > 0:
            out += " or "
        out += str(item)
    return out


def pprint_suvat(suvat: Suvat) -> None:
    print(f"  Displacement = {pretty_format_uncertain_values(suvat.s)} m")
    print(f"  Initial velocity = {pretty_format_uncertain_values(suvat.u)} m/s")
    print(f"  Final velocity = {pretty_format_uncertain_values(suvat.v)} m/s")
    print(f"  Acceleration = {pretty_format_uncertain_values(suvat.a)} m/s^2")
    print(f"  Time = {pretty_format_uncertain_values(suvat.t)} s")


def prepare_components(
    args: argparse.Namespace,
    err: Callable[[str], NoReturn],
) -> list[dict[str, float | None]]:
    """
    Attempts to split non-component arguments into components based on dimension count and angles.
    """
    dim = args.dimensions or 1
    angle = args.angle
    suvat_dict: dict[str, list[float] | None] = {
        "s": args.displacement,
        "u": args.initial_velocity,
        "v": args.final_velocity,
        "a": args.acceleration,
        "t": args.time,
    }

    for val in suvat_dict.values():
        if val is None:
            continue
        if len(val) > dim:
            err("Too many suvat args for the number of dimensions.")
        if angle is not None and len(val) > 1:
            err("Too many suvat args for the number of angles. Only provide 1 of each.")

    def _transform_dict(
        _d: dict[str, list[float] | None]
    ) -> list[dict[str, float | None]]:
        return [
            {k: v[i] if v is not None and i < len(v) else None for k, v in _d.items()}
            for i in range(dim)
        ]

    if angle is not None:
        # Multiple dimensions but the number of angles doesn't match
        if len(angle) != dim - 1:
            err(
                "Count of angles must be one less than the number of dimensions, or pre-componentise suvat args and provide no angles."
            )

        # 2d or 3d
        if dim == 2 or dim == 3:

            def _get_component_list(_val) -> list[float]:
                if dim == 2:
                    _components = componentise_2d(_val, angle[0])
                    return [_components["x"], _components["y"]]
                if dim == 3:
                    _components = componentise_3d(_val, angle[0], angle[1])
                    return [_components["x"], _components["y"], _components["z"]]
                raise ValueError("dim not 2 or 3")

            component_suvat_dict = {
                k: _get_component_list(v[0]) if v is not None else None
                for k, v in suvat_dict.items()
            }
            return _transform_dict(component_suvat_dict)

    # No angles, pre-componentised
    return _transform_dict(suvat_dict)


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()

    # If less than three values are provided, fail
    if len([val for val in args.__dict__.values() if val is not None]) < 3:
        parser.error("At least three values must be provided for the solver to work.")

    for components, dimension in zip(
        prepare_components(args, parser.error), ["x", "y", "z"]
    ):
        solved_suvat = Suvat(**components).solve_for_all()
        print(f"{dimension} dimension:")
        pprint_suvat(solved_suvat)
        print()

    print("Solved!")
