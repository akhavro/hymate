# hymate
Hymate GmbH coding challenge

**NOTE:** Every command to be run in this tutorial should be run from respective [PROJECT] folder.


# PROJECT: Energy Management System
This was written with **Django**. The database is a simple **SQLite3**, enough for the purpose.


## Installation/Execution:
You can either install the app on your local machine, using a Virtual Environment, or run it from a Docker container.


### Locally (RECOMMENDED)

**Requirements:** Python 3

1 - Clone the git repository to your local machine

2 - Set-up a virtual environment for the project and make sure it is active

3 - From `energy_management_system` folder run:
`pip install -r requirements.txt`

4 - Run `python manage.py runserver` or `python manage.py runserver {PORT}` if you wish to run it on a different port (default=8000).

5 - Access the printed url from a browser to make sure it is working.


### Docker

**Requirements:** Docker

1 - Clone the git repository to your local machine

2 - From `energy_management_system` folder run:

`docker build -t app .` and after it build the image `docker run -p 3000:3000 app`

3 - Access `localhost:3000` from a browser to make sure it is working.


## How to use?

There are two steps in using the app which are described below:
### 1 - Setting up the simulation environment
The system is composed by the following objects:

- Producer

- Consumer

- Grid Access

- Storage

To be able to run the simulation we need to create at least one of these.
There is **already one created**, but you can create a different one if you wish.

1.1 - Go to `localhost:<port>/admin` from your browser

1.2 - The login details are admin:admin being user:password (very secure :D)

1.3 - On the left side click on `Consumers>Add` and you can create a new consumer along with the other objects related to it.


**NOTE:** Although the admin UI lets you add several batteries and storages to a Consumer you should only add one, 
because only one is then used by the algorithm. You can always change the Storage capacity by changing the objects that is already
created. The decision of a many-to-many relationship between these objects was made with the goal of added flexibility, that is
in case sometime we would want to add several devices of the same type to a Consumer.


### 2 - Running the simulation
**Note:** Running the simulation is easier if doing so from a local installation. We need to move around files and to run commands.
You can do it on Docker, but you'd need to ssh to the container to retrieve files and to run commands.

We need to input a file (in.csv) containing the rows: *pv_yield_power* and *household_consumption*, containing the information regarding energy produced and energy consumed, respectively. This file will be used as a model for the new file (out.csv), meaning that for each row another 3 columns are going to be added: *grid*, *storage* and *storage_current_level*, respectively meaning "power to/from Grid", "power to/from Storage" and "current amount of energy in Storage".

1 - Copy your in.csv file to `energy_management_system` folder (the file should be located along manage.py)

2 - Run `python manage.py runsimulation <consumer_id>`. The *consumer_id* is the ID of the consumer you want to run the simulation against.

3 - An output file (out.csv) is created in the same folder, you can now check it and adjust your environment values in the `/admin` page as needed.

**Meaning of the values:** the values in *grid* and *storage* are:
- **positive** if our Consumer is consuming energy from these sources
- **negative** when our system is sending excessive energy to these sources


### Extra - Testing
If you wish to run the automated tests, run: `python manage.py test`


## Architecture
The core of the decision process regarding "where the energy should go" or "where the energy should come from" is defined in the *hygorithm* method, located at `core/hygorithm.py` file. The logic there is more or less what can be seen in the following diagram which represents an approximation of the energy flow, controlled by the app. The modules *PowerP*, *PowerC* and *PowerStorage* were not implemented in this project, but these would be responsible for managing several Producers, Consumers and Storages at the same time. Since in our case we only have one of each, the said modules were ignored.

The energy can come either from Producers, from Storage or from Grid. While Producers never receive energy, the Storage and Grid may, in certain circumstances, such as:

- Producers are producing in excess:
    - The batteries will receive energy until the capacity is reached
    - Grid will receive energy if batteries are full

![Screenshot](/energy_management_system/docs/hymate_1.png)