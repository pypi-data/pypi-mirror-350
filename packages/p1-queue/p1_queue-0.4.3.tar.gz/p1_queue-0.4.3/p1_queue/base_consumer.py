# -*- coding: utf-8 -*-

from __future__ import absolute_import
from builtins import str
from builtins import object
import logging
import os
import json
import signal
import tornado.ioloop

from google.cloud import pubsub_v1

LOGGER = logging.getLogger(__name__)


class BaseConsumer(object):
    TOPIC_ID = None
    subscription_name = None
    is_running = False
    loop = None

    def __init__(self):
        self._stopping = False
        self.subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
            project_id=os.getenv('PUBSUB_SUBSCRIBER_PROJECT_ID'),
            sub=self.TOPIC_ID
        )
        self.instance = pubsub_v1.SubscriberClient()
        self.loop = tornado.ioloop.IOLoop.current()
        
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGINT, self._handle_sigterm)

    def _handle_sigterm(self, signum, frame):
        LOGGER.info('Received signal %s. Initiating graceful shutdown...', signum)
        self._stopping = True
        self.loop.add_callback(self.stop)

    def on_message(self, message_id, data, attributes, publish_time):
        pass

    def run(self):
        def handle_message(message):
            if self._stopping:
                LOGGER.info('Consumer is stopping, nacking message %s', 
                           message.message_id)
                message.nack()
                return

            LOGGER.info('Received message # %s: %s, %s, %s' % (
                message.message_id, message.data, message.attributes, 
                message.publish_time))

            try:
                self.on_message(message.message_id, json.loads(message.data),
                              message.attributes, message.publish_time)
                LOGGER.info('Acknowledging message %s', message.message_id)
                message.ack()
            except Exception as e:
                LOGGER.exception(
                    'Error occurred when handling message: %s', str(e))
                message.nack()

        self.streaming_pull_future = self.instance.subscribe(
            self.subscription_name, 
            handle_message
        )
        self.loop.start()

    def stop(self):
        LOGGER.info('Stopping consumer')
        if hasattr(self, 'streaming_pull_future'):
            self.streaming_pull_future.cancel()
            try:
                self.streaming_pull_future.result()
            except Exception as e:
                LOGGER.warning('Error while stopping subscription: %s', str(e))
        
        self.instance.close()
        self.loop.stop()
        LOGGER.info('Consumer stopped')
