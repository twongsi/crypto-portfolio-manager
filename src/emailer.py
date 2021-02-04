from abc import ABC, abstractmethod

import boto3


class AbstractEmailer(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None:
        pass


class Emailer(AbstractEmailer):
    def send(self, to: str, subject: str, body: str) -> None:
        ses_client = boto3.client('ses')
        ses_client.send_email(
            Source=to,
            Destination={
                'ToAddresses': [to]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
