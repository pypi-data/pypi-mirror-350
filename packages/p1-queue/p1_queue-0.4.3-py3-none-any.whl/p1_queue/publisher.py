# -*- coding: utf-8 -*-

from __future__ import absolute_import
from builtins import object
import os
import logging
import json

from google.cloud import pubsub_v1
from google.pubsub_v1.types.pubsub import PublishRequest
from google.pubsub_v1.types.pubsub import PubsubMessage

LOGGER = logging.getLogger(__name__)


class Publisher(object):
    topic_name = None

    def __init__(self, topic_id):
        self.instance = pubsub_v1.PublisherClient()
        self.topic_name = 'projects/{project_id}/topics/{topic}'.format(
            project_id=os.getenv('PUBSUB_PUBLISHER_PROJECT_ID'),
            topic=topic_id,
        )

    def publish(self, body, raise_exception=False, retry_connection=0, timeout=120, **kwargs):
        LOGGER.info('Publishing message %s, %s', body, kwargs)
        future = self.instance.publish(topic=self.topic_name, data=json.dumps(body).encode('utf-8'),  **kwargs)

        try:
            future.result(timeout)
        except Exception as e:
            LOGGER.warning('Message not published')

            if retry_connection > 0:
                self.publish(body, raise_exception, retry_connection - 1, timeout,  **kwargs)
            else:
                if raise_exception:
                    raise e
