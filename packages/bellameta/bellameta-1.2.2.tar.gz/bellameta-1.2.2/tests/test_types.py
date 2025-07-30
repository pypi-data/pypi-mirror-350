import os

import pamly

from bellameta.types import Cohort, Task, Subtype, Stain, BellametaType

def test_cohort():
    assert Cohort.list() == ['Example']

def test_task():
    assert Task.list() == ['Subtyping']
    print(Task.Subtyping.to_label_table_name())

def test_subtype():
    assert Subtype.list() == [pamly.Diagnosis.from_int(i).to_string() for i in range(len(pamly.Diagnosis.list()))]

def test_stain():
    # TODO: there seems to be a bug in pamly as pamly.Stain.from_int(i) throws an error for i>1
    # assert Stain.list() == [pamly.Stain.from_int(i).to_string() for i in range(len(pamly.Stain.list()))]
    assert Stain.list() == [v.to_string() for v in pamly.Stain.list()]