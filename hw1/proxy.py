import socket
import os


services = {
    "JSON": ("json_service", os.getenv("JSON_PORT")),
    "NATIVE": ("native_service", os.getenv("NATIVE_PORT")),
    "MSGPACK": ("msgpack_service", os.getenv("MSGPACK_PORT")),
    "AVRO": ("avro_service", os.getenv("AVRO_PORT")),
    "PROTO": ("proto_service", os.getenv("PROTO_PORT")),
    "XML": ("xml_service", os.getenv("XML_PORT")),
    "YML": ("yaml_service", os.getenv("YML_PORT")),
}

def handle_request(data, addr, conn):
    parts = data.split()
    print(parts, len(parts))
    if len(parts) not in [2, 3] or parts[0] != 'get_result' or parts[1] not in services:
        print("Seems like an error")
        conn.sendto("Invalid request to proxy server".encode(), addr)
        return

    service_address, service_port = services[parts[1]]
    service_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    parts_res = [parts[0]]
    if len(parts) > 2:
        parts_res += parts[2:]
    service_message = " ".join(parts_res)

    service_socket.sendto(service_message.encode("utf-8"), (service_address, int(service_port)))

    # Receive response from the internal service
    service_response, _ = service_socket.recvfrom(4096)
    service_socket.close()

    # Send the response back to the client
    conn.sendto(service_response, addr)
    print('sent response back to {}'.format(addr))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = os.getenv('SERVER_ADDR', '0.0.0.0')
server_port = int(os.getenv('PROXY_PORT', '8000'))


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


