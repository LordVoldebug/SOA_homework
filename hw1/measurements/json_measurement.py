import json
import timeit
from measurements.test_object import SerializationTestObject
def serialize_to_json(obj):
    return json.dumps(obj.__dict__)

def deserialize_from_json(json_str):
    return json.loads(json_str)

def measure_serialization(obj, iterations=1000):
    avg_time = timeit.timeit(lambda: serialize_to_json(obj), number=iterations) / iterations * 1000 * 1000
    serialized = serialize_to_json(obj)
    size_of_serialized_object = len(serialized.encode('utf-8'))  # размер в байтах
    return int(avg_time * 1000), size_of_serialized_object

def measure_deserialization(serialized_obj, iterations=1000):
    avg_time = timeit.timeit(lambda: deserialize_from_json(serialized_obj), number=iterations) / iterations * 1000 * 1000
    return int(avg_time * 1000)

def measure_json(iterations=1000, obj=SerializationTestObject()):
    serialization_time, size_of_serialized_object = measure_serialization(obj, iterations)
    # Сериализуем объект для десериализации
    serialized_object = serialize_to_json(obj)
    deserialization_time = measure_deserialization(serialized_object, iterations)
    return size_of_serialized_object, serialization_time, deserialization_time
