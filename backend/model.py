import json
import random
import pymongo
import requests
from urllib.parse import urlencode
from ticket_values import *
from pymongo import MongoClient

with open('config.json', 'r') as file:
  config = json.load(file)

client = MongoClient()
db = client[config['DB_NAME']]
users = db[config['DB_COLLECTION_USER']]
interactions = db[config['DB_COLLECTION_TICKET']]

url  = 'https://{domain}.zendesk.com/api/v2/{resource}{params}'
credentials = config['API_EMAIL'], config['API_PASSWORD']
session = requests.Session()
session.auth = credentials

def latest_user_update():
  try:
    last_update = users.find().sort('updated_at', pymongo.DESCENDING)\
      .limit(1)[0]
  except IndexError as e:
    return None
  
  return last_update['updated_at']

def import_users():
  last_update = latest_user_update()
  params = {
    'per_page': '2'
  }

  if last_update:
    params['query'] = 'type:user updated>' + last_update
  else:
    params['query'] = 'type:user'

  sesion_url = url.format(domain=config['API_DOMAIN'],
    resource='search.json', params='?' + urlencode(params))
  data = []
  while sesion_url:
    response = session.get(sesion_url)
    if response:
      response = response.json()
      data += response['results']
    sesion_url = response['next_page']
  
  for user in data:
    first_name = user['name'].split(' ')[0]
    last_name = user['name'][len(first_name) + 1:]
    document = {
      'first_name': first_name,
      'last_name': last_name,
      'email': user['email'],
      'integration_id': user['id'],
      'created_at': user['created_at'],
      'updated_at': user['updated_at']
    }
    users.replace_one({'integration_id': document['integration_id']},
      document, True)
  
  return len(data)

def get_users():
  result = []
  documents = users.find()
  if not documents:
    return None

  for user in documents:
    user['_id'] = str(user['_id'])
    result.append(user)
  
  return result

def latest_interaction_update():
  """Get the last update date of the interactions.

    Return date
  """
  try:
    last_update = interactions.find().sort('updated_at', pymongo.DESCENDING)\
      .limit(1)[0]
  except IndexError as e:
    return None
  
  return last_update['updated_at']

def import_interactions():
  """Import new or updated interactions from the API Zendesk.
  
  Return the number of interactions imported

  """
  
  last_update = latest_interaction_update()
  
  # URL params
  params = {
    'per_page': '2'
  }

  # Query
  if last_update:
    params['query'] = 'type:ticket updated>' + last_update
  else:
    params['query'] = 'type:ticket'
  
  sesion_url = url.format(domain=config['API_DOMAIN'],
    resource='search.json', params='?' + urlencode(params))
  data = []
  # Pagination
  while sesion_url:
    response = session.get(sesion_url)
    if response:
      response = response.json()
      data += response['results']
    sesion_url = response['next_page']
  
  for ticket in data:
    ticket['_id'] = ticket['id']
    del ticket['id']
    interactions.replace_one({'_id': ticket['_id']}, ticket, True)
  
  return len(data)

def get_tickets():
  result = []
  for ticket in interactions.find():
    user = users.find_one({'integration_id': ticket['assignee_id']})
    if user:
      ticket['agent_name'] = user['first_name'] + ' ' + user['last_name']
    else:
      ticket['agent_name'] = ''
    result.append(ticket)

  return result

def create_tickets(quantity):
  tickets = []
  user_ids = []
  for user in get_users():
    user_ids.append(user['integration_id'])

  for _ in range(quantity):
    element_subject = random.randint(0, len(subject) - 1)
    element_via = random.randint(0, len(via_channel) - 1)

    tickets.append({
      'subject': subject[element_subject],
      'comment': comment[element_subject],
      'priority': random.choice(priority),
      'status': random.choice(status),
      'type': random.choice(types),
      'via': {
        'channel': via_channel[element_via],
        'source': via_source[0]
      },
      'assignee_id': random.choice(user_ids)
    })
  
  headers = {'Content-Type': 'application/json'}
  result = []
  
  for ticket in tickets:
    response = session.post(url.format(domain=config['API_DOMAIN'],
      resource='tickets.json', params=''), headers=headers,
      data=json.dumps({"ticket": ticket}))
    if response:
      response = response.json()
      item = response.get('ticket')
      item['_id'] = item['id']
      del item['id']
      interactions.replace_one({'_id': item['_id']}, item, True)
      result.append(response)
  
  return result
