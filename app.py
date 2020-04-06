import connexion
from connexion import NoContent
import requests
from pykafka import KafkaClient
import yaml
import json
import datetime
from flask_cors import CORS, cross_origin
import logging.config

def companyinfo(CompanyInfo):

    with open ('kafka_config.yaml', 'r') as f:
        kafka = yaml.safe_load(f.read())

    client = KafkaClient(hosts='{0}:{1}'.format(kafka['kafka']['kafka-server'], kafka['kafka']['kafka-port']))
    topic = client.topics['{0}'.format(kafka['kafka']['topic'])]
    producer = topic.get_sync_producer()
    msg = {
        "type": 'Info',
        "datatime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": CompanyInfo
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return 200

def companyorder(CompanyOrder):

    with open ('kafka_config.yaml', 'r') as f:
        kafka = yaml.safe_load(f.read())

    client = KafkaClient(hosts='{0}:{1}'.format(kafka['kafka']['kafka-server'], kafka['kafka']['kafka-port']))
    topic = client.topics['{0}'.format(kafka['kafka']['topic'])]
    producer = topic.get_sync_producer()
    msg = {
        "type": 'Order',
        "datatime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": CompanyOrder
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    app.run(port=8080)