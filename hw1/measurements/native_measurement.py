import pickle
import timeit
from measurements.test_object import SerializationTestObject

def serialize_to_pickle(obj):
    return pickle.dumps(obj)

def deserialize_from_pickle(pickled_obj):
    return pickle.loads(pickled_obj)

def measure_serialization_pickle(obj, iterations=1000):
    avg_time = timeit.timeit(lambda: serialize_to_pickle(obj), number=iterations) / iterations * 1000 * 1000
    pickled = serialize_to_pickle(obj)
    size_of_pickled_object = len(pickled)  # размер в байтах
    return int(avg_time), size_of_pickled_object

def measure_deserialization_pickle(pickled_obj, iterations=1000):
    avg_time = timeit.timeit(lambda: deserialize_from_pickle(pickled_obj), number=iterations) / iterations * 1000 * 1000
    return int(avg_time)

def measure_pickle(iterations=1000, obj=SerializationTestObject()):
    serialization_time, size_of_serialized_object = measure_serialization_pickle(obj, iterations)
    # Сериализуем объект для десериализации
    serialized_object = serialize_to_pickle(obj)
    deserialization_time = measure_deserialization_pickle(serialized_object, iterations)
    return size_of_serialized_object, serialization_time, deserialization_time
