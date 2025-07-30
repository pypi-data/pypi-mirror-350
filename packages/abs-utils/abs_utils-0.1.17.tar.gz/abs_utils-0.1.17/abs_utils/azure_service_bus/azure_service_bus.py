from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json
from ..logger import setup_logger

logger = setup_logger(__name__)
class AzureServiceBus:
    def __init__(self, connection_string: str, queue_name: str):
        self.client = ServiceBusClient.from_connection_string(conn_str=connection_string)
        self.queue_name = queue_name

    async def send(self, event_payload: dict):
        """Send message to Azure Service Bus"""
        if not self.client or not self.queue_name:
            return

        try:
            sender = self.client.get_queue_sender(queue_name=self.queue_name)
            with sender:
                sender.send_messages(ServiceBusMessage(json.dumps(event_payload)))
        except Exception as e:
            logger.error(f"Failed to send message to Azure Service Bus: {e}") 