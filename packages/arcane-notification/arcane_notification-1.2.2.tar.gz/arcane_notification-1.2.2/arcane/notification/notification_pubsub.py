from datetime import datetime

from .types import Notification


def acknowledge_notification(notification_name: str, sender_service: str, pubsub_client, project, topic_name) -> None:
    """Acknowledges alert notification"""
    pubsub_client.push_to_topic(
        project=project,
        topic_name=topic_name,
        parameters=dict(sender_service=sender_service, notification_name=notification_name),
        await_response=True
    )


def post_notification(notification: Notification, pubsub_client, project, topic_name) -> None:
    """Creates alert notification"""
    message_parameters = notification.to_dict()
    if isinstance(message_parameters.get('end_date'), datetime):
        message_parameters['end_date'] = message_parameters['end_date'].strftime('%Y-%m-%dT%H:%M:%SZ')
    return pubsub_client.push_to_topic(
        project=project,
        topic_name=topic_name,
        parameters=message_parameters,
        await_response=True
    )
