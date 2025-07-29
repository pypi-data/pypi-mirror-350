from __future__ import annotations

import re  # noqa: F401
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, StrictBool
from sysnet_pyutils.models.general import LocationType, PersonTypeEnum, ListTypeBase, MetadataEssentialType

from persons_model.common import RedundantType, DepartmentType, ContactType, IssuingType, RegistryType, MemberType
from persons_model.tag import TagType


class PersonEntityLinkType(BaseModel):
    """
    Navázaný objekt
    """ # noqa: E501
    identifier: Optional[str] = Field(default=None, description="identifikátor uuid")
    code: Optional[str] = Field(default=None, description="Kód navázaného subjektu")
    name: Optional[str] = Field(default=None, description="Název navázaného subjektu")
    link_type: Optional[str] = Field(default=None, description="Typ vazby")


class PersonEntityEntryType(BaseModel):
    """
    Položka subjektu v kontextu
    """ # noqa: E501
    identifier: Optional[str] = Field(default=None, description="identifikátor uuid")
    person_type: Optional[PersonTypeEnum] = Field(default=None, description='Typ osoby (zdroj CRŽP)')
    name: Optional[str] = Field(default=None, description="Název nebo jméno osoby")
    is_admin: Optional[StrictBool] = Field(default=False, description="Je uživatel administrátorem?")
    membership: Optional[str] = Field(default=None, description="Typ členství (admin/representative/employee)")
    tags: Optional[TagType] = Field(default=None, description="Seznam tagů objektu")


class PersonEntityListType(ListTypeBase):
    """
    Seznam vrácených subjektů
    """ # noqa: E501
    hits: Optional[int] = Field(default=None, description="celkový počet vybraných položek")
    entries: Optional[List[Optional[PersonEntityEntryType]]] = Field(default=None, description='Položky seznamu')


class PersonEntityBaseType(BaseModel):
    """
    Osoba, subjekt. Fyzická nebo právnická osoba.
    """ # noqa: E501
    code: Optional[str] = Field(default=None, description="Kód subjektu")
    ico: Optional[str] = Field(default=None, description="Jiný identifikátor")
    birthdate: Optional[datetime] = Field(default=None, description="Datum narození")
    person_type: Optional[PersonTypeEnum] = Field(default=None, description='Typ osoby (zdroj CRŽP)')
    name: Optional[str] = Field(default=None, description="Název nebo jméno osoby")
    full_name: Optional[str] = Field(default=None, description="Plné jméno. U fyzických osob včetně titulů")
    headquarters: Optional[LocationType] = Field(default=None, description='Sídlo osoby')
    redundant_record: Optional[RedundantType] = Field(default=None, description='Dvojí evidence (pokud je v CRŽP chyba)')
    department: Optional[DepartmentType] = Field(default=None, description='Útvar organizace')
    addresses: Optional[List[Optional[LocationType]]] = Field(default=None, description="další adresy")
    address_printable: Optional[str] = Field(default=None, description="Adresa pro tisk")
    representative: Optional[ContactType] = Field(default=None, description='Statutární zástupce')
    contacts: Optional[List[Optional[ContactType]]] = Field(default=None, description="Další kontaktní osoby")
    note: Optional[str] = Field(default=None, description="Poznámka")
    issuing: Optional[List[Optional[IssuingType]]] = Field(default=None, description="Osoba je autoritou vydávající nějaké dokumenty")


class PersonEntityType(PersonEntityBaseType):
    """
    Osoba, subjekt. Fyzická nebo právnická osoba.
    """
    identifier: Optional[str] = Field(default=None, description="identifikátor uuid")
    pid: Optional[str] = Field(default=None, description="identifikátor PID")
    registry: Optional[RegistryType] = Field(default=None, description='Reference na identifikační údaje')
    admins: Optional[List[str]] = Field(default=None, description="Správci subjektu")
    members: Optional[List[Optional[MemberType]]] = Field(default=None, description="Členové subjektu")
    linked_persons: Optional[List[Optional[PersonEntityLinkType]]] = Field(default=None, description="Vazba na jiný subjekt")
    tags: Optional[TagType] = Field(default=None, description="Seznam tagů")
    document: Optional[MetadataEssentialType] = Field(default=None, description='Document metadata')
