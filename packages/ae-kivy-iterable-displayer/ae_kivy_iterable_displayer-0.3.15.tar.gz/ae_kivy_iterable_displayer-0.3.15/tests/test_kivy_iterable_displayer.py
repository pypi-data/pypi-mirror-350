""" unit tests """
from ae.kivy_iterable_displayer import IterableDisplayerPopup, KEY_VAL_SEPARATOR


def test_import():
    assert IterableDisplayerPopup


class TestIterableDisplayerPopup:
    def test_compile_child_maps_from_dict(self):
        idp = IterableDisplayerPopup
        child_maps = idp.compile_data_maps(dict(a="a", b="bb", c="ccc"))

        assert isinstance(child_maps, list)
        assert len(child_maps) == 3
        assert isinstance(child_maps[0], dict)
        assert 'cls' in child_maps[0]
        assert child_maps[0]['cls'] == 'IterableDisplayerLabel'
        assert 'attributes' in child_maps[0]
        assert isinstance(child_maps[0]['attributes'], dict)
        assert 'text' in child_maps[0]['attributes']
        assert child_maps[0]['attributes']['text'] == "a" + KEY_VAL_SEPARATOR + "a"

    def test_compile_child_maps_from_list(self):
        idp = IterableDisplayerPopup
        child_maps = idp.compile_data_maps(["a", "bb", "ccc"])

        assert isinstance(child_maps, list)
        assert len(child_maps) == 3
        assert isinstance(child_maps[0], dict)
        assert 'cls' in child_maps[0]
        assert child_maps[0]['cls'] == 'IterableDisplayerLabel'
        assert 'attributes' in child_maps[0]
        assert isinstance(child_maps[0]['attributes'], dict)
        assert 'text' in child_maps[0]['attributes']
        assert child_maps[0]['attributes']['text'] == "0" + KEY_VAL_SEPARATOR + "a"

    def test_compile_child_maps_from_set(self):
        idp = IterableDisplayerPopup
        tst_set = {"aas", "bbs", "ccs"}
        child_maps = idp.compile_data_maps(tst_set)

        assert isinstance(child_maps, list)
        assert len(child_maps) == 3
        assert isinstance(child_maps[0], dict)
        assert 'cls' in child_maps[0]
        assert child_maps[0]['cls'] == 'IterableDisplayerLabel'
        assert 'attributes' in child_maps[0]
        assert isinstance(child_maps[0]['attributes'], dict)
        assert 'text' in child_maps[0]['attributes']
        for idx, chi_map in enumerate(child_maps):      # set is unordered
            prefix = str(idx) + KEY_VAL_SEPARATOR
            assert child_maps[idx]['attributes']['text'].startswith(prefix)
            tst_set.remove(child_maps[idx]['attributes']['text'][len(prefix):])
        assert not tst_set

    def test_compile_child_maps_from_tuple(self):
        idp = IterableDisplayerPopup
        child_maps = idp.compile_data_maps(("a", "bb", "ccc"))

        assert isinstance(child_maps, list)
        assert len(child_maps) == 3
        assert isinstance(child_maps[0], dict)
        assert 'cls' in child_maps[0]
        assert child_maps[0]['cls'] == 'IterableDisplayerLabel'
        assert 'attributes' in child_maps[0]
        assert isinstance(child_maps[0]['attributes'], dict)
        assert 'text' in child_maps[0]['attributes']
        assert child_maps[0]['attributes']['text'] == "0" + KEY_VAL_SEPARATOR + "a"

    def test_compile_child_maps_from_complex_data_structure(self):
        idp = IterableDisplayerPopup
        child_maps = idp.compile_data_maps(("a", ["bb0", "bb1"], dict(c1="c", c2="cc")))

        assert isinstance(child_maps, list)
        assert len(child_maps) == 3
        assert isinstance(child_maps[0], dict)
        assert 'cls' in child_maps[0]
        assert child_maps[0]['cls'] == 'IterableDisplayerLabel'
        assert 'attributes' in child_maps[0]
        assert isinstance(child_maps[0]['attributes'], dict)
        assert 'text' in child_maps[0]['attributes']
        assert child_maps[0]['attributes']['text'] == "0" + KEY_VAL_SEPARATOR + "a"

        assert isinstance(child_maps[1], dict)
        assert 'cls' in child_maps[1]
        assert child_maps[1]['cls'] == 'IterableDisplayerButton'
        assert 'attributes' in child_maps[1]
        assert isinstance(child_maps[1]['attributes'], dict)
        assert 'text' in child_maps[1]['attributes']
        assert child_maps[1]['attributes']['text'] == "1" + KEY_VAL_SEPARATOR + "['bb0', 'bb1']"

        assert isinstance(child_maps[2], dict)
        assert 'cls' in child_maps[2]
        assert child_maps[2]['cls'] == 'IterableDisplayerButton'
        assert 'attributes' in child_maps[2]
        assert isinstance(child_maps[2]['attributes'], dict)
        assert 'text' in child_maps[2]['attributes']
        assert child_maps[2]['attributes']['text'] == "2" + KEY_VAL_SEPARATOR + "{'c1': 'c', 'c2': 'cc'}"

    def test_compile_child_maps_special_keys(self):
        idp = IterableDisplayerPopup
        child_maps = idp.compile_data_maps(dict(total_bytes=369))
        assert child_maps[0]['attributes']['text'] == "total_bytes" + KEY_VAL_SEPARATOR + "369"

        child_maps = idp.compile_data_maps(dict(total_bytes=1025))
        assert child_maps[0]['attributes']['text'].startswith("total_bytes" + KEY_VAL_SEPARATOR + "1025 (")
