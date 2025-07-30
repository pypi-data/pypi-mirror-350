from pydantic import BaseModel
from zodable_sample_package.digital.guimauve.example.Country import Country

class Address(BaseModel):
    street: str
    city: str
    country: Country
