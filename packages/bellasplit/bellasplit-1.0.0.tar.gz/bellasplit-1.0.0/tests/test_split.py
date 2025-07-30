import sqlite3

from bellameta import types as t

from bellasplit.base_split import SplitWriter

def test_data_source(data):
    assert set(data.labels).issubset(set([t.Subtype.DLBCL.to_string(), t.Subtype.FL.to_string()]))

def test_split(split):
    assert len(split.train) > len(split.test)
    assert len(split.test) > len(split.val)
    assert set(split.train).isdisjoint(set(split.test))
    assert set(split.val).isdisjoint(set(split.train))

def test_write(db, split):
    writer = SplitWriter(db=db, split=split)
    writer.write()
    assert set(split.source_data.hashes) == set(check_entries(db))


def check_entries(db):
    with sqlite3.connect(db.sqlite_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hash FROM split")
        data = cursor.fetchall()
        data = [d[0] for d in data]
    return data
