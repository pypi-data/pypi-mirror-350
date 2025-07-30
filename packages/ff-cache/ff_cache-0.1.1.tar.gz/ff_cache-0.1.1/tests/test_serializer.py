from ff_cache.serializer import PickleSerializer


serializer = PickleSerializer()

def test_serialize_build_in_types():
    _int = 1
    _int_str = serializer.encode(_int)
    _int_decode = serializer.decode(_int_str)
    assert _int == _int_decode

    _float = 3.1415926
    _float_str = serializer.encode(_float)
    _float_decode = serializer.decode(_float_str)
    assert _float == _float_decode

    _str = "ff-cache"
    _str_str = serializer.encode(_str)
    _str_decode = serializer.decode(_str_str)
    assert _str == _str_decode

    _list = ["1", 2]
    _list_str = serializer.encode(_list)
    _list_decode = serializer.decode(_list_str)
    assert _list == _list_decode

    _tuple = (1, "2")
    _tuple_str = serializer.encode(_tuple)
    _tuple_decode = serializer.decode(_tuple_str)
    assert _tuple == _tuple_decode

    _dict = {"a": "a", "b": "b"}
    _dict_str = serializer.encode(_dict)
    _dict_decode = serializer.decode(_dict_str)
    assert _dict == _dict_decode


class DataObject:

    def __init__(self, a: str, b: str):
        self.a = a
        self.b = b

def test_serialize_custom_type():
    _obj = DataObject(a="test_a", b="test_b")
    _obj_str = serializer.encode(_obj)
    _obj_decode = serializer.decode(_obj_str)
    # assert _obj == _obj_decode
    assert isinstance(_obj_decode, DataObject)
    assert _obj_decode.a == "test_a"
    assert _obj_decode.b == "test_b"