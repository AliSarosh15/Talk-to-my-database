from sqlalchemy import inspect


def get_database_schema(engine):
    inspector= inspect(engine)

    tables= inspector.get_table_names()
    print("tables found :",tables)

    schema={}

    for table_name in tables:
        schema[table_name]={
            "columns":{},
            "primary_key":[],
            "foreign_keys":[]
        }
#COLUMNs
        for column in inspector.get_columns(table_name):
            schema[table_name]["columns"][column["name"]]={
                "type":str(column["type"]),
                "nullable":column["nullable"]
            }
#PRIMARY KEYS
        schema[table_name]["primary_key"]=inspector.get_pk_constraint(table_name).get("constrained_columns",[])


#foreign keys

        for fk in inspector.get_foreign_keys(table_name):
            schema[table_name]["foreign_keys"].append({
                "column":fk["constrained_columns"][0],
                "ref_table":fk["referred_table"],
                "ref_column":fk["referred_columns"][0]
            })

    return schema

#acts as systems eyes


