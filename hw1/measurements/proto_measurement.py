from measurements.test_object import SerializationTestObject
import timeit
import measurements.serialization_test_object_pb2 as serialization_test_object_pb2


def obj_to_protobuf(obj):
    protobuf_obj = serialization_test_object_pb2.SerializationTestObject()
    protobuf_obj.non_empty_string = obj.non_empty_string
    protobuf_obj.array.extend(obj.array)
    for key, value in obj.dictionary.items():
        protobuf_obj.dictionary[key] = value
    protobuf_obj.integer = obj.integer
    protobuf_obj.floating_point = obj.floating_point
    return protobuf_obj

def protobuf_to_obj(protobuf_obj):
    obj = SerializationTestObject()
    obj.non_empty_string = protobuf_obj.non_empty_string
    obj.array = list(protobuf_obj.array)
    obj.dictionary = dict(protobuf_obj.dictionary)
    obj.integer = protobuf_obj.integer
    obj.floating_point = protobuf_obj.floating_point
    return obj
def serialize_to_protobuf(obj):
    protobuf_obj = obj_to_protobuf(obj)
    return protobuf_obj.SerializeToString()

def deserialize_from_protobuf(protobuf_bytes):
    protobuf_obj = serialization_test_object_pb2.SerializationTestObject()
    protobuf_obj.ParseFromString(protobuf_bytes)
    return protobuf_to_obj(protobuf_obj)

def measure_protobuf(iterations=1000, obj=SerializationTestObject()):
    protobuf_bytes = serialize_to_protobuf(obj)
    size_in_bytes = len(protobuf_bytes)
    serialization_time = timeit.timeit(lambda: serialize_to_protobuf(obj), number=iterations) / iterations * 1000 * 1000
    deserialization_time = timeit.timeit(lambda: deserialize_from_protobuf(protobuf_bytes), number=iterations) / iterations * 1000 * 1000
    return int(size_in_bytes), int(serialization_time), int(deserialization_time)

