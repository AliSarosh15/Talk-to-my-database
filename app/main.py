from fastapi import FastAPI, HTTPException,Depends
from app.database import engine,get_db
from app.schema.extractor import get_database_schema
from app.schema.schema_store import set_schema,get_schema
from contextlib import asynccontextmanager
from app.schema.semantic_store import load_semantic_schema, get_semantic_schema,set_semantic_schema
from app.nlp.intent_parser import parse_intent
from fastapi import Query
from app.query_builder import build_query
from sqlalchemy.orm import Session
from app.executor import execute_query
import traceback
from app.llm_parser import parse_with_llm

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Extracting db schema ......")
    
 #step 1- extract db schema
    schema=get_database_schema(engine)
    set_schema(schema)

    print("db schema loaded:",schema)

    #step2-build semantic schema
    semantic_schema=load_semantic_schema(schema)
    set_semantic_schema(semantic_schema)
    print("sematic schema loaded")

    yield



app= FastAPI(title="Talk to my Database",lifespan=lifespan)



@app.get("/schema")
def show_schema():
    return get_schema()

@app.get("/semantic_schema")
def show_semantic_schema():
    return get_semantic_schema()

@app.get("/query")
def query_db(q: str,db:Session=Depends(get_db)):
    try:
        semantic_schema=get_semantic_schema()
        
#STEP 1 -RULE BASED FIRST
        intent=parse_intent(q,semantic_schema)
        print("RULE INTENT:", intent)
        print("CHECKING INTENT VALIDITY..")
        print("tables:",intent.get("tables"))
        print("operation", intent.get("operation"))
        #step 2 -LLM FALLBACK(ONLY IF WEAK INTENT)
        if (
            not intent
            or "tables" not in intent
            or not isinstance(intent.get("tables"), list)
            or len(intent.get("tables"))==0
            ):
            print("ENTERING LLM FALLBACK")
            try:
                print("Falling back to llm...")
                intent= parse_with_llm(q, semantic_schema)
                print("LLM INTENT:", intent)

                if not intent or not intent.get("tables"):
                    raise ValueError("LLM could not understand query properly")
            except Exception as e:
                print("LLM failed, falling back:", e)
                raise ValueError("Could not understand query")
            
        print("FINAL INTENT:", intent)
        #step3 Build SQL
        query,params=build_query(intent,semantic_schema)
        #step 4 execute
        result=execute_query(db,query,params)

        return {
            "success":True,
            "query":str(query),
            "count":len(result),
            "data":result
        }
    except ValueError as ve:
        #user mistake (bad query)
        raise HTTPException(status_code=400,detail=str(ve))
    except Exception as e:
        traceback.print_exc()

        #server issues
        raise HTTPException(status_code=500,detail=str(e))
    


# @app.get("/schema/[table_name]")
# def read_table_schema(table_name:str):
#     schema=get_database_schema(engine)

#     if table_name not in schema:
#         raise HTTPException(
#             status_code=404,
#             detail="table not found"
#         )
    
#     return{
#         "table":table_name,
#         "columns":schema[table_name]
#     }

# #for query 

# @app.post("/intent")
# def get_intent(query:IntentRequest):
#     schema=get_database_schema(engine)
#     intent= parse_intent(query.text,schema)
 
#     if not intent["table"]:
#         raise HTTPException(status_code=400,detail="table not found in query")
    
#     return intent
