# Tcp Chat server

import socket, select

CLR_BLACK=u"\u001b[30m"
CLR_RED=u"\u001b[31m"
CLR_GREEN=u"\u001b[32m"
CLR_YELLOW=u"\u001b[33m"
CLR_BLUE=u"\u001b[34m"
CLR_MAGENTA=u"\u001b[35m"
CLR_CYAN=u"\u001b[36m"
CLR_WHITE=u"\u001b[37m"
CTRL_RESET=u"\u001b[0m"

# Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
  #Do not send the message to master socket and the client who has send us the message
  for socket in CONNECTION_LIST:
    if socket != server_socket and socket != sock :
      try :
        socket.send(message)
      except :
        # broken socket connection may be, chat client pressed ctrl+c for example
        socket.close()
        CONNECTION_LIST.remove(socket)

if __name__ == "__main__":

  # List to keep track of socket descriptors
  CONNECTION_LIST = []
  RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
  PORT = 5000

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # this has no effect, why ?
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(("127.0.0.1", PORT))
  server_socket.listen(10)

  # Add server socket to the list of readable connections
  CONNECTION_LIST.append(server_socket)

  print("SERVER STARTED @ PORT " + str(PORT))

  while 1:
    # Get the list sockets which are ready to be read through select
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

    for sock in read_sockets:
      # New connection
      if sock == server_socket:
        # Handle the case in which there is a new connection recieved through server_socket
        sockfd, addr = server_socket.accept()
        CONNECTION_LIST.append(sockfd)
        print ("CLIENT (%s, %s) CONNECTED" % addr)
        broadcast_data(sockfd, "--- [%s:%s] ENTERED THE ROOM\n" % addr)

      # Some incoming message from a client
      else:
        # Data recieved from client, process it
        try:
          #In Windows, sometimes when a TCP program closes abruptly,
          # a "Connection reset by peer" exception will be thrown
          data = sock.recv(RECV_BUFFER)
          if data:
            broadcast_data(sock, "\r" + CLR_GREEN + str(sock.getpeername()[0]) + "> " + CTRL_RESET + data)

        except:
          broadcast_data(sock, "CLIENT (%s, %s) IS OFFLINE" % addr)
          print ("CLIENT (%s, %s) IS OFFLIN " % addr)
          sock.close()
          CONNECTION_LIST.remove(sock)
          continue

  server_socket.close()
