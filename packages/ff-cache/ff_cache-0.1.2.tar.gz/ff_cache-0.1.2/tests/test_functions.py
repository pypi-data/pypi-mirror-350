from datetime import datetime, timedelta
from ff_cache.functions import ttl_from_result
from ff_cache.constant import DATETIME_FORMAT

class DataObject:
    pass

def test_ttl_from_result():
    dict_ttl = {"ttl": 10}
    assert ttl_from_result(result=dict_ttl) == dict_ttl["ttl"]

    dict_expires_in = {"expires_in": 20}
    assert ttl_from_result(result=dict_expires_in) == dict_expires_in["expires_in"]

    obj_ttl = DataObject()
    obj_ttl.ttl = 30
    assert ttl_from_result(result=obj_ttl) == obj_ttl.ttl

    obj_expires_in = DataObject()
    obj_expires_in.expires_in = 40
    assert ttl_from_result(result=obj_expires_in) == obj_expires_in.expires_in

    now = datetime.now()
    exipred_at = now + timedelta(seconds=10)
    dict_expired_at = {"expired_at": exipred_at}
    ttl = ttl_from_result(result=dict_expired_at)
    assert ttl <= 10 and ttl >= 9
    
    now = datetime.now()
    exipred_at = now + timedelta(seconds=10)
    dict_expired_at_str = {"expired_at": exipred_at.strftime(DATETIME_FORMAT)}
    ttl = ttl_from_result(result=dict_expired_at_str)
    assert ttl <= 10 and ttl >= 9

    now = datetime.now()
    exipred_at = now + timedelta(seconds=10)
    obj_expired_at = DataObject()
    obj_expired_at.expired_at = exipred_at
    ttl = ttl_from_result(result=obj_expired_at)
    assert ttl <= 10 and ttl >= 9

    now = datetime.now()
    exipred_at = now + timedelta(seconds=10)
    obj_expired_at_str = DataObject()
    obj_expired_at_str.expired_at = exipred_at.strftime(DATETIME_FORMAT)
    ttl = ttl_from_result(result=obj_expired_at_str)
    assert ttl <= 10 and ttl >= 9

    dict_invalidate_expired_at = {"expired_at": "test"}
    assert 0 == ttl_from_result(result=dict_invalidate_expired_at)
    
    invalidate_ttl_result = {}
    assert 0 == ttl_from_result(result=invalidate_ttl_result)