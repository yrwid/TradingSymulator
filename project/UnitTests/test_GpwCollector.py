from app.GpwCollector import GpwCollector


def test_collect():
    gpwColl = GpwCollector()
    assert gpwColl.collect() == 1