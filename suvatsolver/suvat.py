import math
from pydantic import validate_call
from dataclasses import dataclass, asdict
from typing import Self


@validate_call
@dataclass
class Suvat:
    s: float | None = None
    u: float | None = None
    v: float | None = None
    a: float | None = None
    t: float | None = None

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
            self.s = 0
            return self

        # Given u, a, t
        if self.u is not None and self.a is not None and self.t is not None:
            self.s = (self.u * self.t) + (0.5 * self.a * (self.t**2))
            return self

        # Given u, v, t
        if self.u is not None and self.v is not None and self.t is not None:
            self.s = 0.5 * self.t * (self.u + self.v)
            return self

        # Given v, a, t
        if self.v is not None and self.a is not None and self.t is not None:
            self.s = (self.v * self.t) - (0.5 * self.a * (self.t**2))
            return self

        # Given u, v, a
        if self.u is not None and self.v is not None and self.a is not None:
            self.s = ((self.v**2) - (self.u**2)) / (2.0 * self.a)
            return self

        raise Exception("Cannot be solved with more than two unknowns!")

    def solve_for_u(self) -> Self:
        if self.u is not None:
            return self

        if self.t == 0:
            self.u = 0
            return self

        # Given v, a, t
        if self.v is not None and self.a is not None and self.t is not None:
            self.u = self.v - (self.a * self.t)
            return self

        # Given s, v, t
        if self.s is not None and self.v is not None and self.t is not None:
            self.u = ((2.0 * self.s) / self.t) - self.v
            return self

        # Given s, v, a
        if self.s is not None and self.v is not None and self.a is not None:
            self.u = math.sqrt((self.v**2) - 2.0 * self.a * self.s)
            return self

        # Given s, a, t
        if self.s is not None and self.a is not None and self.t is not None:
            self.u = (self.s / self.t) - 0.5 * self.a * self.t
            return self

        raise Exception("Cannot be solved with more than two unknowns!")

    def solve_for_v(self) -> Self:
        if self.v is not None:
            return self

        if self.t == 0:
            self.v = 0
            return self

        # Given u, a, t
        if self.u is not None and self.a is not None and self.t is not None:
            self.v = self.u + (self.a * self.t)
            return self

        # Given s, u, a
        if self.s is not None and self.u is not None and self.a is not None:
            self.v = math.sqrt((self.u**2) + (2 * self.a * self.s))
            return self

        # Given s, a, t
        if self.s is not None and self.a is not None and self.t is not None:
            self.v = (self.s / self.t) + (0.5 * self.a * self.t)
            return self

        # Given s, u, t
        if self.s is not None and self.u is not None and self.t is not None:
            self.v = ((2 * self.s) / self.t) - self.u
            return self

        raise Exception("Cannot be solved with more than two unknowns!")

    def solve_for_a(self) -> Self:
        if self.a is not None:
            return self

        if self.t == 0:
            self.a = 0
            return self

        # Given u, v, t
        if self.u is not None and self.v is not None and self.t is not None:
            self.a = (self.v - self.u) / self.t
            return self

        # Given s, u, v
        if self.s is not None and self.u is not None and self.v is not None:
            self.a = ((self.v**2) - (self.u**2)) / (2.0 * self.s)
            return self

        # Given s, u, t
        if self.s is not None and self.u is not None and self.t is not None:
            self.a = (2.0 * (self.s - (self.u * self.t))) / (self.t**2)
            return self

        # Given s, v, t
        if self.s is not None and self.v is not None and self.t is not None:
            self.a = (2.0 * ((self.v * self.t) - self.s)) / (self.t**2)
            return self

        raise Exception("Cannot be solved with more than two unknowns!")

    def solve_for_t(self) -> Self:
        if self.t is not None:
            return self

        # Given u, v, s
        if self.s is not None and self.u is not None and self.v is not None:
            self.t = (2.0 * self.s) / (self.u + self.v)
            return self

        # Given s, u, a
        if self.s is not None and self.u is not None and self.a is not None:
            self.t = self.u / (self.s - (0.5 * self.a))
            return self

        # Given u, v, a
        if self.u is not None and self.v is not None and self.a is not None:
            if self.v - self.u == 0 and self.a == 0:
                self.t = 1.0
                return self
            self.t = (self.v - self.u) / self.a
            return self

        # Given s, v, a
        if self.s is not None and self.v is not None and self.a is not None:
            top = self.v - math.sqrt((self.v**2) - (2.0 * self.a * self.s))
            if top == 0 and self.a == 0:
                self.t = 1.0
                return self
            self.t = top / self.a
            return self

        raise Exception("Cannot be solved with more than two unknowns!")
