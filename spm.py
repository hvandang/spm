from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import hvac
import os
import json

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


# 1. Initialize vault client linking to vault server by ip
'''parser = reqparse.RequestParser()
parser.add_argument('shares', type=str)
parser.add_argument('threshold', type=str)'''

class Init(Resource):
    def post(self):
        # create a vault in vault server	
        '''args = parser.parse_args()
        shares = str(args['shares'])
        threshold = str(args['threshold'])'''
        initVault(1,1) #shares=1, threshold=1
		
def initVault(shares, threshold): 
    client = hvac.Client(url='http://vault-server:8200')# http://127.0.0.1:8200
    vault = client.initialize(shares,threshold)
    root_token = vault['root_token']
    unseal_keys = vault['keys']
    # write root token into file
    f = open('vaultoken', 'w')
    f.write(root_token)
    f.close()
    client.token = root_token
    # unseal the vault
    client.unseal_multi(unseal_keys)
    client.write('secret/foo', baz='bar', lease='1h')
    result = client.read('secret/foo') # a dict object
    f = open('secret', 'w')
    f.write(json.dumps(result)) # write a dict
    f.close()

api.add_resource(Init, '/init')	

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=5003)
    
# write root token into file
#file = os.open(os.path.expanduser('/home/vault-token'), os.O_WRONLY | os.O_CREAT, 0600)
#os.write(f, root_token)
#os.close(f)

# Write secret to vault

#print(client.read('secret/foo'))