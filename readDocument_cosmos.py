import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
HOST = ''
MASTER_KEY = ''
DATABASE_ID = ''
COLLECTION_ID = ''
database_link = 'dbs/' + DATABASE_ID
collection_link = database_link + '/colls/' + COLLECTION_ID
class IDisposable(cosmos_client.CosmosClient):
    """ A context manager to automatically close an object with a close method
    in a with statement. """

    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        return self.obj # bound to target

    def __exit__(self, exception_type, exception_val, trace):
        # extra cleanup in here
        self = None

class DocumentManagement(cosmos_client.CosmosClient):
    def ReadItems(client,doc_id):
        print('Read Document Item by Id')
        doc_link = collection_link+'/docs/'+doc_id
        options = {
            "enableCrossPartitionQuery":True,
            "partitionKey": 'name'
        }
        response = client.ReadItem(doc_link,options)
        print('Item:{0}'.format(response))

    def ReadDocuments(client):
        print('\nReading all documents in a collection\n')
        # NOTE: Use MaxItemCount on Options to control how many documents come back per trip to the server
        #       Important to handle throttles whenever you are doing operations such as this that might
        #       result in a 429 (throttled request)
        documentlist = list(client.ReadItems(collection_link, {'maxItemCount':10}))
        print(client.ReadItems(collection_link,{'maxItemCound':10}))
        print('Found {0} documents'.format(documentlist.__len__()))
        for doc in documentlist:
            print('Document Id: {0}'.format(doc.get('id')))
            ReadItems(client,doc.get('id'))
def run_sample():
    with IDisposable(cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )) as client:
        try:
            DocumentManagement.ReadDocuments(client)
            print('read document done')
        except Exception as e:
            print('read document failed"{0}'.format(e.args))            
if __name__ == '__main__':
    try:
        run_sample()

    except Exception as e:
            print("Top level Error: args:{0}, message:N/A".format(e.args))
