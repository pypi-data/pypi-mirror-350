from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from persons_model.person_entity import PersonEntityEntryType
from persons_model.role import RoleEntryType


class ContextRolesType(BaseModel):
    # Role uživatele nebo subjektu v kontextu
    admin: Optional[List[Optional[RoleEntryType]]] = Field(default=[], description='Tyto role uživatel nebo subjekt spravuje')
    holder: Optional[List[Optional[RoleEntryType]]] = Field(default=[], description='Tyto role uživatel nebo subjekt  vlastní')


class ContextPersonsType(BaseModel):
    # Spravované subjekty uživatelem
    admin: Optional[List[Optional[PersonEntityEntryType]]] = Field(default=[], description='Tyto subjekty uživatel spravuje')
    contact: Optional[List[Optional[RoleEntryType]]] = Field(default=[], description='V těchto subjektech je uživatel kontaktní osobou')
    member: Optional[List[Optional[RoleEntryType]]] = Field(default=[], description='V těchto subjektech je uživatel členem')
    representative: Optional[List[Optional[RoleEntryType]]] = Field(default=[], description='V těchto subjektech je uživatel členem')


class ContextIndividualType(BaseModel):
    # Kontext konkrétního jednotlivce
    identifier: Optional[str] = Field(default=None, description="identifikátor uuid")
    username: Optional[str] = Field(default=None, description="Uživatelské jméno osoby")
    roles: Optional[ContextRolesType] = Field(default=None, description='Role uživatele v kontextu')
    persons: Optional[ContextPersonsType] = Field(default=None, description='Spravované subjekty uživatelem')
