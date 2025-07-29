import asyncio
from json import dumps
from datetime import datetime
from fastapi import Request
from tzlocal import get_localzone
from Osdental.ServicesBus.TaskQueue import task_queue
from Osdental.Handlers.Instances import environment, microservice_name, microservice_version
from Osdental.Shared.Constant import Constant

class CustomRequest:

    def __init__(self, request: Request):
        self.request = request
        self.local_tz = get_localzone()
        asyncio.create_task(self.send_to_service_bus())

    async def send_to_service_bus(self) -> None:
        message_in = await self.request.json()  
        message_json = {
            'idMessageLog': self.request.headers.get('Idmessagelog'),
            'type': Constant.RESPONSE_TYPE_REQUEST,
            'environment': environment,
            'dateExecution': datetime.now(self.local_tz).strftime('%Y-%m-%d %H:%M:%S'),
            'header': dumps(dict(self.request.headers)),
            'microServiceUrl': str(self.request.url),
            'microServiceName': microservice_name,
            'microServiceVersion': microservice_version,
            'serviceName': message_in.get('operationName'),
            'machineNameUser': self.request.headers.get('Machinenameuser'),
            'ipUser': self.request.headers.get('Ipuser'),
            'userName': self.request.headers.get('Username'),
            'localitation': self.request.headers.get('Localitation'),
            'httpMethod': self.request.method,
            'httpResponseCode': Constant.DEFAULT_EMPTY_VALUE,
            'messageIn': dumps(message_in) if isinstance(message_in, dict) else message_in,
            'messageOut': Constant.DEFAULT_EMPTY_VALUE,
            'errorProducer': Constant.DEFAULT_EMPTY_VALUE,
            'auditLog': Constant.MESSAGE_LOG_INTERNAL
        }
        asyncio.create_task(task_queue.enqueue(message_json))