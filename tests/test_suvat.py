from dataclasses import asdict
import itertools
import pytest

from suvatsolver import Suvat


class TestSuvat:
    # Solved suvat equations to test against the Suvat class
    valid_test_data = [
        {
            "s": [5],
            "u": [-9.5, 9.5],
            "v": [10.5, -10.5],
            "a": [2],
            "t": [10, -0.5],
        }
    ]

    def test__append_if_unique(self):
        suvat = Suvat()
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
                suvat = Suvat(
                    **{k: self.valid_test_data[0][k] for k in given_variables}
                )
                assert set(suvat.unknowns()) == set(unknown_variables)


    def test_solvable(self):
        for i in range(5):
            combos = itertools.combinations("suvat", i)
            for c in combos:
                given_variables = c[:i]
                suvat = Suvat(
                    **{k: self.valid_test_data[0][k] for k in given_variables}
                )

                # Not enough knowns
                if (i < 3):
                    assert suvat.solvable() == False
                else:
                    assert suvat.solvable() == True


    def test_solve_for_all(self):
        combos = itertools.combinations("suvat", 3)
        expected = self.valid_test_data[0]
        for c in combos:
            suvat = Suvat(
                **{k: [expected[k][0]] for k in c}
            )
            suvat.solve_for_all()
            print(c, asdict(suvat))
            for key in expected:
                solved = asdict(suvat)
                for possibility_index in range(len(solved[key])):
                    assert solved[key][possibility_index] == expected[key][possibility_index]
