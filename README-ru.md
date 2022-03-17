Rus | [Eng](./README.md)  

![](https://img.shields.io/badge/python-3.9-green) ![](https://img.shields.io/badge/python-3.10-green)

![Logo](logo.png)   

Реализация API, которая позволяет веб-сервисам подключаться к сетевому оборудованию через cli. Для подключения к оборудованию используется библиотека Netmiko. Можно использовать все типы оборудования, поддерживаемые этой библиотекой. 

***
## запуск без docker  
chmod +x net_proxy.py   
pip install -r requirements.txt  
#изменить конфигурацию - ~/net_proxy/settings.cfg  
nohup ./net_proxy.py &

Или вы можете создать файл конфигурации и запустить его как демон.
***
 

## запуск в docker  
Создать docker image:  
docker build -t net_proxy .  

Запустить docker контейнер:  
docker run -d -it -p [SERVER IP]:4444:4444/tcp --name net_proxy -v "$PWD"/logs:/app/logs -v "$PWD"/cfg:/app/cfg net_proxy:lates      
 
***

### Аутентификация
BasicAuth по логину/паролю

***

### http codes
Все ответы с кодом 200.

***

### errors
Ошибки возвращаются в json формате:

    {
    'error': 'MESSAGE'
    }

### ответ на команды

    {
    'result': <DATA>
    }

***

net_send - команды, выполняемые из привилегированного режима.  
net_change - команды выполняемые из режима конфигурации.  

POST запрос.  
JSON schema запроса

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
Для net_send  

    {
    'result':
    [
    'COMMAND RESPONSE 1',
    'COMMAND RESPONSE 2',
    ...
    'COMMAND RESPONSE n'
    ]
    }
Для net_change  

    {
    'result': string
    }

***

## примеры запросов для маршрутизатора cisco

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