import pickle
import base64
from abc import ABC, abstractmethod


class Serializer(ABC):

    @abstractmethod
    def encode(self, obj):
        """
        编码
        """

    @abstractmethod
    def decode(self, encode_str):
        """
        解码
        """

class PickleSerializer(Serializer):

    def encode(self, obj):
        """
        编码
        """
        pickled_bytes = pickle.dumps(obj)
        encoded = base64.b64encode(pickled_bytes).decode('utf-8')
        return encoded
    
    def decode(self, encode_str):
        """
        解码
        """
        pickled_bytes = base64.b64decode(encode_str.encode('utf-8'))
        obj = pickle.loads(pickled_bytes)
        return obj