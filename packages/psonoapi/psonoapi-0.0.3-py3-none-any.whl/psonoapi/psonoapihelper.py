import requests
import json
import nacl.encoding
import nacl.signing
import nacl.secret
import binascii
import uuid
from nacl.public import PrivateKey, PublicKey, Box
from .datamodels import *

class PsonoAPIHelper:
    @staticmethod
    def generate_client_login_info(session: PsonoServerSession):
        """
        Generates and signs the login info
        Returns a tuple of the session private key and the login info
        """

        box = PrivateKey.generate()
        session.private_key = box.encode(encoder=nacl.encoding.HexEncoder).decode()
        session.public_key = box.public_key.encode(encoder=nacl.encoding.HexEncoder).decode()

        info = {
            'api_key_id': session.server.key_id,
            'session_public_key': session.public_key,
            'device_description': session.server.session_name,
        }

        info = json.dumps(info)

        signing_box = nacl.signing.SigningKey(session.server.private_key, encoder=nacl.encoding.HexEncoder)

        # The first 128 chars (512 bits or 64 bytes) are the actual signature, the rest the binary encoded info
        signed = signing_box.sign(info.encode())
        signature = binascii.hexlify(signed.signature)

        return  {
            'info': info,
            'signature': signature.decode(),
        }
    @staticmethod
    def decrypt_server_login_info(login_info_hex, login_info_nonce_hex, session: PsonoServerSession):
        """
        Takes the login info and nonce together with the session public and private key.
        Will decrypt the login info and interpret it as json and return the json parsed object.
        """

        crypto_box = Box(PrivateKey(session.private_key, encoder=nacl.encoding.HexEncoder),
                        PublicKey(session.public_key, encoder=nacl.encoding.HexEncoder))

        login_info = nacl.encoding.HexEncoder.decode(login_info_hex)
        login_info_nonce = nacl.encoding.HexEncoder.decode(login_info_nonce_hex)

        login_info = json.loads(crypto_box.decrypt(login_info, login_info_nonce).decode())

        return login_info
    
    @staticmethod
    def verify_signature(login_info, login_info_signature,server_signature):
        """
        Takes the login info and the provided signature and will validate it with the help of server_signature.

        Will raise an exception if it does not match.
        """

        verify_key = nacl.signing.VerifyKey(server_signature, encoder=nacl.encoding.HexEncoder)

        verify_key.verify(login_info.encode(), binascii.unhexlify(login_info_signature))

    @staticmethod
    def encrypt_symmetric(msg, secret):
        """
        Encrypts a message with a random nonce and a given secret
        """

        # generate random nonce
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

        # open crypto box with session secret
        secret_box = nacl.secret.SecretBox(secret, encoder=nacl.encoding.HexEncoder)

        # encrypt msg with crypto box and nonce
        encrypted = secret_box.encrypt(msg.encode(), nonce)

        # cut away the nonce
        text = encrypted[len(nonce):]

        # convert nonce and encrypted msg to hex
        nonce_hex = nacl.encoding.HexEncoder.encode(nonce).decode()
        text_hex = nacl.encoding.HexEncoder.encode(text).decode()
        return {'text': text_hex, 'nonce': nonce_hex}


    @staticmethod
    def decrypt_symmetric(text_hex, nonce_hex, secret):
        """
        Decryts an encrypted text with nonce with the given secret

        :param text_hex:
        :type text_hex:
        :param nonce_hex:
        :type nonce_hex:
        :param secret:
        :type secret:
        :return:
        :rtype:
        """

        text = nacl.encoding.HexEncoder.decode(text_hex)
        nonce = nacl.encoding.HexEncoder.decode(nonce_hex)

        secret_box = nacl.secret.SecretBox(secret, encoder=nacl.encoding.HexEncoder)

        return secret_box.decrypt(text, nonce)

    @staticmethod
    def api_request(method, endpoint, data, session: PsonoServerSession):
        """
        Static API Request helper that will also automatically decrypt the content if a session secret was provided.
        Will return the decrypted content.

        """

        if session.token:
            headers = {'content-type': 'application/json', 'authorization': 'Token ' + session.token}
        else:
            headers = {'content-type': 'application/json'}
        if session and session.secret_key and data is not None:
            data = json.dumps(__class__.encrypt_symmetric(data,session.secret_key))
        r = requests.request(method, session.server.server_url + endpoint, data=data, headers=headers, verify=session.server.ssl_verify)

        if not session.secret_key:
            return_data =  r.json()
        else:
            encrypted_content = r.json()
            decrypted_content = __class__.decrypt_symmetric(encrypted_content['text'], encrypted_content['nonce'], session.secret_key)
            return_data =  json.loads(decrypted_content)

        if 'throttle' in return_data.get('detail',''):
            raise Exception(f"Request was throttled {return_data}")
        return return_data
    
    @staticmethod
    def add_item_to_datastore(datastore,secret:PsonoSecret):
        splitpath = secret.path.split('/')
        folder = "/".join(splitpath[:-1])
        name = splitpath[-1]
        item = PsonoDataStoreItem(
            id=secret.link_id,
            name=name,
            type=secret.type,
            secret_id=secret.secret_id,
            secret_key=secret.secret_key
        )
        folderdata = __class__.create_or_get_folder(datastore,folder)

        if 'items' not in folderdata:
            folderdata['items'] = []
        folderdata['items'].append(item)


 
    @staticmethod
    def create_or_get_folder(datastore: PsonoDataStore,folder: str) -> PsonoDataStoreFolder:
        partialpath = list()
        previouspath: dict
        for folderpart in folder.split('/'):
            partialpath.append(folderpart)
            thispath = __class__.get_path(datastore,"/".join(partialpath))
            if thispath is None:
                thispath = __class__.create_folder(previouspath,folderpart)
            previouspath = thispath
        
        return previouspath
    
    @staticmethod
    def create_folder(datastore: PsonoDataStore,foldername):
        newfolder = PsonoDataStoreFolder(
            id=str(uuid.uuid4()),
            name=foldername,
        )
        datastore.folders.append(newfolder)
        return newfolder
    
    @staticmethod
    def get_datastore_path(datastore:PsonoDataStoreFolder,folder: str,traversedpath=''):
        folderpath = folder.split('/')
        end = False
        if len(folderpath) == 0 or folderpath[-1] == "":
            end = True

        for folderdata in datastore.folders:
            if folderdata.name == folderpath[0]:
                if folderdata.share_id is not None:
                    traversedpath = traversedpath + folderpath[0] + "/"
                    return folderdata,traversedpath
                elif end:
                    traversedpath = traversedpath + folderpath[0] + "/"
                    return folderdata,traversedpath
                else:
                    traversedpath = traversedpath + folderpath[0] + "/"
                    return __class__.get_datastore_path(folderdata,"/".join(folderpath[1:]),traversedpath)

        for itemdata in datastore.items:
            if itemdata.name == folderpath[0]:
                return itemdata,traversedpath
        raise Exception(f"Cannot find \"{folderpath[0]}\" in \"{traversedpath}\"")
    @staticmethod
    def get_datastore(datastore_id,session: PsonoServerSession) -> PsonoDataStore:
        """
        :param datastore_id:
        :type datastore_id:
        :return:
        :rtype:
        """

        method = 'GET'
        endpoint = '/datastore/' + datastore_id + '/'
        datastore_return = __class__.api_request(method, endpoint,None,session)        
        
        datastore_data =  json.loads(__class__.decrypt_data(datastore_return,session))
        
        datastore_data['secret_key'] = datastore_return['secret_key']
        datastore_data['secret_key_nonce'] = datastore_return['secret_key_nonce']
        return PsonoDataStore(**datastore_data)
    
    def decrypt_secret_key(encrypted_item: dict,session: PsonoServerSession):
        if 'secret_key_nonce' in encrypted_item.keys():
            return __class__.decrypt_symmetric(
                    encrypted_item['secret_key'],
                    encrypted_item['secret_key_nonce'],
                    session.user_secret_key
                )
        else:
            return encrypted_item['secret_key'].encode('utf-8')

    def decrypt_data(encrypted_item: dict,session: PsonoServerSession):
        secret_key = __class__.decrypt_secret_key(encrypted_item,session)
        return __class__.decrypt_symmetric(
            encrypted_item['data'],
            encrypted_item['data_nonce'],
            secret_key
        )