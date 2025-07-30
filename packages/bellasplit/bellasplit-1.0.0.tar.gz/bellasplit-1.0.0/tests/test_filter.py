import pytest

from bellameta import types as t
    
def test_filter_cohort(subtyping):
    assert len(subtyping.filter(cohort=t.Cohort.Example)) == 100
    with pytest.raises(ValueError):
        subtyping.filter(cohort='made_up')

def test_filter_invalid(subtyping):
    with pytest.raises(ValueError):
        subtyping.filter(made_up_table='hello')