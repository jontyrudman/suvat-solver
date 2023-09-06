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
                self._append_if_unique("u", math.sqrt((v**2) - 2.0 * a * s),
                    -1 * math.sqrt((v**2) - 2.0 * a * s),
)
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
                self._append_if_unique(
                    "v",
                    math.sqrt((u**2) + (2 * a * s)),
                    -1 * math.sqrt((u**2) + (2 * a * s)),
                )
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
                self._append_if_unique("t", top / a, -1 * top / a)
            return self

        raise Exception("Cannot be solved with more than two unknowns!")
