#Intergration with the PI

DOWNLOAD Apache2, there are tutorial online. When you finish downloading, you should be able to access a local web app w/ http://localhost or http://<IP-ADDRESS>

DOWNLOAD dist/store on Raspberry pi, put the information into a folder called my-app
Use command sudo cp ~/my-app/* /var/www/html/ to copy app web information into apache2 server folder.
This should change the web app display, and display our Turn ON/OFF server.