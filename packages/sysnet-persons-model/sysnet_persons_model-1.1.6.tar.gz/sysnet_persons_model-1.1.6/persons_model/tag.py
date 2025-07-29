from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field
from sysnet_pyutils.models.general import ListTypeBase


class TagItemType(BaseModel):
    """
    Značka
    """
    tag: Optional[str] = Field(default=None, description="Vlastní značka (Permity, RL, Stanoviska)")
    color: Optional[str] = Field(default=None, description="HTML kód barvy tagu")


class TagListType(ListTypeBase):
    """
    Seznam vrácených tagů
    """
    hits: Optional[int] = Field(default=None, description="celkový počet vybraných položek")
    entries: Optional[List[Optional[TagItemType]]] = None


class TagType(BaseModel):
    """
    Seznam tagů v datovém objektu
    """
    taglist: Optional[List[Optional[TagItemType]]] = None

    def has_tag(self, tag_name: str) -> bool:
        if self.taglist is None:
            return False
        for item in self.taglist:
            if item.tag == tag_name:
                return True
        return False

    def add_tag(self, tag: TagItemType) -> bool:
        out = False
        if tag is None:
            return out
        if self.taglist is None:
            self.taglist = []
            out = True
        if not self.has_tag(tag.tag):
            self.taglist.append(tag)
            out = True
        return out

    def remove_tag(self, tag_name: str) -> bool:
        out = False
        if self.taglist is None:
            return out
        for i, item in enumerate(self.taglist):
            if item.tag == tag_name:
                del self.taglist[i]
                out = True
                break
        return out
