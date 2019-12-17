from sanic import Sanic
from sanic import response
from sanic_cors import CORS
from sanic.views import HTTPMethodView

import model

# Create instance of sanic
app = Sanic(__name__)
CORS(app)

async def import_users(request):
  if request.method == 'OPTIONS':
    return response.json({})
  
  result = model.import_users()
  return response.json({'message': 'Ok', 'result': result}, status=200)

async def import_interactions(request):
  if request.method == 'OPTIONS':
    return response.json({})
  
  result = model.import_interactions()
  return response.json({'message': 'Ok', 'result': result}, status=200)

class UsersResource(HTTPMethodView):
  async def get(self, request):
    data = model.get_users()
    if not data:
      return response.json({'message': 'There aren\'t users'}, status=404)
    
    return response.json({'message': 'Ok', 'users': data})

  async def options(self, request):
    return response.json({})

class TicketsResource(HTTPMethodView):
  async def post(self, request):
    data = request.json
    result = []
    if data:
      result = model.create_tickets(int(data.get('number_tickets')))

    return response.json({'message': 'Ok', 'result': len(result)})

  async def get(self, request):
    data = model.get_tickets()
    if not data:
      return response.json({'message': 'There aren\'t tickets'}, status=404)
    
    return response.json({'message': 'Ok', 'tickets': data})

  async def options(self, request):
    return response.json({})

# Endpoints
app.add_route(import_users, '/import/users', ['POST', 'OPTIONS'])
app.add_route(import_interactions, '/import/tickets', ['POST', 'OPTIONS'])
app.add_route(UsersResource.as_view(), '/users')
app.add_route(TicketsResource.as_view(), '/tickets')

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)