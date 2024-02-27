A multithreaded TCP server programmed in Python. A TCP persistent connection is utilized in the project to keep the connection alive with a timeout of 10 seconds. 

The repository contains main.py that acts as the server and then it contains other html pages and image that are objects passed to the client.

• How to compile code -  

o First, make sure index.html, page2.html, main.py, jpeg are all in the same folder.

o Next, open a terminal and locate the folder.

o Type “py main.py” and execute the main.py

o Once the port is ready, open a browser and type in http://localhost:8080/index.html and it should redirect to page2.html

o To check 404 http response, type a random page name to the same port and it should open a custom 404 page that is located in the main.py’s “send_404” function.


Screenshots of http response from wireshark -

![Screenshot 2024-02-26 205919](https://github.com/praisy16/Multithreaded-Web-Server-/assets/112771153/652a45ab-e53c-47fe-90cf-82bebfb55a15)


![Screenshot 2024-02-26 210117](https://github.com/praisy16/Multithreaded-Web-Server-/assets/112771153/feb3f14e-380c-4b79-bad7-b39c866ea3ce)


![Screenshot 2024-02-27 161135](https://github.com/praisy16/Multithreaded-Web-Server-/assets/112771153/e99db817-3dab-4171-b825-f7d3b35efb70)
