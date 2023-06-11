import socket
import sys
import os
import measurements.json_measurement
import measurements.native_measurement
import measurements.xml_measurement
import measurements.yaml_measurement
import measurements.msgpack_measurement
import measurements.proto_measurement
import measurements.avro_measurement


def transfrom_function(function, name):
    def res_function(*args, **kwargs):
        res = function(*args, **kwargs)
        return f"{name} - {res[0]} - {res[1]} mcs - {res[2]} mcs"
    return res_function


def output_format(functions):
    res = {}
    for f in functions:
        res[f] = transfrom_function(functions[f], f)
    return res


FUNCTIONS = {"JSON": measurements.json_measurement.measure_json,
             "NATIVE": measurements.native_measurement.measure_pickle,
             "XML": measurements.xml_measurement.measure_xml,
             "YAML": measurements.yaml_measurement.measure_yaml,
             "MSGPACK": measurements.msgpack_measurement.measure_msgpack,
             "PROTO": measurements.proto_measurement.measure_protobuf,
             "AVRO": measurements.avro_measurement.measure_avro}
FUNCTIONS = output_format(FUNCTIONS)


def handle_request(data, addr, conn):
    parts = data.split()
    if len(parts) not in [1, 2] or parts[0] != 'get_result' or (len(parts) == 2 and not parts[1].isdigit()) or (len(parts) == 2 and int(parts[1]) < 0):
        conn.sendto("Invalid request format".encode(), addr)
        return
    if len(parts) == 1:
        function_to_execute = FUNCTIONS.get(FORMAT, None)
        if function_to_execute is None:
            conn.sendto(f"Error: function {FORMAT} not found in FUNCTIONS dict".encode(), addr)
            return
        result = function_to_execute()
    else:
        function_to_execute = FUNCTIONS.get(FORMAT, None)
        if function_to_execute is None:
            conn.sendto(f"Error: function {FORMAT} not found in FUNCTIONS dict".encode(), addr)
            return
        result = function_to_execute(int(parts[1]))
    conn.sendto(str(result).encode(), addr)

FORMAT = sys.argv[1].upper()
if FORMAT not in FUNCTIONS:
    print(f"Error: {FORMAT} not found in FUNCTIONS dict")
    sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = os.getenv('SERVER_ADDR', '0.0.0.0')
server_port = int(os.getenv('SERVER_PORT', '8000'))

server_addr_port = (server_address, server_port)
print(f"starting up on {server_addr_port[0]} port {server_addr_port[1]}")
sock.bind(server_addr_port)

while True:

    print("\nwaiting to receive message")
    data, addr = sock.recvfrom(4096)
    data = data.decode()

    print(f"received {len(data)} bytes from {addr}")
    print(data)

    handle_request(data, addr, sock)
