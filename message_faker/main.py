import queue_wrapper
from faker import Faker
import json
import message_wrapper
from time import time

fake = Faker()

q = queue_wrapper.get_queue('graph-messages')

msgs = 0

milliseconds = lambda: int(time() * 1000)
def make_message(i):
    return {
        'body': json.dumps({ 
            "name": fake.name(),
            "country": fake.country(),
            "company": fake.company(),
            "index": i,
        }),
        'attributes': {
            'index': { 'StringValue': '%d' % i, 'DataType': 'String'}
        }
    }

start = milliseconds()

while True:
    batch = [make_message(i) for i in range(0, 10)]
    message_wrapper.send_messages(q, batch)
    msgs = msgs + len(batch)

    if msgs % 100 == 0:
        t = milliseconds()
        rt = msgs / ((t-start)/1000)
        print("%d messages in %d milliseconds; %f messages/sec" % (msgs, (t-start), rt))

