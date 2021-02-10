import http.client
import json
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

token = ""

def anonyomous_access():
    # TODO implement
    global token
    connection = http.client.HTTPSConnection('ecosystem.egain.cloud')
    headers = {'Accept': 'application/json','Accept-Language': 'en-US'}
    connection.request('POST', '/system/ws/v15/ss/portal/555500000001000/authentication/anonymous',"",headers)
    response = connection.getresponse()
    status = response.status
    token = response.getheader('X-egain-session')
    #print ("status", status, "token", token)    
    return status

def chat_availability():
    # TODO implement
    connection = http.client.HTTPSConnection('ecosystem.egain.cloud')
    headers = {'Content-Type': 'application/json','Accept-Language': 'en-US','X-egain-session': token}
    connection.request('GET', '/system/ws/chat/entrypoint/agentAvailability/1004',"",headers)
    response = connection.getresponse()
    status = response.status
    responseXml = ET.fromstring(response.read()) 
    available = responseXml.attrib.get("available") 
    #print("status", status, "available", available)
    return available

def dispatch(event):
    """
    Called when the user specifies an intent for this bot.
    """

    # Dispatch to your bot's intent handlers
    if (event['currentIntent']['name'] == 'Chat'):
        status = anonyomous_access()
        response = '{"sessionAttributes": { },"dialogAction": {"type": "Close","fulfillmentState": "Fulfilled","message": {"contentType": "PlainText","content": ""}}}'
        jsonresponse = json.loads(response)
        if (status == 204):
            if (chat_availability() == "true"):
                logger.debug('status:{} availability {}'.format(status, "Available"))
                jsonresponse["dialogAction"]["message"]["content"] = "Yes a Agent is available"
                return jsonresponse
            else:
                logger.debug('status:{} availability {}'.format(status, "Unavailable"))
                jsonresponse["dialogAction"]["message"]["content"] = "No an Agent is not available"
                return jsonresponse
        else:
            logger.debug('status {}',format(status))
            jsonresponse["message"]["content"] = "Chat System is down"
            return jsonresponse
    raise Exception('Intent with name ' + intent_name + ' not supported')
    
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    logger.debug(format(event))
    return dispatch(event)

