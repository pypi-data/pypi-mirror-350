from __future__ import annotations
import socket
from pydantic import BaseModel, ConfigDict, Json, Field,AliasGenerator
from typing import Any, List, Union, Optional,Dict
from contextvars import ContextVar
from contextlib import contextmanager
from typing import Any

_parent_data = ContextVar("_parent_data")

class MyBase(BaseModel):
  def __init__(self, /, **data: Any):
    super().__init__(**data)
    self._parent_data = _parent_data.get(None)

  def psono_dump(self):
    return self.model_dump(exclude_none=True,exclude_unset=True,by_alias=True)
  def psono_dump_json(self):
    return self.model_dump_json(exclude_none=True,exclude_unset=True,by_alias=True)
  @classmethod
  @contextmanager
  def bind(cls, parent_data):
    token = _parent_data.set(parent_data)
    try:
       yield cls
    finally:
        _parent_data.reset(token)

# allows us to easily import environment variables
def _psono_config_alias_generator(fieldname: str): 
    newfieldname =  'PSONO_API_' + fieldname.upper()
    return newfieldname

class PsonoServerConfig(BaseModel):
    key_id: str = Field(default=None)
    private_key: Optional[str] = Field(default=None)
    secret_key: Optional[str] = Field(default=None)
    server_url: str = Field(default='https://www.psono.pw/server')
    server_public_key: Optional[str] = Field(default=None)
    server_signature: Optional[str] = Field(default=None)
    session_name: str= Field(default='Python Client ' + socket.gethostname())
    ssl_verify: bool = Field(default=True)
    class Config:
        populate_by_name = True
        alias_generator=AliasGenerator(alias=_psono_config_alias_generator)

class PsonoServerSession(BaseModel):
    logged_in: bool = Field(default=False)
    server: PsonoServerConfig
    token: Optional[str] = Field(default=None)
    private_key: Optional[str] = Field(default=None)
    secret_key: Optional[str] = Field(default=None)
    public_key: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    user_public_key: Optional[str] = Field(default=None)
    user_private_key: Optional[str] = Field(default=None)
    user_secret_key: Optional[str] = Field(default=None)
    user_restricted: Optional[bool] = Field(default=None)
  

class PsonoCustomField(BaseModel):
    name: str
    type: str
    value: str


class PsonoDataItem(MyBase):
    name: str 
    id: str 
    deleted: Optional[bool] = Field(default=None)

class PsonoDataStoreItem(PsonoDataItem):
    type: str
    urlfilter: Optional[str] = Field(default=None)
    autosubmit: Optional[bool] = Field(default=None)
    secret_key: str
    secret_id: str


class PsonoDataStoreFolder(PsonoDataItem):
    share_id: Optional[str] = Field(default=None)
    share_secret_key: Optional[str] = Field(default=None)
    items: Optional[List[PsonoDataStoreItem]] = Field(default=list())
    folders: Optional[List[PsonoDataStoreFolder]] = Field(default=list())
    
class PsonoShareIndexItem(BaseModel):
    secret_key: str
    paths: List[List[str]]

class PsonoShare(MyBase):
    id: str
    user_id: str
    datastore: PsonoDataStore
    rights: PsonoRights

class PsonoRights(MyBase):
    read: bool
    write: bool
    grant: bool

class PsonoShareStore(PsonoDataStoreFolder):
    id: Optional[str] = Field(exclude=True,default=None)

class PsonoDataStore(PsonoDataStoreFolder):
    # override the parent values that don't apply
    name: Optional[str] = Field(exclude=True,default=None)
    id: Optional[str] = Field(exclude=True,default=None)

    datastore_id: str
    secret_key: str = Field(exclude=True)
    share_index: Dict[str,PsonoShareIndexItem]
    items: Optional[List[PsonoDataStoreItem]] = Field(default=list())
    folders: Optional[List[PsonoDataStoreFolder]] = Field(default=list())



psono_type_list = {
    'website_password',
    'application_password',
    'bookmark',
    'credit_card',
    'environment_variables',
    'mail_gpg_own_key',
    'note',
    'totp'
}
def _psono_alias_generator(fieldname: str):
    for type in psono_type_list:
        if fieldname.startswith(type):
            alias =  fieldname.replace(type+ '_','')
            return alias
    return fieldname
def _psono_alias_generator_generator(secret_type: str):
    def callback(fieldname: str):
        return secret_type + '_' + fieldname
    return callback


class PsonoSecret(MyBase):
    secret_id: str = Field(exclude=True)
    secret_key: str = Field(exclude=True)
    custom_fields: Optional[List[PsonoCustomField]] = Field(default=None)
    type: str = Field(exclude=True)
    link_id: Optional[str] = Field(exclude=True,default=None)
    path: str = Field(exclude=True)
    tags: Optional[List[str]] = Field(default=None)
    title: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    def set_custom_field(self,name,value):
        for field in self.custom_fields:
            if field.name == name:
                field.value = value
    def get_custom_field(self,name,value):
        for field in self.custom_fields:
            if field.name == name:
                return field.value
    class Config:
        populate_by_name = True
        alias_generator=AliasGenerator(alias=_psono_alias_generator)


class PsonoWebsitePassword(PsonoSecret):
    allow_http: bool = Field(default=False)
    auto_submit: bool = Field(default=False)
    password: Optional[str] = Field(default=None)
    totp_algorithm: Optional[str] = Field(default=None)
    totp_digits: Optional[int] = Field(default=None)
    totp_period: Optional[int] = Field(default=None)
    url: Optional[str] = Field(default=None)
    url_filter: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    class Config:
        populate_by_name = True
        alias_generator=AliasGenerator(alias=_psono_alias_generator_generator('website_password'),serialization_alias=_psono_alias_generator_generator('website_password'))

class PsonoApplicationPassword(PsonoSecret):
    password: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    class Config:
        populate_by_name = True
        alias_generator=AliasGenerator(alias=_psono_alias_generator_generator('application_password'),serialization_alias=_psono_alias_generator_generator('application_password'))

class PsonoBookmark(PsonoSecret):
    url: str = Field(default=None)
    url_filter: str = Field(default=None)
    class Config:
        populate_by_name = True
        alias_generator=AliasGenerator(alias=_psono_alias_generator_generator('bookmark'),serialization_alias=_psono_alias_generator_generator('bookmark'))

class PsonoCreditCard(PsonoSecret):
    cvc: str = Field(default=None)
    name: str = Field(default=None)
    number: str = Field(default=None)
    valid_through: str = Field(default=None)
    notes: str = Field(default=None)
    class Config:
        populate_by_name = True
        alias_generator=AliasGenerator(alias=_psono_alias_generator_generator('credit_card'),serialization_alias=_psono_alias_generator_generator('credit_card'))

class PsonoEnvironmentVariable(PsonoSecret):
    key: str
    value: str

class PsonoEnvironmentVariables(PsonoSecret):
    variables: Optional[List[PsonoEnvironmentVariable]] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    class Config:
        populate_by_name = True
        alias_generator=AliasGenerator(alias=_psono_alias_generator_generator('environment_variables'),serialization_alias=_psono_alias_generator_generator('environment_variables'))

class PsonoGPGKey(PsonoSecret):
    type: str = 'mail_gpg_own_key'
    public: Optional[str] = Field(default=None)
    private: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)    
    name: Optional[str] = Field(default=None)
    notes: str = Field(default='')
    class Config:
        populate_by_name = True
        alias_generator=AliasGenerator(alias=_psono_alias_generator_generator('mail_gpg_own_key'),serialization_alias=_psono_alias_generator_generator('mail_gpg_own_key'))

class PsonoTOTP(PsonoSecret):
    type: str = 'totp'
    totp_algorithm: Optional[str] = Field(default=None)
    totp_code: Optional[str] = Field(default=None)
    totp_digits: Optional[int] = Field(default=None)
    totp_period: Optional[int] = Field(default=None)
    totp_notes: Optional[str] = Field(default=None)
    class Config:
        populate_by_name = True
        alias_generator=AliasGenerator(alias=_psono_alias_generator_generator('totp'),serialization_alias=_psono_alias_generator_generator('totp'))

class PsonoNote(PsonoSecret):
    type: str = 'note'
    notes: Optional[str] = Field(default=None)



PsonoTypeMap = {
    'website_password': PsonoWebsitePassword,
    'application_password': PsonoApplicationPassword,
    'bookmark': PsonoBookmark,
    'credit_card': PsonoCreditCard,
    'environment_variables': PsonoEnvironmentVariables,
    'mail_gpg_own_key': PsonoGPGKey,
    'note': PsonoNote,
    'totp': PsonoTOTP
}
def _psono_alias_generator(fieldname: str):
    for type in PsonoTypeMap:
        if fieldname.startswith(type):
            return fieldname.replace(type,'')
    return fieldname
    