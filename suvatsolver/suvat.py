import math
from typing import Self
import itertools


class Suvat:
    s: list[float] | None = None
    u: list[float] | None = None
    v: list[float] | None = None
    a: list[float] | None = None
    t: list[float] | None = None

    def __init__(
        self,
        s: float | None = None,
        u: float | None = None,
        v: float | None = None,
        a: float | None = None,
        t: float | None = None,
    ):
        if sum(x is not None for x in [s, u, v, a, t]) < 3:
            raise Exception("Less than three known values")

        if (
            a is not None
            and u is not None
            and v is not None
            and ((a > 0 and u > v) or (a < 0 and u < v))
        ):
            raise Exception("Acceleration mismatch")

        if t is not None and t <= 0:
            raise Exception("Time cannot be less than or equal to zero")

        if s != 0 and u == 0 and v == 0:
            raise Exception("Displacement cannot be non-zero with zero velocity")

        self.s = [float(s)] if s is not None else None
        self.u = [float(u)] if u is not None else None
        self.v = [float(v)] if v is not None else None
        self.a = [float(a)] if a is not None else None
        self.t = [float(t)] if t is not None else None

    def _append_if_unique(self, variable_name: str, *values: float):
        if variable_name not in list("suvat"):
            raise ValueError("variable_name must be one of the suvat chars!")

        for value in values:
            original_assignment = self.__getattribute__(variable_name)
            if original_assignment is None:
                self.__setattr__(variable_name, [value])
            elif (
                isinstance(original_assignment, list)
                and value not in original_assignment
            ):
                self.__setattr__(variable_name, [*original_assignment, value])

    def unknowns(self) -> list[str]:
        return [key for key, val in vars(self).items() if val is None]

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
            for u, a, t in itertools.product(self.u, self.a, self.t):
                self._append_if_unique("s", (u * t) + (0.5 * a * (t**2)))
            return self

        # Given u, v, t
        if self.u is not None and self.v is not None and self.t is not None:
            for u, v, t in itertools.product(self.u, self.v, self.t):
                self._append_if_unique("s", 0.5 * t * (u + v))
            return self

        # Given v, a, t
        if self.v is not None and self.a is not None and self.t is not None:
            for v, a, t in itertools.product(self.v, self.a, self.t):
                self._append_if_unique("s", (v * t) - (0.5 * a * (t**2)))
            return self

        # Given u, v, a
        if self.u is not None and self.v is not None and self.a is not None:
            for u, v, a in itertools.product(self.u, self.v, self.a):
                self._append_if_unique("s", ((v**2) - (u**2)) / (2.0 * a))
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
            for v, a, t in itertools.product(self.v, self.a, self.t):
                self._append_if_unique("u", v - (a * t))
            return self

        # Given s, v, t
        if self.s is not None and self.v is not None and self.t is not None:
            for s, v, t in itertools.product(self.s, self.v, self.t):
                self._append_if_unique("u", ((2.0 * s) / t) - v)
            return self

        # Given s, v, a, no certainty when dealing with negatives
        if self.s is not None and self.v is not None and self.a is not None:
            for s, v, a in itertools.product(self.s, self.v, self.a):
                res = math.sqrt((v**2) - 2.0 * a * s)

                # Pick the u greater than v if a is negative
                if (a < 0 and res > v) or (a > 0 and res < v):
                    self._append_if_unique("u", res)
                if (a < 0 and -1 * res > v) or (a > 0 and -1 * res < v):
                    self._append_if_unique("u", -1 * res)

            return self

        # Given s, a, t
        if self.s is not None and self.a is not None and self.t is not None:
            for s, a, t in itertools.product(self.s, self.a, self.t):
                self._append_if_unique("u", (s / t) - 0.5 * a * t)
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
            for u, a, t in itertools.product(self.u, self.a, self.t):
                self._append_if_unique("v", u + (a * t))
            return self

        # Given s, u, a
        if self.s is not None and self.u is not None and self.a is not None:
            for s, u, a in itertools.product(self.s, self.u, self.a):
                res = math.sqrt((u**2) + (2 * a * s))

                # Pick the v (maybe multiple) greater than u if a is positive
                if (a > 0 and res > u) or (a < 0 and res < u):
                    self._append_if_unique("v", res)

                # Give the negative version if also applicable, due to uncertainty
                if (a > 0 and -1 * res > u) or (a < 0 and -1 * res < u):
                    self._append_if_unique("v", -1 * res)

            return self

        # Given s, a, t
        if self.s is not None and self.a is not None and self.t is not None:
            for s, a, t in itertools.product(self.s, self.a, self.t):
                self._append_if_unique("v", (s / t) + (0.5 * a * t))
            return self

        # Given s, u, t
        if self.s is not None and self.u is not None and self.t is not None:
            for s, u, t in itertools.product(self.s, self.u, self.t):
                self._append_if_unique("v", ((2 * s) / t) - u)
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
            for u, v, t in itertools.product(self.u, self.v, self.t):
                self._append_if_unique("a", (v - u) / t)
            return self

        # Given s, u, v
        if self.s is not None and self.u is not None and self.v is not None:
            for s, u, v in itertools.product(self.s, self.u, self.v):
                self._append_if_unique("a", ((v**2) - (u**2)) / (2.0 * s))
            return self

        # Given s, u, t
        if self.s is not None and self.u is not None and self.t is not None:
            for s, u, t in itertools.product(self.s, self.u, self.t):
                self._append_if_unique("a", (2.0 * (s - (u * t))) / (t**2))
            return self

        # Given s, v, t
        if self.s is not None and self.v is not None and self.t is not None:
            for s, v, t in itertools.product(self.s, self.v, self.t):
                self._append_if_unique("a", (2.0 * ((v * t) - s)) / (t**2))
            return self

        raise Exception("Cannot be solved with more than two unknowns!")

    def solve_for_t(self) -> Self:
        if self.t is not None:
            return self

        # Given s, u, v
        if self.s is not None and self.u is not None and self.v is not None:
            for s, u, v in itertools.product(self.s, self.u, self.v):
                self._append_if_unique("t", (2.0 * s) / (u + v))
            return self

        # Given s, u, a
        if self.s is not None and self.u is not None and self.a is not None:
            for s, u, a in itertools.product(self.s, self.u, self.a):
                self._append_if_unique("t", u / (s - (0.5 * a)))
            return self

        # Given u, v, a
        if self.u is not None and self.v is not None and self.a is not None:
            for u, v, a in itertools.product(self.u, self.v, self.a):
                if v - u == 0 and a == 0:
                    self._append_if_unique("t", 1.0)
                    continue
                self._append_if_unique("t", (v - u) / a)
            return self

        # Given s, v, a, the u generated in the formula will be positive
        if self.s is not None and self.v is not None and self.a is not None:
            self.t = []
            for s, v, a in itertools.product(self.s, self.v, self.a):
                top = v - math.sqrt((v**2) - (2.0 * a * s))
                if top == 0 and self.a == 0:
                    self._append_if_unique("t", 1.0)
                    continue
                self._append_if_unique("t", top / a)
            return self

        raise Exception("Cannot be solved with more than two unknowns!")
