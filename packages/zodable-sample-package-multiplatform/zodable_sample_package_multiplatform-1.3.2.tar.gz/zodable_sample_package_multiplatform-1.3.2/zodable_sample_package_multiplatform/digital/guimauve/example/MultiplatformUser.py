from pydantic import BaseModel
from uuid import UUID
from zodable_sample_package_multiplatform.digital.guimauve.example.MultiplatformType import MultiplatformType

class MultiplatformUser(BaseModel):
    id: UUID
    type: MultiplatformType
