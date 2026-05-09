SEMANTIC_SCHEMA={}

def set_semantic_schema(schema):
    global SEMANTIC_SCHEMA
    SEMANTIC_SCHEMA=schema

def get_semantic_schema():
    return SEMANTIC_SCHEMA


def generate_table_aliases(table_name):
    mapping={
        "users":["customers","clients","people","users"],
        "orders":["purchases","transactions","payments","orders"]
    }
    return mapping.get(table_name,[table_name])


def generate_column_aliases(column_name):
    mapping={
        "name":["name","full name"],
        "created_at":["created date", "signup date"],
        "email":["email"],
        "role":["role"],
        "user_id":["user id", "customer id","client id"],
        "price":["cost","amount","total","spend"],
        "status":["status"],
        "id":["id","identifier"]
    }

    return mapping.get(column_name,[column_name])

def load_semantic_schema(raw_schema):
    global SEMANTIC_SCHEMA
    semantic_schema={}
    for table,meta in raw_schema.items():
        semantic_schema[table]={
            "aliases": [],
            "metrics":[],
            "time_columns":[],
            "columns":{},
            "relations":meta.get("foreign_keys",[])

        }
        if table.endswith("s"):
            semantic_schema[table]["aliases"].append(table[:-1])
        
        semantic_schema[table]["aliases"].extend(generate_column_aliases(table))

        #column semantics
        for col in meta["columns"]:
            col_lower=col.lower()
            if col_lower in ["created_at","updated_at","date","timestamp"]:
                semantic_schema[table]["time_columns"].append(col)
            
            if col_lower in ["amount","price","total","cost"]:
                semantic_schema[table]["metrics"].append(col)
            #column aliases
            semantic_schema[table]["columns"][col]=generate_column_aliases(col)
            
    SEMANTIC_SCHEMA=semantic_schema

    return semantic_schema


