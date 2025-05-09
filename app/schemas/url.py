from pydantic import BaseModel, HttpUrl
from datetime import datetime

# Description:
#   Inputs and outputs for URL operations.
# Inputs:
#   original_url: validated HTTP URL to shorten.
# Outputs:
#   id: database record identifier.
#   original_url: the original URL.
#   short_path: the generated short URL path.
#   created_at: timestamp when record was created.
#   visit_count: number of times the short URL was accessed.
class UrlCreate(BaseModel):
    original_url: HttpUrl

class UrlInfo(BaseModel):
    id: int
    original_url: HttpUrl
    short_path: str
    created_at: datetime
    visit_count: int
