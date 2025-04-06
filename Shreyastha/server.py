import socket
import threading
import json

# Server setup
HOST = '0.0.0.0'  # Accept connections from any IP
PORT = 5555
clients = []
auctions = {}  # {item_id: {'name': 'item', 'highest_bid': amount, 'bidder': 'user'}}

def broadcast(message):
    """Send updates to all clients."""
    for client in clients:
        try:
            client.sendall(json.dumps(message).encode())
        except:
            clients.remove(client)

def handle_client(client):
    """Handle communication with a client."""
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            request = json.loads(data)

            if request['type'] == 'new_item':
                item_id = len(auctions) + 1
                auctions[item_id] = {'name': request['name'], 'highest_bid': 0, 'bidder': None}
                broadcast({'type': 'update', 'auctions': auctions})

            elif request['type'] == 'bid':
                item_id = request['item_id']
                amount = request['amount']
                user = request['user']

                if item_id in auctions and amount > auctions[item_id]['highest_bid']:
                    auctions[item_id]['highest_bid'] = amount
                    auctions[item_id]['bidder'] = user
                    broadcast({'type': 'update', 'auctions': auctions})
                else:
                    client.sendall(json.dumps({'type': 'error', 'message': 'Bid too low'}).encode())

        except:
            break

    client.close()
    clients.remove(client)


def start_server():
    """Starts the auction server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        print(f"New connection: {addr}")
        clients.append(client)
        client.sendall(json.dumps({'type': 'update', 'auctions': auctions}).encode())
        threading.Thread(target=handle_client, args=(client,)).start()
  
start_server()