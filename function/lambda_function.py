import os
import logging
import jsonpickle
import json
import boto3
from aws_xray_sdk.core import patch_all
import os
from time import time
from neo4j import GraphDatabase

neo4j_uri = os.environ.get('NEO4J_URI')
neo4j_user = os.environ.get('NEO4J_USERNAME')
neo4j_password = os.environ.get('NEO4J_PASSWORD')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

if neo4j_uri is None or neo4j_user is None or neo4j_password is None:
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    raise Exception("Missing environment variables for connecting to Aura; double check!")

driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password),
    max_connection_lifetime=5*60,
    keep_alive=True)

client = boto3.client('lambda')
client.get_account_settings()

milliseconds = lambda: int(time() * 1000)

def write_graph_record(tx, event):
    json_messages = [json.loads(msg['body']) for msg in event['Records']]

    start = milliseconds()

    try:
        tx.run("""
            UNWIND $json_messages AS message
            MERGE (p:Person { name: message.name })
            MERGE (c:Company { name: message.company })
            MERGE (co:Country { name: message.country })
            MERGE (p)-[:WORKS_FOR]->(c)
            MERGE (c)-[:IN]->(co);
        """, json_messages=json_messages)
    except Exception as e:
        raise e
    finally:
        delta = milliseconds() - start
        rt = len(json_messages) / (delta/1000)
        logger.info('Wrote batch of %d graph records in %d ms or %f recs/sec avg' % (len(json_messages), delta, rt))

def lambda_handler(event, context):
    #logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    #logger.info('## EVENT\r' + jsonpickle.encode(event))
    #logger.info('## CONTEXT\r' + jsonpickle.encode(context))
    #logger.info("## CONNECTING TO %s" % neo4j_uri)

    with driver.session() as session:
        session.write_transaction(write_graph_record, event)

    response = client.get_account_settings()
    return response['AccountUsage']