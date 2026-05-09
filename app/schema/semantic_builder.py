def build_semantic_schema(raw_schema):
    semantic_schema={}

    for table, meta in raw_schema.items():
        semantic_schema[table]={
            "aliases":[],
            "metrics":[],
            "time_columns":[],
            "columns":list(meta["columns"].keys()),
            "relations":meta["foreign_keys"]

        }

        #table aliases(auto+rule based)
        if table.endswith("s") and not table.endswith("ss"):
            semantic_schema[table]["aliases"].append(table[:-1])

        semantic_schema[table]["aliases"].extend([table,table.replace("_"," ")])

        #column sematics
        for col in meta["columns"]:
            col_lower=col.lower()
        #time detection
            if "date" in col_lower or "time" in col_lower:
                semantic_schema[table]["time_columns"].append(col)
        #metric detection
            if col_lower in ["amount","price","total","cost","spend","revenue","balance"]:
                semantic_schema[table]["metrics"].append(col)

    return semantic_schema