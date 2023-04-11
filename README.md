# 559W23-Project

Requirements to run this system:

Node Package Manager (npm)

Once on the client folder, a user can use the following command to install all the packages that the React app requires:
npm install

To start the Frontend application, type the following into the command line:
npm start

For the "server" folder, follow the following steps:
-Make sure to have python, and pip installed in your machine.

-A virtual environment was also created inside the 'server' folder, so users will need to create their own. Setting up an environment can be found here:
https://towardsdatascience.com/create-virtual-environment-using-virtualenv-and-add-it-to-jupyter-notebook-6e1bf4e03415


To activate the created virtual environment, type this command (For Windows PowerShell):
.\.<nameOfYourVirtualEnvironment>\Scripts\Activate.ps1

Once activated, you will notice the virtual environment name appears at the very left in the command line in a green font.

The server folder will also need its packages installed. This can be done with the following command:
python -m pip install -r requirements.txt

We can then type the following command to start the FastAPI server:
python main.py

To start the replica nodes and central node, change into the "rpc" directory and type the following:
python replica_node.py [Port#]

python central_node.py
