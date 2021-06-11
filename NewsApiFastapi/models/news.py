from pydantic import BaseModel

class News( BaseModel ):
    site : str
    title : str
    author : str
    desc : str
    content : str
    date : str
    img : str
    category : str
