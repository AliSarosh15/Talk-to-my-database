from app.database import engine
from app.schema.extractor import get_database_schema

SCHEMA_CACHE={}

def set_schema(schema):
    global SCHEMA_CACHE
    SCHEMA_CACHE=schema

def get_schema():
    return SCHEMA_CACHE








# import re

# def parse_intent(text:str,schema:dict):
#     text=text.lower()

#     intent={
#         "action":"select",
#         "table":None,
#         "limit":10
#     }

#     #detect limits

#     limit_match=re.search(r"\b(\d+)\b",text)
#     if limit_match:
#         intent["limit"]=int(limit_match.group(1))

#     #detect tables name

#     for table in schema.keys():
#         if table in text:
#             intent["table"]=table
#             break
    

#     return intent