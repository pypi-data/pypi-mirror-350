from pydantic import BaseModel

class ShopifyCredentials(BaseModel):
    hostname: str
    accessToken: str
