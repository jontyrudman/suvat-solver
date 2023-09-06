import itertools
import pytest

from suvatsolver import Suvat


class TestSuvat:
    # Solved suvat equations to test against the Suvat class
    test_data = [
        {
            "inputs": {
                "s": 5,
                "u": -9.5,
                "v": 10.5,
                "a": 2,
                "t": 10,
            },
            "valid_result": {
                "s": [5],
                "u": [-9.5, 9.5],
                "v": [10.5],
                "a": [2],
                "t": [10, 0.5],
            },
        }
    ]

    def test_constructor(self):
        """
        - Ensure that inputs end up as singletons containing floats.
        - Ensure that an exception is raised when invalid data is provided.
        """
        # Check type conversions
        suvat = Suvat(s=1, u=2, v=3)
        assert suvat.s is not None and isinstance(suvat.s[0], float)
        assert vars(suvat) == {"s": [1.0], "u": [2.0], "v": [3.0], "a": None, "t": None}

        # Check exceptions
        # Too many unknowns
        with pytest.raises(Exception):
            suvat = Suvat(s=1)

        # Acceleration mismatch
        with pytest.raises(Exception):
            suvat = Suvat(s=1, u=2, v=3, a=-1)

        # Zero/negative time
        with pytest.raises(Exception):
            suvat = Suvat(s=1, u=2, v=3, t=0)
        with pytest.raises(Exception):
            suvat = Suvat(s=1, u=2, v=3, t=-0)

        # Non-zero disp with zero vel
        with pytest.raises(Exception):
            suvat = Suvat(s=1, u=0, v=0)

    def test__append_if_unique(self):
        suvat = Suvat(u=1, v=1, a=1)
        assert suvat.s is None
        suvat._append_if_unique("s", 1)
        assert suvat.s == [1]
        suvat._append_if_unique("s", 2)
        assert suvat.s == [1, 2]
        suvat._append_if_unique("s", 1)
        assert suvat.s == [1, 2]

        with pytest.raises(ValueError):
            suvat._append_if_unique("g", 0)

    def test_unknowns(self):
        combos = itertools.permutations("suvat", 5)

        for c in combos:
            for i in range(5):
                given_variables = c[:i]
                unknown_variables = c[i:]
                if (i < 3):
                    with pytest.raises(Exception):
                        suvat = Suvat(
                            **{k: self.test_data[0]["inputs"][k] for k in given_variables}
                        )
                else:
                    suvat = Suvat(
                        **{k: self.test_data[0]["inputs"][k] for k in given_variables}
                    )
                    assert set(suvat.unknowns()) == set(unknown_variables)

    def test_solve_for_all(self):
        combos = itertools.combinations("suvat", 3)
        expected = self.test_data[0]["valid_result"]
        for c in combos:
            suvat = Suvat(**{k: self.test_data[0]["inputs"][k] for k in c})
            suvat.solve_for_all()
            for key in expected:
                solved = vars(suvat)
                assert set(solved[key]).issubset(set(expected[key]))
