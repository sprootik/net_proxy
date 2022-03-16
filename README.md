## v1.0.0
![Logo](logo.png)   
   
An api implementation that allows web services to connect to network equipment via cli.

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
Ответ на команды:  
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
    'result': string ## строка с выполненными командами
    }
