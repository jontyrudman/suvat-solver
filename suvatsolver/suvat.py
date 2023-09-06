import math
from pydantic import validate_call
from dataclasses import dataclass, asdict
from typing import Self
import itertools


@validate_call
@dataclass
class Suvat:
    s: list[float] | None = None
    u: list[float] | None = None
    v: list[float] | None = None
    a: list[float] | None = None
    t: list[float] | None = None

    def unknowns(self) -> list[str]:
        return [key for key, val in asdict(self).items() if val is None]

    def solvable(self) -> bool:
        return len(self.unknowns()) <= 2

    def solve_for_all(self) -> Self:
        return (
            self.solve_for_s().solve_for_u().solve_for_v().solve_for_a().solve_for_t()
        )

    def solve_for_s(self) -> Self:
        if self.s is not None:
            return self

        if self.t == 0:
            self.s = [0.0]
            return self

        # Given u, a, t
        if self.u is not None and self.a is not None and self.t is not None:
            self.s = [
                (u * t) + (0.5 * a * (t**2))
                for u, a, t in itertools.product(self.u, self.a, self.t)
            ]
            return self

        # Given u, v, t
        if self.u is not None and self.v is not None and self.t is not None:
            self.s = [
                0.5 * t * (u + v)
                for u, v, t in itertools.product(self.u, self.v, self.t)
            ]
            return self

        # Given v, a, t
        if self.v is not None and self.a is not None and self.t is not None:
            self.s = [
                (v * t) - (0.5 * a * (t**2))
                for v, a, t in itertools.product(self.v, self.a, self.t)
            ]
            return self

        # Given u, v, a
        if self.u is not None and self.v is not None and self.a is not None:
            self.s = [
                ((v**2) - (u**2)) / (2.0 * a)
                for u, v, a in itertools.product(self.u, self.v, self.a)
            ]
            return self

        raise Exception("Cannot be solved with more than two unknowns!")

    def solve_for_u(self) -> Self:
        if self.u is not None:
            return self

        if self.t == 0:
            self.u = [0.0]
            return self

        # Given v, a, t
        if self.v is not None and self.a is not None and self.t is not None:
            self.u = [
                v - (a * t) for v, a, t in itertools.product(self.v, self.a, self.t)
            ]
            return self

        # Given s, v, t
        if self.s is not None and self.v is not None and self.t is not None:
            self.u = [
                ((2.0 * s) / t) - v
                for s, v, t in itertools.product(self.s, self.v, self.t)
            ]
            return self

        # Given s, v, a, no certainty when dealing with negatives
        if self.s is not None and self.v is not None and self.a is not None:
            self.u = []
            for s, v, a in itertools.product(self.s, self.v, self.a):
                self.u += [
                    math.sqrt((v**2) - 2.0 * a * s),
                    -1 * math.sqrt((v**2) - 2.0 * a * s),
                ]
            return self

        # Given s, a, t
        if self.s is not None and self.a is not None and self.t is not None:
            self.u = [
                (s / t) - 0.5 * a * t
                for s, a, t in itertools.product(self.s, self.a, self.t)
            ]
            return self

        raise Exception("Cannot be solved with more than two unknowns!")

    def solve_for_v(self) -> Self:
        if self.v is not None:
            return self

        if self.t == 0:
            self.v = [0.0]
            return self

        # Given u, a, t
        if self.u is not None and self.a is not None and self.t is not None:
            self.v = [
                u + (a * t) for u, a, t in itertools.product(self.u, self.a, self.t)
            ]
            return self

        # Given s, u, a
        if self.s is not None and self.u is not None and self.a is not None:
            self.v = []
            for s, u, a in itertools.product(self.s, self.u, self.a):
                self.v += [
                    math.sqrt((u**2) + (2 * a * s)),
                    -1 * math.sqrt((u**2) + (2 * a * s)),
                ]
            return self

        # Given s, a, t
        if self.s is not None and self.a is not None and self.t is not None:
            self.v = [
                (s / t) + (0.5 * a * t)
                for s, a, t in itertools.product(self.s, self.a, self.t)
            ]
            return self

        # Given s, u, t
        if self.s is not None and self.u is not None and self.t is not None:
            self.v = [
                ((2 * s) / t) - u
                for s, u, t in itertools.product(self.s, self.u, self.t)
            ]
            return self

        raise Exception("Cannot be solved with more than two unknowns!")

    def solve_for_a(self) -> Self:
        if self.a is not None:
            return self

        if self.t == 0:
            self.a = [0.0]
            return self

        # Given u, v, t
        if self.u is not None and self.v is not None and self.t is not None:
            self.a = [
                (v - u) / t for u, v, t in itertools.product(self.u, self.v, self.t)
            ]
            return self

        # Given s, u, v
        if self.s is not None and self.u is not None and self.v is not None:
            self.a = [
                ((v**2) - (u**2)) / (2.0 * s)
                for s, u, v in itertools.product(self.s, self.u, self.v)
            ]
            return self

        # Given s, u, t
        if self.s is not None and self.u is not None and self.t is not None:
            self.a = [
                (2.0 * (s - (u * t))) / (t**2)
                for s, u, t in itertools.product(self.s, self.u, self.t)
            ]
            return self

        # Given s, v, t
        if self.s is not None and self.v is not None and self.t is not None:
            self.a = [
                (2.0 * ((v * t) - s)) / (t**2)
                for s, v, t in itertools.product(self.s, self.v, self.t)
            ]
            return self

        raise Exception("Cannot be solved with more than two unknowns!")

    def solve_for_t(self) -> Self:
        if self.t is not None:
            return self

        # Given s, u, v
        if self.s is not None and self.u is not None and self.v is not None:
            self.t = [
                (2.0 * s) / (u + v)
                for s, u, v in itertools.product(self.s, self.u, self.v)
            ]
            return self

        # Given s, u, a
        if self.s is not None and self.u is not None and self.a is not None:
            self.t = [
                u / (s - (0.5 * a))
                for s, u, a in itertools.product(self.s, self.u, self.a)
            ]
            return self

        # Given u, v, a
        if self.u is not None and self.v is not None and self.a is not None:
            self.t = []
            for u, v, a in itertools.product(self.u, self.v, self.a):
                if v - u == 0 and a == 0:
                    self.t += [1.0]
                    return self
                self.t += [(v - u) / a]
            return self

        # Given s, v, a, the u generated in the formula will be positive
        if self.s is not None and self.v is not None and self.a is not None:
            self.t = []
            for s, v, a in itertools.product(self.s, self.v, self.a):
                top = v - math.sqrt((v**2) - (2.0 * a * s))
                if top == 0 and self.a == 0:
                    self.t += [1.0]
                    return self
                self.t += [top / a, -1 * top / a]
            return self

        raise Exception("Cannot be solved with more than two unknowns!")
