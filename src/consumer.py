# Group - 30
# Members - 
# Taniya Adil - IIT2019054
# Alka Trivedi - IIT2019055

#!/usr/bin/env python

"""Consumes stream for printing all messages to the console.
"""

#import libraries

import argparse
import json
import sys
import time
import socket
from confluent_kafka import Consumer, KafkaError, KafkaException
import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#function to process the message consume by the consumer
def msg_process(msg):
    
    #get the message value
    val = msg.value()

    #converting message to the json value
    dval = json.loads(val)

    #printing message consumed by the consumer
    print(dval)

    #writing message consumed by the consumer to a text file
    with open('input.txt', 'a', buffering=20*(1024**2)) as f:
    	f.write(str(dval) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')

    args = parser.parse_args()

    conf = {'bootstrap.servers': 'localhost:9092',
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'group.id': socket.gethostname()}

    consumer = Consumer(conf)

    running = True

    try:
        while running:
            #consumer subscribe to the topic created
            consumer.subscribe([args.topic])

            #start fetching record in sequential order from the specified topic subscribed by the consumer
            msg = consumer.poll(1)

            #checking if msg is none
            if msg is None:
                continue

            #checking if the msg is the error msg
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    sys.stderr.write('Topic unknown, creating %s topic\n' %
                                     (args.topic))
                elif msg.error():
                    raise KafkaException(msg.error())

            #if the msg is neither none nor it contains any error then we will process the msg
            else:
            	msg_process(msg)

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    main()
