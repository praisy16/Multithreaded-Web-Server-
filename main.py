# http://localhost:8080/index.html
# Praisy Daniel
# 1001941360

from socket import *
from _thread import start_new_thread


#custom 404 page - creates a custom 404 page and sends it to the server when -
# a request resource is not found
def send_404(connectionSocket):
    
    #html 404 body
    html_body = "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1><p>The page you requested does not exist.</p></body></html>"
   
    #initialize http response with 404 code 
    http_response = "HTTP/1.0 404 Not Found\nContent-Type: text/html\n"
    http_response += f"Content-Length: {len(html_body)}\n\n"
    
    # Send the 404 response
    connectionSocket.sendall(http_response.encode() + html_body.encode())



#server function - serves the client with objects. First, the function keeps the connection alive -
# and then it takes the file path and breaks down any unncessary params in the link
# then the appropriate objects are passed to the client followed by a 202 code
# a timeout is set for 10 seconds, then the connection is closed.
def tcp_server(connectionSocket):
    
    #boolean to track the persistent connection 
    connectionAlive = True
   
    #while the connection is alive, serve the client 
    while connectionAlive:
        try:
            
            #get message from client 
            message = connectionSocket.recv(1024).decode()
            
            #if no message then break the loop
            if not message:
                break

            print(message)

            connectionAlive = "Connection: keep-alive" in message

            #send 404 error if path is incorrect format 
            tokens = message.split(' ')
            if len(tokens) < 2:
                send_404(connectionSocket)
                break

            #get the second element aka file path from request 
            path = tokens[1]
            filePath = path.strip('/')

            # 301 Moved Permanently: Redirect from index.html to page2.html
            if filePath == 'index.html':
                http_response = 'HTTP/1.0 301 Moved Permanently\nLocation: http://localhost:8080/page2.html\n\n'
                connectionSocket.send(http_response.encode())
                continue

            # Determine content type based on file extension
            contentType = 'application/octet-stream'
            if filePath.endswith('.jpg') or filePath.endswith('.jpeg'):
                contentType = 'image/jpeg'
            elif filePath.endswith('.html'):
                contentType = 'text/html'

            # filter out query param like '?q=python&page=1' etc. from original file path
            cleanpath = filePath.split('?')[0]  
            if '_xsrf=' in cleanpath or '\r' in cleanpath or '\n' in cleanpath:
                send_404(connectionSocket)
                continue

            try:
                #read requested content 
                with open(cleanpath, 'rb') as file:
                    content = file.read()

                http_response = f'HTTP/1.0 200 OK\nContent-Type: {contentType}\nContent-Length: {len(content)}\n'
                http_response += "Connection: keep-alive\n\n" if connectionAlive else "\n"
                connectionSocket.sendall(http_response.encode() + content)

            #call on send_404 function if no file is found
            except FileNotFoundError:
                send_404(connectionSocket)

            # timeout after 10 secs if connections remains alive 
            if connectionAlive:
                connectionSocket.settimeout(10.0)  

        #handle time out 
        except timeout:
            print("Connection timed out")
            break
        
        #handle any other exceptions 
        except Exception as e:
            print(f"Error: {e}")
            break

    #close connection and end thread
    connectionSocket.close()
    print("Connection closed.")



# main function - passes the port number and binds it with the local ip address
# then the connection is accepted and it runs in a loop unti an error is encountered
def main():
    serverPort = 8080
    
    #create a TCP connection 
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', serverPort))
  
    #start listening with 2 queued connections 
    serverSocket.listen(2)
    print("The server is ready to receive")

    while True:
        
        #accept the connection
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection accepted from {addr}")
        
        #handle client in a new thread 
        start_new_thread(tcp_server, (connectionSocket,))


if __name__ == "__main__":
    main()
