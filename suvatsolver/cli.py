import argparse
from . import Suvat


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="SUVAT Solver",
        description="Solve SUVAT equations. Requires at least three known values.",
    )

    parser.add_argument(
        "-s",
        "--displacement",
        type=float,
        help="how far the projectile has moved (m) from its starting position",
    )
    parser.add_argument(
        "-u",
        "--initial-velocity",
        type=float,
        help="the projectile's starting velocity (m/s)",
    )
    parser.add_argument(
        "-v",
        "--final-velocity",
        type=float,
        help="the projectile's final velocity (m/s)",
    )
    parser.add_argument(
        "-a",
        "--acceleration",
        type=float,
        help="the projectile's acceleration (m/s^2)",
    )
    parser.add_argument(
        "-t",
        "--time",
        type=float,
        help="the duration (s) of the projectile's motion",
    )

    return parser


def pprint_suvat(suvat: Suvat) -> None:
    print(f"Displacement = {suvat.s} m")
    print(f"Initial velocity = {suvat.u} m/s")
    print(f"Final velocity = {suvat.v} m/s")
    print(f"Acceleration = {suvat.a} m/s^2")
    print(f"Time = {suvat.t} s")


def cli() -> None:
    parser = get_parser()
    args = parser.parse_args()

    # If less than three values are provided, fail
    if len([val for val in args.__dict__.values() if val is not None]) < 3:
        parser.error("At least three values must be provided for the solver to work.")

    solved_suvat = Suvat(
        s=args.displacement,
        u=args.initial_velocity,
        v=args.final_velocity,
        a=args.acceleration,
        t=args.time,
    ).solve_for_all()

    print("Solved!\n")
    pprint_suvat(solved_suvat)
