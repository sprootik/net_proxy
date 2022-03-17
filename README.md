Eng | [Rus](./README-ru.md)   

![](https://img.shields.io/badge/python-3.9-green) ![](https://img.shields.io/badge/python-3.10-green)

![Logo](logo.png)   
   
An api implementation that allows web services to connect to network equipment via cli. The Netmiko library is used to connect to the equipment. All hardware types supported by this library can be used.

***
## run without docker  
chmod +x net_proxy.py   
pip install -r requirements.txt  
#change configuration - ~/net_proxy/settings.cfg  
nohup ./net_proxy.py &

Or you can create a config file and run it as a daemon
***
 

## run in docker  
Create docker image:  
docker build -t net_proxy .  

Run docker:  
docker run -d -it -p [SERVER IP]:4444:4444/tcp --name net_proxy -v "$PWD"/logs:/app/logs -v "$PWD"/cfg:/app/cfg net_proxy:lates      
 
***

### Authentication
BasicAuth by login/password

***

### http codes
All responses with code 200.

***

### errors
Errors are returned in json, format:

    {
    'error': 'MESSAGE'
    }

### response to commands

    {
    'result': <DATA>
    }

***

net_send - execute commands from privileged mode.  
net_change - executing commands from configuration mode.  

POST request.  
JSON schema request

    {
        'type': 'object',
        'properties': {
            'host': {'type': 'string'},
            'port': {'type': 'number'},
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'devtype': {'type': 'string'},
            "commmands": {'type': 'array'}
        },
        'required': ['host', 'port', 'username', 'password', 'devtype']
    }
Response to commands:  
For net_send  

    {
    'result':
    [
    'COMMAND RESPONSE 1',
    'COMMAND RESPONSE 2',
    ...
    'COMMAND RESPONSE n'
    ]
    }
For net_change  

    {
    'result': string
    }

***

## request examples for cisco

    curl -u test:test --request POST --header 'Content-Type: application/json' --data '{"host": "192.168.0.1", "port": 22, "username": "cisco", "password": "cisco123", "devtype": "cisco_ios", "commmands": ["int lo123", "des test", "no int lo123"]}' 'http://127.0.0.1:4444/net_change'

    {"result":"configure terminal
    Enter configuration commands, one per line.  End with CNTL/Z.  
    R1(config)#int lo123
    R1(config-if)#des test
    R1(config-if)#no int lo123
    R1(config)#end
    R1#"}

    curl -u test:test --request POST --header 'Content-Type: application/json' --data '{"host": "192.168.0.1", "port": 22, "username": "cisco", "password": "cisco123", "devtype": "cisco_ios", "commmands": ["sh run | i username", "sh run | i aaa"]}' 'http://127.0.0.1:4444/net_send'

    {"result":[
        "username cisco privilege 15 password 0 cisco123",
        "no aaa new-model"
        ]}