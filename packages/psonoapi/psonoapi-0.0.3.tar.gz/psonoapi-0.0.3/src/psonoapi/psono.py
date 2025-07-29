from .psonoapihelper import PsonoAPIHelper
from .datamodels import *
import nacl,json,os,logging,uuid


class PsonoAPI:
    def __init__(self,serverconfig: PsonoServerConfig = None,login: bool = True):
        if serverconfig is None:
            serverconfig = PsonoServerConfig(**dict(os.environ))
        self.session = PsonoServerSession(server=serverconfig)
        self.logger = logging.getLogger(__name__)
        if login:
            self.login()

    def _api_request(self,method: str,endpoint: str,data = None):
        return PsonoAPIHelper.api_request(method,endpoint,data,self.session)
    
    def _get_datastores(self):
        # Simple list of datastores, not encrypted
        endpoint = '/datastore/'
        datastore_return = self._api_request('GET', endpoint)             
        content = dict()
        for datastore_info in datastore_return['datastores']:
            content[datastore_info['id']] = datastore_info
        return content
    
    def _write_datastore(self,datastore: PsonoDataStore):
       method = 'POST'
       endpoint = '/datastore/'
       encrypted_datastore = PsonoAPIHelper.encrypt_symmetric(datastore.psono_dump(), datastore.secret_key)
       data = json.dumps({
            'datastore_id': self.datastore.datastore_id,
            'data': encrypted_datastore['text'],
            'data_nonce': encrypted_datastore['nonce'],
       })

       return self._api_request(method, endpoint, data=data)

    def set_datastore(self,datastore_id = None):
        self.datastore = self._get_datastore(datastore_id)
    
    def get_datastore(self,datastore_id = None) -> PsonoDataStore:
        if datastore_id is None:
            datastores = self._get_datastores()
            # Read content of all password datastores
            for datastore in datastores.values():
                if datastore['type'] != 'password':
                    continue
                datastore_id = datastore['id']
                break
        datastore_read_result = PsonoAPIHelper.get_datastore(datastore_id,self.session)
        return datastore_read_result


    def update_secret(self,secret: PsonoSecret):       
        encrypted_secret = PsonoAPIHelper.encrypt_symmetric(secret.psono_dump_json(), secret.secret_key)
        
        data = json.dumps({
            'secret_id': secret.secret_id,
            'data': encrypted_secret['text'],
            'data_nonce': encrypted_secret['nonce'],
            'callback_url': '',
            'callback_user': '',
            'callback_pass': '',
        })

        secret_result = self._api_request('POST','/secret/', data=data)

        return secret_result
        

    def generate_new_secret(self,secrettype) -> PsonoSecret:
        if secrettype not in psono_type_list:
            raise(f"Secret type {secrettype} Not one of accepted list: {psono_type_list}")
        link_id = str(uuid.uuid4())
        secret_key = nacl.encoding.HexEncoder.encode(nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)).decode()
        newsecret=PsonoTypeMap[secrettype](link_id=link_id,secret_key=secret_key,type=secrettype,secret_id='new',path='new')
        return newsecret
    
    def _write_new_secret(self,secret:PsonoSecret):
        encrypted_secret = PsonoAPIHelper.encrypt_symmetric(secret.psono_dump_json(), secret.secret_key)

        data = json.dumps({
            'data': encrypted_secret['text'],
            'data_nonce': encrypted_secret['nonce'],
            'link_id': secret.link_id,
            'parent_datastore_id': self.datastore['id'],
            'callback_url': '',
            'callback_user': '',
            'callback_pass': '',
        })
        secret_result = self._api_request('PUT','/secret/', data=data)
        return secret_result
    

    def write_secret(self,secret: PsonoSecret,create: bool = True,datastore: PsonoDataStore = None):      
        if datastore is None:
            datastore = self.datastore
        try:
            existing_secret_metadata = self.get_psono_path(secret.path,self.datastore)
            if isinstance(existing_secret_metadata,PsonoDataStoreFolder):
                raise Exception("Trying to write a secret that is already a folder")
            self.update_secret(secret)
        except:
            if not create:
                raise Exception(f"Trying to write secret to {secret.path} but create is set to False")
            secret_result = self._create_secret(secret,datastore)
                          
            # Add item to folder - this will create the folder/item if it doesn't exist.
            PsonoAPIHelper.add_item_to_datastore(self.datastore,secret)
            #  save datastore back to server
            #self._write_datastore(datastore)
        
        




    def get_path(self,path) -> PsonoDataItem :

        pathdetail,traversedpath = PsonoAPIHelper.get_datastore_path(self.datastore,path)
        if isinstance(pathdetail,PsonoDataStoreItem):
            item =  self._get_secret_data(pathdetail)
        elif isinstance(pathdetail,PsonoDataStoreFolder) and pathdetail.share_id is not None:
            sharedatastore = self.get_share(pathdetail)
            substorepath = path.replace(traversedpath,'')
            subpath,traversedpath = PsonoAPIHelper.get_datastore_path(sharedatastore,substorepath)
            pathdetail = subpath
            item = self._get_secret_data(subpath)
        else:
            return pathdetail
        
        item['path'] = path
        item['type'] = pathdetail.type
        item['link_id'] = pathdetail.id
        item['secret_key'] = pathdetail.secret_key
        ObjectClass = PsonoTypeMap[pathdetail.type]
        return ObjectClass(**item)     
    
    def get_share(self,share: PsonoDataStoreFolder) -> PsonoShare:
        share_return = self._api_request('GET','/share/'+ share.share_id + '/')
        sharedata = json.loads(PsonoAPIHelper.decrypt_symmetric(share_return['data'],share_return['data_nonce'],share.share_secret_key))
        psonoshare = PsonoShareStore(**sharedata)
        return psonoshare

    def _get_secret_data(self,secretdata: PsonoDataStoreItem):
        secretreturndata =  self._api_request('GET','/secret/' + secretdata.secret_id + '/')
        secretreturndata['secret_key'] = secretdata.secret_key
        secret_data = json.loads(PsonoAPIHelper.decrypt_data(secretreturndata,self.session).decode('utf-8'))
        secret_data['secret_id'] = secretdata.secret_id
        return secret_data


  

    def login(self):
        # 1. Generate the login info including the private key for PFS
        client_login_info = PsonoAPIHelper.generate_client_login_info(self.session)

        if True: # if logging in via apikey (no others are currently supported)
            endpoint = '/api-key/login/'
        
        json_response = PsonoAPIHelper.api_request('POST', '/api-key/login/', json.dumps(client_login_info),self.session)

        # If the signature is set, verify it
        if self.session.server.server_signature is not None:
            PsonoAPIHelper.verify_signature(json_response['login_info'],
                                          json_response['login_info_signature'],
                                          self.session.server.server_signature)
        else:
            self.logger.warning('Server signature is not set, cannot verify identity')
        
        self.session.public_key = json_response['server_session_public_key']
        decrypted_server_login_info = PsonoAPIHelper.decrypt_server_login_info(
            json_response['login_info'],
            json_response['login_info_nonce'],
            self.session
        )

        self.session.token = decrypted_server_login_info['token'] 
        self.session.secret_key = decrypted_server_login_info['session_secret_key'] 
        self.session.username = decrypted_server_login_info['user']['username']
        self.session.public_key = decrypted_server_login_info['user']['public_key'] 
        self.session.user_restricted = decrypted_server_login_info['api_key_restrict_to_secrets'] 
        

        # if the api key is unrestricted then the request will also return the encrypted secret and private key
        # of the user, symmetric encrypted with the api secret key
        if not self.session.user_restricted:
            def _decrypt_with_api_secret_key(session: PsonoServerSession,secret_hex, secret_nonce_hex):
                return PsonoAPIHelper.decrypt_symmetric(secret_hex, secret_nonce_hex, session.server.secret_key)

            self.session.user_private_key = _decrypt_with_api_secret_key(self.session,
                decrypted_server_login_info['user']['private_key'],
                decrypted_server_login_info['user']['private_key_nonce']
            )

            self.session.user_secret_key = _decrypt_with_api_secret_key(self.session,
                decrypted_server_login_info['user']['secret_key'],
                decrypted_server_login_info['user']['secret_key_nonce']
            ) 
            self.datastore = self.get_datastore()
