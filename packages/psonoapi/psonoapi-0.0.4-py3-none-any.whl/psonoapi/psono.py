from .psonoapihelper import PsonoAPIHelper
from .datamodels import *
import nacl,json,os,logging,uuid,deepdiff


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

    def _write_store(self,store: Union[PsonoDataStore,PsonoShareStore]):
        if isinstance(store,PsonoShareStore):
            return self._write_share(store)
        else:
            return self._write_datastore(store)
        
    def _write_share(self,sharestore: PsonoShareStore):
       method = 'PUT'
       endpoint = '/share/'
       encrypted_store = PsonoAPIHelper.encrypt_symmetric(sharestore.psono_dump_json(), sharestore.share_secret_key)
       data = json.dumps({
            'share_id': sharestore.share_id,
            'data': encrypted_store['text'],
            'data_nonce': encrypted_store['nonce'],
       })

       return self._api_request(method, endpoint, data=data)
    
    def _write_datastore(self,datastore: PsonoDataStore):
       method = 'POST'
       endpoint = '/datastore/'
       encrypted_datastore = PsonoAPIHelper.encrypt_symmetric(datastore.psono_dump_json(), datastore.secret_key)
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
        newsecret=psono_type_map[secrettype](link_id=link_id,secret_key=secret_key,type=secrettype,secret_id='new',path='new')
        return newsecret
    
    def _write_new_secret(self,secret:PsonoSecret,datastore_id: str = None,share_id: str = None):
        encrypted_secret = PsonoAPIHelper.encrypt_symmetric(secret.psono_dump_json(), secret.secret_key)
        parent_id_type= 'parent_datastore_id'
        if datastore_id is None and share_id is None:
            datastore_id = self.datastore.datastore_id
            parent_id = self.datastore.datastore_id
        elif datastore_id is not None:
            parent_id = datastore_id 
        else:
            parent_id_type= 'parent_share_id'
            parent_id = share_id 

        data = json.dumps({
            'data': encrypted_secret['text'],
            'data_nonce': encrypted_secret['nonce'],
            'link_id': secret.link_id,
            parent_id_type: parent_id,
            'callback_url': '',
            'callback_user': '',
            'callback_pass': '',
        })
        secret_result = self._api_request('PUT','/secret/', data=data)
        return secret_result
    

    def write_secret(self,secret: PsonoSecret,create: bool = True,datastore: PsonoDataStore = None):      
        if datastore is None:
            datastore = self.datastore
        existing_secret_metadata = None
       
        # if self.get_secret(secret.secret_id):
        #     self.update_secret(secret)
        #     return
        try:
            existing_secret_metadata = self.get_path(secret.path)
        except:
            pass
        if isinstance(existing_secret_metadata,PsonoDataStoreFolder):
            raise Exception("Trying to write a secret that is already a folder")
        elif isinstance(existing_secret_metadata,PsonoSecret):
            self.update_secret(secret)
            return
    
        if not create:
            raise Exception(f"Trying to write secret to {secret.path} but create is set to False")
        
        # we always get an up to date copy of the datastore
        datastore,datastorepath = self._get_store_by_path(secret.path)
        
        
        #if isinstance(datastore,PsonoShareStore):
        #    secret_result = self._write_new_secret(secret,share_id=datastore.share_id)
        #else:
        #    secret_result = self._write_new_secret(secret,datastore_id=datastore.datastore_id)
            
        #secret.secret_id = secret_result['secret_id']
        # Adjust the path to be where the share/datastore is.
        secret.path = secret.path.replace(datastorepath,'')
        # Add item to folder - this will create the folder/item if it doesn't exist.
        #print(f"Writing new secret {secret} to datastore {datastore.name}")
        secret=PsonoSecret(secret_id='233cdfdb-6b42-4e66-b1a4-0da0501253bd',
                                  secret_key='f27f83e42e57ff41d2e23e7f0ebcf2dfeb29550957d73e37cd080f02d8904f98',
                                  custom_fields=None,
                                  type='application_password',
                                  link_id='20353588-a332-4186-98ba-1d734f5b7f8c',
                                  path='testing_new_share_item',
                                  tags=None, 
                                  title=None, 
                                  notes=None, 
                                  password='1234', 
                                  username=None)
        print(datastore)
        PsonoAPIHelper.add_item_to_datastore(datastore,secret)
        print(datastore)
        print(self._write_store(datastore))

                   
        
        
        




    def _get_store_by_path(self,path,datastore: PsonoDataStore=None) -> Union[PsonoDataStore,PsonoShareStore] :
        if datastore is None:
            datastore = self.datastore
        try:
            pathdetail,traversedpath = PsonoAPIHelper.get_datastore_path(self.datastore,path)
        except:
            pathdetail = datastore
            traversedpath = ''
        if isinstance(pathdetail,PsonoDataStoreFolder) and pathdetail.share_id is not None:
            sharedatastore = self.get_share(pathdetail)
            store =  sharedatastore
        else:
            store =  datastore
        return (store,traversedpath)
        

    def get_path(self,path,datastore: PsonoDataStore=None,metadata_only=False) -> PsonoDataItem :
        if datastore is None:
            datastore = self.datastore
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
        if metadata_only:
            return pathdetail
        item['path'] = path
        item['type'] = pathdetail.type
        item['link_id'] = pathdetail.id
        item['secret_key'] = pathdetail.secret_key
        return PsonoAPIHelper.translate_secret_data(item)
    
    def get_share(self,share: PsonoDataStoreFolder) -> PsonoShare:
        share_return = self._api_request('GET','/share/'+ share.share_id + '/')
        sharedata = json.loads(PsonoAPIHelper.decrypt_symmetric(share_return['data'],share_return['data_nonce'],share.share_secret_key))
        if "share_id" not in sharedata:
            psonoshare = PsonoShareStore(**sharedata,share_id=share.share_id,share_secret_key=share.share_secret_key)
        else:
            psonoshare = PsonoShareStore(**sharedata)
        return psonoshare

    def _get_secret_data(self,secretdata: PsonoDataStoreItem):
        secretreturndata =  self._api_request('GET','/secret/' + secretdata.secret_id + '/')
        secretreturndata['secret_key'] = secretdata.secret_key
        secret_data = json.loads(PsonoAPIHelper.decrypt_data(secretreturndata,self.session).decode('utf-8'))
        secret_data['secret_id'] = secretdata.secret_id
        return secret_data
    
    def get_secret(self,secret_id):
        secretreturndata =  self._api_request('GET','/secret/' + secret_id + '/')
        #secretdata = self._get_secret_data(tempsecret)
        secret_data = json.loads(PsonoAPIHelper.decrypt_data(secretreturndata,self.session).decode('utf-8'))
        #ObjectClass = PsonoTypeMap[pathdetail.type]
        #return ObjectClass(**item)  

  

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
