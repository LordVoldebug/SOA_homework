from measurements.test_object import SerializationTestObject
import yaml
import timeit

def obj_to_dict(obj):
    return obj.__dict__

def dict_to_obj(d):
    obj = SerializationTestObject()
    obj.__dict__.update(d)
    return obj

def serialize_to_yaml(obj):
    return yaml.dump(obj_to_dict(obj))

def deserialize_from_yaml(yaml_string):
    return dict_to_obj(yaml.safe_load(yaml_string))

def measure_yaml(iterations=1000, obj=SerializationTestObject()):
    yaml_string = serialize_to_yaml(obj)
    size_in_bytes = len(yaml_string.encode('utf-8')) # YAML is a string, so we have to encode it to bytes to get the size
    serialization_time = timeit.timeit(lambda: serialize_to_yaml(obj), number=iterations) / iterations * 1000 * 1000
    deserialization_time = timeit.timeit(lambda: deserialize_from_yaml(yaml_string), number=iterations) / iterations * 1000 * 1000
    return int(size_in_bytes), int(serialization_time), int(deserialization_time)
