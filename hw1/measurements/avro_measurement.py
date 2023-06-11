from measurements.test_object import SerializationTestObject
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
import timeit
import io

SCHEMA = avro.schema.parse("""
{
    "namespace": "example.avro",
    "type": "record",
    "name": "SerializationTestObject",
    "fields": [
        {"name": "non_empty_string", "type": "string"},
        {"name": "array",  "type": {"type": "array", "items": "int"}},
        {"name": "dictionary", "type": {
            "type": "map", 
            "values": "int"
            }
        },
        {"name": "integer", "type": "int"},
        {"name": "floating_point", "type": "float"}
    ]
}
""")

def serialize_to_avro(obj):
    writer = avro.io.DatumWriter(SCHEMA)
    bytes_writer = io.BytesIO()
    df_writer = DataFileWriter(bytes_writer, writer, SCHEMA)
    df_writer.append(obj.__dict__)
    df_writer.flush()
    return bytes_writer.getvalue()

def deserialize_from_avro(avro_bytes):
    bytes_reader = io.BytesIO(avro_bytes)
    df_reader = DataFileReader(bytes_reader, avro.io.DatumReader())
    for obj in df_reader:
        sto = SerializationTestObject()
        sto.__dict__.update(obj)
        return sto
    return None

def measure_avro(iterations=1000, obj=SerializationTestObject()):
    # Measure serialization
    serialization_time = timeit.timeit(lambda: serialize_to_avro(obj), number=iterations) / iterations * 1000 * 1000
    avro_bytes = serialize_to_avro(obj)

    # Measure deserialization
    deserialization_time = timeit.timeit(lambda: deserialize_from_avro(avro_bytes), number=iterations) / iterations * 1000 * 1000

    return len(avro_bytes), int(serialization_time), int(deserialization_time)
