import msgpack
import timeit

class SerializationTestObject:
    def __init__(self):
        self.string = "Hello, world!"
        self.array = [1, 2, 3, "four", "five", 6.0]
        self.dictionary = {"key1": "value1", "key2": 2, "key3": 3.0}
        self.integer = 42
        self.floating_point = 3.14159

def obj_to_dict(obj):
    return obj.__dict__

def dict_to_obj(d):
    obj = SerializationTestObject()
    obj.__dict__.update(d)
    return obj

def serialize_to_msgpack(obj):
    return msgpack.packb(obj_to_dict(obj), use_bin_type=True)

def deserialize_from_msgpack(msgpack_bytes):
    return dict_to_obj(msgpack.unpackb(msgpack_bytes, raw=False))

def measure_msgpack(iterations=1000, obj=SerializationTestObject()):
    msgpack_bytes = serialize_to_msgpack(obj)
    size_in_bytes = len(msgpack_bytes) # MessagePack already produces bytes, so we can directly measure the length
    serialization_time = timeit.timeit(lambda: serialize_to_msgpack(obj), number=iterations) / iterations * 1000 * 1000
    deserialization_time = timeit.timeit(lambda: deserialize_from_msgpack(msgpack_bytes), number=iterations) / iterations * 1000 * 1000
    return int(size_in_bytes), int(serialization_time), int(deserialization_time)
