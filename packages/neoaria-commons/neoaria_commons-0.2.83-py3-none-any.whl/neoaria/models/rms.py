import random
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from enum import Enum
import json, zlib, uuid, time

import requests

class ApplicationFunction(BaseModel): 
    id:str = None    # that is UUID type 4
    name:str = None
    allow:bool = False
    conditions: Optional[dict] = None

class Applications(BaseModel):
    id:str = None # 고유 ID
    name:str = None # 어플리케이션 이름
    functions: List[ApplicationFunction]= None # 어플리케이션 비즈니스 목록

    def getFunction(self, id:str) -> ApplicationFunction:
        for func in self.functions:
            if func.id == id:
                return func
        return None

class DefaultApplications(BaseModel):
    
    id:str = None # 고유 ID
    name:str = None # 어플리케이션 이름
    functions: List[ApplicationFunction]= None # 어플리케이션 비즈니스 목록

    def getFunction(self, id:str) -> ApplicationFunction:
        for func in self.functions:
            if func.id == id:
                return func
        return None

class DefaultPermission(BaseModel):
    id: str = None # permission 고유 ID
    user_id: str = None # 사용자 ID
    entity_type: str
    entity_id: str
    created_at: int # permission 생성시간
    modificated_at: int = 0 # permission 수정시간
    applications: List[Applications] = None # 할당된 어플리케이션 목록
    
    def getPermissions(self) -> str:
        permissions = {}
        for app in self.applications:
            permissions[app.id] = {}
            for func in app.functions:
                permissions[app.id][func.id] = func.allow
        
        return permissions
    
    def getPermissionsDict(self) -> dict:
        permissions = {}
        for app in self.applications:
            permissions[app.id] = {}
            for func in app.functions:
                permissions[app.id][func.id] = func
        
        return permissions

class DefaultAccount(BaseModel):
    id: str
    name: str
    tel: Optional[str] = None
    email: str
    department_id: Optional[str] = None
    department_ids: Optional[List[str]] = None
    organization_id: Optional[str] = None
    organization_ids: Optional[List[str]] = None
    created_at: int
    modificated_at: int = 0
    is_deleted: bool = False

    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.name:
            return False
        
        if not self.email:
            return False
        
        if not self.created_at:
            return False
        
        return True
    
class Address(BaseModel):
    zipCode: Optional[str] = None
    address: Optional[str] = None
    detail: Optional[str] = None

class DefaultDepartment(BaseModel):
    id: str
    name: str
    tel: Optional[str] = None
    manager_id: Optional[str] = None
    organization_id: str
    created_at: int
    modificated_at: int
    is_deleted: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.name:
            return False

        if not self.created_at:
            return False
        
        return True
    
class DefaultOrganizaion(BaseModel):
    id: str
    name: str
    address: Address
    tel: Optional[str] = None
    manager_id: Optional[str] = None
    created_at: int
    modificated_at: int
    is_deleted: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.name:
            return False
        
        if not self.created_at:
            return False
        
        return True

class DeployStatus(Enum):
    DEPLOYED = "Deployed" # 배포
    DEPLOYMENTSTOPPED = "DeploymentStopped" # 배포중단
    NOTDEPLOYED = "NotDeployed" # 미배포

class ElementStatus(Enum):
    REVIEWREQUESTED = "ReviewRequested" # 검토요청
    REVIEWREJECTED = "ReviewRejected" # 검토반려
    REVIEWCOMPLETED = "ReviewCompleted" # 검토완료
    APPROVED = "Approved" # 승인완료
    APPROVEDREJECTED = "ApprovalRejected" # 승인반려
    EDITING = "Editing" # 수정중
    INITIALIZED = "Initialized" # 배포 (서비스 되고 있는 상태)
    APPROVALREQUESTPROCESSING = "ApprovalRequestProcessing" # 승인 요청 처리 중
    APPROVALREQUESTERROR = "ApprovalRequestError" # 승인 요청 오류
    APPROVALREQUESTED = "ApprovalRequested" # 승인 요청
    APPROVALPROCESSING = "ApprovalProcessing" # 승인 요청 중
    APPROVALERROR = "ApprovalError" # 승인 오류

class Language(Enum):
    KO = "ko"
    EN = "en"
    AU = "en_AU"
    CN = "zh_CN"
    TW = "zh_TW"
    DE = "de"
    FR = "fr"
    ES = "es"
    RU = "ru"
    JA = "ja"
    ID = "id"
    AR = "ar"

class FormType(Enum):
    FORMAL = "Formal"
    CASUAL = "Casual"

class CIDType(Enum):
    UUID = "uuid"
    FLOAT = "float"
    STRING = "string"
    UNKNOWN = "unknown"

class ContentsType(Enum):
    FORMALCONTENTS = "FormalContents"
    CASUALCONTENTS = "CasualContents"
    IMAGECONTENTS = "ImageContents"
    VIDEOCONTENTS = "VideoContents"

class ImageContentsType(Enum):
    GALLERY = "Gallery"
    RESOURCE = "Resource"

class TranslationStatus(Enum):
    NONE = "None" # 번역 전
    DONE = "Done" # 번역완료
    WORKING = "Working" # 번역 중
    
class DeployStatusModel(BaseModel):
    status: DeployStatus
# 각각의 value 모델 정의
class BaseValue(BaseModel):
    value: Union[str, int, float, None]
    VT: Optional[str] = None
    TT: Optional[str] = None

class JsonValue(BaseModel):
    value: Union[dict, str]  # value가 dict 형태일 때 사용
    VT: Optional[str] = None
    TT: Optional[str] = None

# CID 모델 정의
class CID(BaseModel):
    v1: BaseValue
    v2: BaseValue
    v3: BaseValue

class CIDField(BaseModel):
    title: str
    value: CID

# Language 모델 정의
class LanguageValuesModel(BaseModel):
    code: Optional[BaseValue] = None
    currentLanguage: Optional[JsonValue] = None
    masterId: Optional[BaseValue] = None
    translationId: Optional[BaseValue] = None
    translationStatus: Optional[JsonValue] = None

class Language(BaseModel):
    title: str
    value: LanguageValuesModel

class Classification(BaseModel):
    firstClassification: JsonValue
    secondClassification: JsonValue
    thirdClassification: JsonValue

class ClassificationFields(BaseModel):
    title: str
    value: Classification

# Information 모델 정의
class InformationValuesModel(BaseModel):
    version: Optional[BaseValue] = None
    title: BaseValue
    typeId: BaseValue
    viewCount: Optional[BaseValue] = None
    informationStatus: Optional[BaseValue] = None
    fileName: Optional[BaseValue] = None
    travelTime: Optional[BaseValue] = None
    type: BaseValue

class AddressValuesModel(BaseModel):
    zipcode: BaseValue
    address: BaseValue

class AreaValuesModel(BaseModel):
    legalAreaCode: JsonValue
    legalSigunguCode: JsonValue
    legalDongCodes: JsonValue
    legalBdongCode: JsonValue

class Information(BaseModel):
    title: str
    value: InformationValuesModel


class Area(BaseModel):
    title: str
    value: AreaValuesModel

class WGS84(BaseModel):
    level: BaseValue
    latitude: BaseValue
    longitude: BaseValue

class WGS84Field(BaseModel):
    title: str
    value: WGS84

class WGS84Model(BaseModel):
    wgs84: WGS84Field

class Map(BaseModel):
    title: str
    value: WGS84Model
    
class CurrentStatus(BaseModel):
    currentStatus: BaseValue

class Status(BaseModel):
    title: str
    value: CurrentStatus

# Base 모델 정의
class BaseFields(BaseModel):
    language: Optional[Language] = None
    classification: Optional[ClassificationFields] = None
    information: Optional[Information] = None
    address: Optional[Address] = None
    area: Optional[Area] = None
    map: Optional[Map] = None
    status: Optional[Status] = None

class BaseField(BaseModel):
    title: str
    value: BaseFields

# Alram 모델 정의
class Alram(BaseModel):
    id: Optional[str] = None
    message: Optional[str] = None
    target: Optional[DefaultAccount] = None    # account
    status: Optional[str] = None
    sended_at: Optional[int] = None
    reservated_at: Optional[int] = None
    order: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.sended_at:
            self.sended_at = int(time.time() * 1000)

        if not self.reservated_at:
            self.reservated_at = int(time.time() * 1000)

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.message:
            return False
        
        if not self.target.validate:
            return False
        
        if not self.sended_at:
            return False
        
        if not self.reservated_at:
            return False 
        
        return True

# Toplink 모델 정의
class Toplink(BaseModel):

    id: Optional[str] = None
    at: Optional[int] = None
    end: Optional[int] = None
    order: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.at:
            self.at = self.at.strftime('%Y-%m-%d %H:%M:%S')
        if self.end:
            self.end = self.end.strftime('%Y-%m-%d %H:%M:%S')

# Notify 모델 정의
class Notify(BaseModel):

    id: Optional[str] = None
    content: Optional[str] = None
    writer: Optional[str] = None
    created_at: Optional[int] = None
    modificated_at: Optional[int] = None
    topLink: Optional[Toplink] = None
    order: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

        if self.topLink:
            self.topLink = Toplink(**self.topLink.model_dump())

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.content:
            return False
        
        if not self.writer:
            return False

        if not self.created_at:
            return False
        
        if self.modificated_at is None:
            return False 
        
        if not self.topLink:
            return False
        
        if not self.topLink.id:
            return False
        
        if not self.topLink.at:
            return False
        
        if not self.topLink.end:
            return False
        
        if not self.topLink.order:
            return False
        
        if not self.order:
            return False
        
        return True

# Advertisement 모델 정의
class Advertisement(BaseModel):
    id: Optional[str] = None
    link: Optional[str] = None
    imagePath: Optional[str] = None
    created_at: Optional[int] = None
    modificated_at: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.link:
            return False
        
        if not self.imagePath:
            return False

        if not self.created_at:
            return False
        
        if self.modificated_at is None:
            return False 
        
        return True

# Banner 모델 정의
class Banner(BaseModel):

    id: Optional[str] = None
    contentId: Optional[str] = None
    state: Optional[str] = None
    created_at: Optional[int] = None
    modificated_at: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.contentId:
            return False
        
        if not self.state:
            return False

        if not self.created_at:
            return False
        
        if self.modificated_at is None:
            return False
        
        return True

# Menu 모델 정의    
class Menu(BaseModel):

    id: Optional[str] = None
    name: Optional[str] = None
    icon: Optional[str] = None
    children: Optional[List['Menu']] = None # type: ignore
    created_at: Optional[int] = None
    modificated_at: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.name:
            return False
        
        if not self.icon:
            return False

        if not self.created_at:
            return False
        
        if self.modificated_at is None:
            return False

        return True

# Article 정의
class Article(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True

# Category 정의
class Category(BaseModel):

    id: Optional[str] = str(uuid.uuid4())
    name: Optional[str] = None
    type: Optional[str] = None
    children: Optional[List['Category']] = None # type: ignore
    created_at: Optional[int] = None
    modificated_at: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.name:
            return False
        
        if not self.type:
            return False
        
        if not self.created_at:
            return False
    
        if self.modificated_at is None:
            return False
         
        return True

# Course 정의
class Course(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True    

# Event 정의
class Event(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True

# Festival 정의
class Festival(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True
    
# Image 정의
class Image(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True
    
# OnlineEvent 정의
class OnlineEvent(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True

# Show 정의
class Show(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True

# ThemePath 정의
class ImagePath(BaseModel):
    cid: str
    imageUrl: str
    imageDepotUrl: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# child 정의
class ThemeChild(BaseModel):
    cid: str
    categoryId: str
    contentsName: str
    address: str
    baseCategoryName: str
    type: str
    introduction: str
    id: Optional[str] = None
    depotId: Optional[str] = None
    fileName: Optional[str] = None
    koglType: Optional[str] = None
    depotFileId: Optional[str] = None
    imagePathList: List[ImagePath] = Field(default_factory=list)
    tid: Optional[str] = None
    category2: Optional[str] = None
    category3: Optional[str] = None
    telephone: Optional[str] = None
    homepage: Optional[str] = None
    copyright: Optional[str] = None
    registrationTime: int = 0
    modificationTime: int = 0
    url: Optional[str] = None
    videoDuration: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Writer 정의
class ThemeWriter(BaseModel):
    id: str
    name: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Theme 정의
class Theme(BaseModel):
    id: str
    registrationTime: int
    modificationTime: int
    pavilionId: str
    citizenId: str
    cineroomId: str
    audienceId: str
    actorId: str
    name: str
    parentId: str
    elementTypeId: Optional[str] = None
    writer: ThemeWriter = Field(default_factory=ThemeWriter)
    lastUpdater: ThemeWriter = Field(default_factory=ThemeWriter)
    lastUpdateTime: int = 0
    used: bool
    cineroomName: Optional[str] = None
    type: Optional[str] = None
    langUsed: bool
    existChild: bool
    marketingType: Optional[str] = None
    cmsCategoryId: Optional[str] = None
    idPaths: List[str] = Field(default_factory=list)
    folderType: bool = False
    imagePath: Optional[str] = None
    bannerImgPath: Optional[str] = None
    publicType: bool
    children: Optional[List[ThemeChild]] = None
    contents: List[ThemeChild] = Field(default_factory=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self) -> bool:
        if not self.id:
            return False
        
        if not self.pavilionId:
            return False
        
        if not self.citizenId:
            return False
        
        if not self.cineroomId:
            return False
        
        if not self.audienceId:
            return False
        
        if not self.actorId:
            return False
        
        if not self.name:
            return False
        
        if not self.imagePath:
            return False
        
        if not self.bannerImgPath:
            return False
        
        return True        
    
# TouristDestination 정의
class TouristDestination(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True    

# Culture 정의
class Culture(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True    

# Food 정의
class Food(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True    

# Accommodation 정의
class Accommodation(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True    

# Shopping 정의
class Shopping(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True    

# Leisure 정의
class Leisure(BaseModel):
    cid: CIDField
    base: BaseField

    def validate(self) -> bool:
        if not self.cid.value.v3.value:
            return False
        
        if not self.base.value.language.value.code.value:
            return False
        
        if not self.base.value.classification.value.firstClassification.value:
            return False
        
        if not self.base.value.classification.value.secondClassification.value:
            return False
        
        if not self.base.value.classification.value.thirdClassification.value:
            return False
        
        if not self.base.value.information.value.title.value:
            return False
        
        if not self.base.value.information.value.type.value:
            return False
        
        if not self.base.value.information.value.typeId.value:
            return False
        
        if not self.base.value.address.value.zipcode.value:
            return False
        
        if not self.base.value.address.value.address.value:
            return False
        
        if not self.base.value.area.value.legalAreaCode.value:
            return False
        
        if not self.base.value.area.value.legalSigunguCode.value:
            return False
        
        if not self.base.value.area.value.legalDongCodes.value:
            return False
        
        if not self.base.value.area.value.legalBdongCode.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.level.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.latitude.value:
            return False
        
        if not self.base.value.map.value.wgs84.value.longitude.value:
            return False
        
        if not self.base.value.status.value.currentStatus.value:
            return False
        
        return True    

# Deployment 정의
class Deployment(BaseModel):

    id: Optional[str] = None
    contentId: Optional[str] = None
    state: Optional[str] = None
    created_at: Optional[int] = None
    modificated_at: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.contentId:
            return False
        
        if not self.state:
            return False

        if not self.created_at:
            return False
        
        if self.modificated_at is None:
            return False
        
        return True
    
# FileModel 정의
class FileModel(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    fileSize: Optional[int] = None
    extension: Optional[str] = None
    watermarkApplied: Optional[bool] = None
    watermarkImage: Optional[str] = None
    copyrightApplied: Optional[bool] = None
    copyrightText: Optional[str] = None
    resolution: Optional[str] = None
    metaInfo: Optional[List[dict]] = None
    created_at: Optional[int] = None
    modificated_at: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.name:
            return False
        
        if not self.fileSize:
            return False
        
        if not self.extension:
            return False
        
        if not self.watermarkApplied:
            return False
        
        if not self.watermarkImage:
            return False
        
        if not self.copyrightApplied:
            return False
        
        if not self.copyrightText:
            return False
        
        if not self.resolution:
            return False   
            
        if not self.metaInfo:
            return False       
        
        if not self.created_at:
            return False       
        
        if self.modificated_at is None:
            return False       
        
        return True

# Log 모델 정의
class Log(BaseModel):
    id: Optional[str] = None
    message: Optional[str] = None
    createdBy: Optional[str] = None
    created_at: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.message:
            return False
        
        if not self.createdBy:
            return False

        if not self.created_at:
            return False
                
        return True

# Notify 모델 정의
class Notify(BaseModel):
    
    id: Optional[str] = None
    content: Optional[str] = None
    writer: Optional[str] = None
    created_at: Optional[int] = None
    modificated_at: Optional[int] = None
    topLink: Optional[Toplink] = None
    order: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

        if not self.modificated_at:
            self.modificated_at = 0

        if self.topLink:
            self.topLink = Toplink(**self.topLink.model_dump())

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.content:
            return False
        
        if not self.writer:
            return False

        if not self.created_at:
            return False
        
        if self.modificated_at is None:
            return False 
        
        if not self.topLink:
            return False
        
        if not self.topLink.id:
            return False
        
        if not self.topLink.at:
            return False
        
        if not self.topLink.end:
            return False
        
        if not self.topLink.order:
            return False
        
        if not self.order:
            return False
        
        return True

# Search 모델 정의
class Search(BaseModel):

    type: Optional[str] = None
    targetField: Optional[str] = None
    defaultTargetField: Optional[str] = None
    resultField: Optional[str] = None
    startValue: Optional[str] = None
    dataSize: Optional[str] = None
    keyword: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self) -> bool:

        if not self.type:
            return False
        
        if not self.targetField:
            return False
        
        if not self.defaultTargetField:
            return False

        if not self.resultField:
            return False
        
        if not self.startValue:
            return False 
        
        if not self.dataSize:
            return False
        
        if not self.keyword:
            return False
        
        return True

# Statistics 모델 정의    
class Statistics(BaseModel):

    id: Optional[str] = str(uuid.uuid4())
    organizationName: Optional[str] = None
    registerationType: Optional[str] = None
    created_at: Optional[int] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.created_at:
            self.created_at = int(time.time() * 1000)

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.organizationName:
            return False
        
        if not self.registerationType:
            return False
        
        return True
    
# Template 모델 정의
class Template(BaseModel):

    id: Optional[str] = str(uuid.uuid4())
    name: Optional[str] = None
    lang: Optional[str] = None
    version: Optional[str] = None
    detail: Optional[dict] = None
    creatorId: Optional[str] = None
    creationTime: Optional[str] = None
    modificationTime: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.creationTime is None:
            now = datetime.now()

            self.creationTime = int(time.mktime(now.timetuple()) * 1000 + now.microsecond / 1000)

    def validate(self) -> bool:
        
        if not self.name:
            return False
        
        if not self.lang:
            return False

        if not self.version:
            return False
        
        if not self.detail:
            return False

        # if not self.creatorId:
        #     return False
        
        return True

# Translation 모델 정의
class Translation(BaseModel):

    id: Optional[str] = None
    originLang: Optional[str] = None
    targetText: Optional[str] = None
    targetLang: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self) -> bool:

        if not self.id:
            return False
        
        if not self.originLang:
            return False
        
        if not self.targetText:
            return False

        if not self.targetLang:
            return False
        

        return True

# cid 구분 펑션
def determine_cid(value) -> CIDType:
        # Check if the value is a UUID
        try:
            uuid_obj = uuid.UUID(value)
            return CIDType.UUID
        except (ValueError, TypeError, AttributeError):
            pass

        # Check if the value is a number
        try:
            float_value = float(value)
            return CIDType.FLOAT
        except (ValueError, TypeError):
            pass

        # Check if the value is a string
        if isinstance(value, str):
            return CIDType.STRING

        return CIDType.UNKNOWN

def gen_v1_cid(
    url: str = None,
    params: Dict = None,
    timeout: int = 10
) -> Dict[str, Union[str, bool]]:
    """V1 방식의 CID 생성 (API 기반)"""

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        sequence = data.get("sequence")
        
        if sequence:
            return {"success": True, "data": sequence}
        return {"success": False, "message": "응답에 sequence 값이 없습니다."}
            
    except requests.Timeout:
        return {"success": False, "message": "API 요청 시간이 초과되었습니다."}
    except requests.ConnectionError:
        return {
            "success": False,
            "message": f"서버({url})에 연결할 수 없습니다. 네트워크 연결을 확인해주세요."
        }
    except requests.RequestException as e:
        return {"success": False, "message": f"API 호출 중 오류가 발생했습니다: {str(e)}"}
    except ValueError as e:
        return {"success": False, "message": f"응답 데이터 처리 중 오류가 발생했습니다: {str(e)}"}


def gen_v2_cid(seed: Optional[int] = None) -> str:
    """V2 방식의 CID 생성 (Base62 기반)"""
    BASE_LIST = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    MIN_VALUE = 0
    MAX_VALUE = 61
    ID_LENGTH = 6

    if seed is None:
        seed = int(time.time() * 1000)
    
    random.seed(seed)
    
    id_chars = [
        BASE_LIST[
            random.randint(MIN_VALUE, MAX_VALUE)
        ]
        for _ in range(ID_LENGTH)
    ]
    
    return "".join(id_chars)


def gen_v3_cid() -> uuid.UUID:
    """V3 방식의 CID 생성 (UUID)"""
    return uuid.uuid4()