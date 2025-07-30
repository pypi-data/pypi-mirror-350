from pydantic import BaseModel
from typing import Optional, Dict

class FileResponseBuilder(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    size: Optional[int] = 0
    ext: Optional[str] = None
    base64: Optional[str] = None
    url: Optional[str] = None
    mimeType: Optional[str] = None

    def to_json(self) -> str:
        return self.model_dump(mode='json')
    
    def to_dict(self) -> Dict[str,str]:
        return self.model_dump(mode='python')
