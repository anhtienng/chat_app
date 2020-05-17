import Client
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client = Client.Client(client_socket)
client.Run()
