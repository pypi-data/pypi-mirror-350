# -*- coding: utf-8 -*-
# Reference: Pika usage example in its documentation

from __future__ import absolute_import
from builtins import str
from builtins import object
import logging
import pika
import json
import signal

LOGGER = logging.getLogger(__name__)


class BaseConsumer(object):
    EXCHANGE = ''
    EXCHANGE_TYPE = 'topic'
    QUEUE = ''
    ROUTING_KEY = '#'

    def __init__(self, amqp_url):
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._random_queue = self.QUEUE == ''
        self._url = amqp_url
        self._stopping = False
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGINT, self._handle_sigterm)

    def _handle_sigterm(self, signum, frame):
        LOGGER.info('Received signal %s. Setting stopping flag...', signum)
        self._stopping = True

    def connect(self):
        LOGGER.info('Connecting to %s', self._url)
        return pika.SelectConnection(pika.URLParameters(self._url),
                                     self.on_connection_open,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        LOGGER.info('Connection opened')
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None

        if self._random_queue:
            self.QUEUE = ''

        if self._closing:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s',
                           reply_code, reply_text)
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        if not self._closing:

            # Create a new connection
            self._connection = self.connect()

            # There is now a new connection, needs a new ioloop to run
            self._connection.ioloop.start()

    def open_channel(self):
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        LOGGER.warning('Channel %i was closed: (%s) %s',
                       channel, reply_code, reply_text)
        self._connection.close()

    def setup_exchange(self, exchange_name):
        LOGGER.info('Declaring exchange %s', exchange_name)
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange_name,
                                       self.EXCHANGE_TYPE)

    def on_exchange_declareok(self, unused_frame):
        LOGGER.info('Exchange declared')
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        if queue_name:
            LOGGER.info('Declaring queue %s', queue_name)
            self._channel.queue_declare(
                self.on_queue_declareok, queue_name, durable=True)
        else:
            LOGGER.info('Declaring exclusive queue')
            self._channel.queue_declare(
                self.on_queue_declareok, durable=True, exclusive=True)

    def on_queue_declareok(self, method_frame):
        self.QUEUE = method_frame.method.queue

        LOGGER.info('Binding %s to %s with %s',
                    self.EXCHANGE, self.QUEUE, self.ROUTING_KEY)
        self._channel.queue_bind(self.on_bindok, self.QUEUE,
                                 self.EXCHANGE, self.ROUTING_KEY)

    def on_bindok(self, unused_frame):
        LOGGER.info('Queue bound')
        self.set_qos()

    def set_qos(self):
        LOGGER.info('Setting QoS (maximum prefetch count = 1)')
        self._channel.basic_qos(self.on_qosok, prefetch_count=1)

    def on_qosok(self, method_frame):
        LOGGER.info('QoS set')
        self.start_consuming()

    def start_consuming(self):
        LOGGER.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self._on_message,
                                                         self.QUEUE)

    def add_on_cancel_callback(self):
        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        LOGGER.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, basic_deliver, properties, body):
        pass

    def _on_message(self, unused_channel, basic_deliver, properties, body):
        if isinstance(body, bytes):
            body = body.decode('UTF-8')

        LOGGER.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body)

        try:
            self.on_message(basic_deliver, properties, json.loads(body))
            self.acknowledge_message(basic_deliver.delivery_tag)
        except Exception as e:
            LOGGER.warning('Error occured when handling message: %s', str(e))
            self.negative_acknowledge_message(basic_deliver.delivery_tag)
        
        if self._stopping:
            LOGGER.info('Stopping flag detected, initiating shutdown...')
            self.stop()

    def acknowledge_message(self, delivery_tag):
        LOGGER.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def negative_acknowledge_message(self, delivery_tag):
        LOGGER.inf('Negative acknowledging message %s', delivery_tag)
        self._channel.basic_nack(delivery_tag)

    def stop_consuming(self):
        if self._channel:
            LOGGER.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def on_cancelok(self, unused_frame):
        LOGGER.info('RabbitMQ acknowledged the cancellation of the consumer')
        self.close_channel()

    def close_channel(self):
        LOGGER.info('Closing the channel')
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        LOGGER.info('Stopping')
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.start()
        LOGGER.info('Stopped')

        if self._random_queue:
            self.QUEUE = ''

    def close_connection(self):
        LOGGER.info('Closing connection')
        self._connection.close()
