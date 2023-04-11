# 559W23-Project

Requirements to run this system:

Node Package Manager (npm)

Once on the client side, a user can use the following command to install all the packages that the React app requires:
npm install

To start the Frontend application, type the following into the command line:
npm start

For the "server" folder, follow the following steps:
-Make sure to have python, and pip installed in your machine.
-A virtual environment was also created inside the 'server' folder. Setting up an environment can be found here:
https://towardsdatascience.com/create-virtual-environment-using-virtualenv-and-add-it-to-jupyter-notebook-6e1bf4e03415

The virtual environment name created will appear as a folder. It appears as .venv in the image below:
![image](https://user-images.githubusercontent.com/47372279/231035415-0e6a0c1d-b1ae-4e24-a74c-b1a83991ed46.png)

To activate the created virtual environment, type this command (For Windows PowerShell):
.\.<nameOfYourVirtualEnvironment>\Scripts\Activate.ps1

Once activated, you will notice the virtual environment name in the command line appears in this green font:
![image](https://user-images.githubusercontent.com/47372279/231035848-11f85a5a-8753-422f-b08f-1f6f7eb3222c.png)

We can then type the following command to start the FastAPI server:
python main.py

To start the replica nodes and central node, change into the rpc directory and type the following:
python replica_node.py [Port#]

python central_node.py
