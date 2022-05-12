# Group - 30
# Members - 
# Taniya Adil - IIT2019054
# Alka Trivedi - IIT2019055

#!/usr/bin/env python

"""Generates a stream to Kafka from a time series csv file.
"""

#import libraries
import argparse
import csv
import json
import sys
import time
from dateutil.parser import parse
from confluent_kafka import Producer
import socket


#function acked to print the message produced by the producer
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg.value()), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename', type=str,
                        help='Time series csv file.')
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')
    parser.add_argument('--speed', type=float, default=1, required=False,
                        help='Speed up time series by a given multiplicative factor.')
    args = parser.parse_args()

    topic = args.topic
    p_key = args.filename

    conf = {'bootstrap.servers': "localhost:9092",
            'client.id': socket.gethostname()}
    producer = Producer(conf)

    #reading csv file
    rdr = csv.reader(open(args.filename))
    next(rdr)  #skiping header

    while True:

        try:
            #line by line reading the csv file
            line1 = next(rdr, None)

            #extracting values
            hadm_id, subject_id, admit_dt, disch_dt = line1[0], line1[1], line1[2], line1[3]

            #converting csv columns to key value pair
            result = {}
            result = {'hadm_id' : hadm_id, 'subject_id' : subject_id, 'admit_dt' : admit_dt, 'disch_dt' : disch_dt}

            #convert dict to json as message format
            jresult = json.dumps(result)

            #produce the message
            producer.produce(topic, key=p_key, value=jresult, callback=acked)
            #clearing the internal buffer
            producer.flush()

        except TypeError:
            sys.exit()


if __name__ == "__main__":
    main()
