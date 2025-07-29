from __future__ import annotations

import re  # noqa: F401
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, SecretStr, StrictBool
from sysnet_pyutils.models.general import LocationType, ListTypeBase, MetadataEssentialType

from persons_model.common import ContactType, RegistryType
from persons_model.tag import TagType


class IndividualBaseType(BaseModel):
    """
    Osoba - lidská bytost, uživatel
    """
    name: Optional[str] = Field(default=None, description="Jméno osoby pro zobrazení")
    username: Optional[str] = Field(default=None, description="Uživatelské jméno osoby")
    dn: Optional[str] = Field(default=None, description="LDAP distinguished name")
    password: Optional[SecretStr] = Field(default=None, description="Přístupové heslo osoby")
    contact: Optional[List[Optional[ContactType]]] = Field(default=None, description="Seznam kontaktních osob")
    contact_default: Optional[int] = Field(default=0, description="Primární kontaktní údaje")
    address: Optional[List[Optional[LocationType]]] = Field(default=None, description='Seznam adres')
    address_default: Optional[int] = Field(default=0, description="Primární adresní údaje")
    address_printable: Optional[str] = Field(default=None, description="Adresa pro tisk")
    birthdate: Optional[datetime] = Field(default=None, description="Datum narození")
    gdpr: Optional[StrictBool] = Field(default=True, description="Udělen souhlas se zpracováním dat GDPR")
    note: Optional[str] = Field(default=None, description='Libovolná poznámka')


class IndividualEntryType(BaseModel):
    """
    Osoba - lidská bytost, uživatel
    """
    identifier: Optional[str] = Field(default=None, description="identifikátor uuid")
    name: Optional[str] = Field(default=None, description="Jméno osoby pro zobrazení")
    username: Optional[str] = Field(default=None, description="Uživatelské jméno osoby")
    tags: Optional[TagType] = Field(default=None, description="Seznam tagů objektu")


class IndividualType(IndividualBaseType):
    """
    Osoba - lidská bytost, uživatel
    """
    identifier: Optional[str] = Field(default=None, description="identifikátor uuid")
    pid: Optional[str] = Field(default=None, description="identifikátor PID")
    registry: Optional[RegistryType] = Field(default=None, description="Referenční registr")
    tags: Optional[TagType] = Field(default=None, description="Seznam tagů objektu")
    document: Optional[MetadataEssentialType] = Field(default=None, description="Metadata")


class IndividualListType(ListTypeBase):
    """
    Seznam vrácených uživatelů
    """
    hits: Optional[int] = Field(default=None, description="celkový počet vybraných položek")
    entries: Optional[List[Optional[IndividualEntryType]]] = Field(default=None, description='Položky seznamu')
