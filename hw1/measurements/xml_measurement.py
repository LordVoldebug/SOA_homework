from measurements.test_object import SerializationTestObject

import timeit
import dicttoxml
import xmltodict

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


def serialize_to_xml(obj):
    return dicttoxml.dicttoxml(obj_to_dict(obj))


def deserialize_from_xml(xml_string):
    return dict_to_obj(xmltodict.parse(xml_string)['root'])


def measure_xml(iterations=1000, obj=SerializationTestObject()):
    xml_string = serialize_to_xml(obj)
    size_in_bytes = len(xml_string)
    serialization_time = timeit.timeit(lambda: serialize_to_xml(obj), number=iterations) / iterations * 1000 * 1000
    deserialization_time = timeit.timeit(lambda: deserialize_from_xml(xml_string), number=iterations) / iterations * 1000 * 1000
    return int(size_in_bytes), int(serialization_time), int(deserialization_time)

