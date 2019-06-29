# master

This repo contains the code for the master system of the Human-firewall project.
The code was written using Python3.

The master makes an extensive use of the [slave system](https://github.com/humanfirewall-iot19/slave) (because a master is also a slave) and of the [bot subsystem](https://github.com/humanfirewall-iot19/bot).

## Features

The master system takes care of the following operations:
- Exposing its role over the LAN.
- Supporting disaster recovery of the slaves.
- Management of the ring event triggered by the slaves.
- Execution and management of the bot subsystem (used to notify users of a new "ring" event).
- Providing a message broker to implement a publish-subscribe architecture between slaves and bot.
- Supporting every feature already provided by the slave (image taking, face recognition etc).

## How to deploy 
For the deployment use the [master-scripts](https://github.com/humanfirewall-iot19/master-scripts).
The script will take care of installing all the needed dependencies and executing the master in a correct manner.

## Dependencies

For the full list of dependencies refer to the [requirements file](requirements.txt)
