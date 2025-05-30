import socket
import select
x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
x.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
l = ('127.0.0.1',8080)
x.bind(l)
x.listen(1)
print(f'listening on{l}')
while True:
        read_ready_sockets,_, _  = select.select(
            [x],
            [],
            [],
            0
        )
        if read_ready_sockets:
            for ready_socket in read_ready_sockets:
                client_socket, client_address = ready_socket.accept()
                client_msg = client_socket.recv(4096)
                print(f"Client said: {client_msg.decode('utf-8')}")
                client_socket.sendall(
                bytes(f"""HTTP/1.1 200 OK\r\nContent-type: text/html\r\nSet-Cookie: ServerName=Ryanesserver\r
                \r\n
                <!doctype html>
                <html>
                    <head/>
                    <body>
                        <h1>Welcome to Ryane's HTTP server!</h1>
                        <h2>Server address: {l[0]}:{l[1]}</h2>
                        <h3>You're connected through address: {client_address[0]}:{client_address[1]}</h3>
                        <body>
                            <pre>{client_msg.decode("utf-8")}<pre>
                        </body>
                    </body>
                </html>
                \r\n\r\n
                """, "utf-8")
            )
                try:
                    client_socket.close()
                except OSError:
                    pass