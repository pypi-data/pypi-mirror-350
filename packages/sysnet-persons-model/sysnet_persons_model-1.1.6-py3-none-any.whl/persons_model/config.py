from typing import Optional

from pydantic import StrictBool, BaseModel


class ConfigType(BaseModel):
    """
    PutConfigRequest
    """ # noqa: E501
    cache: Optional[StrictBool] = None
