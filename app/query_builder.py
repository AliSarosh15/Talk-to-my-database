from sqlalchemy import text

print("BUILD QUERY FUNC CALLED")

def build_query(intent:dict,semantic_schema:dict):
    print("INTENT RECIEVED:", intent)

    tables=intent.get("tables",[])
    filters=intent.get("filters",[])
    limit= intent.get("limit",10)
    operation=intent.get("operation","read")
    aggregation_column=intent.get("aggregation_column")
    group_by=intent.get("group_by")
    order_by=intent.get("order_by")
    order=intent.get("order", "desc")

    # display_column = None
    # if intent.get("group_by") == "user_id" and "users" in tables:
    #     display_column = "users.name"

#safety checks
    if not tables:
        raise ValueError("Table not found in query")
    
    if operation not in ["read", "count","avg","sum","min","max"]:
        raise ValueError("Invalid Operation")
    
    if aggregation_column == "amount" and "transactions" not in tables:
        tables.append("transactions")

    base_table=tables[0]

    #handle join
    join_clause=""
    if len(tables) >1:
        t1,t2=tables[0],tables[1]

        relations_t1=semantic_schema.get(t1, {}).get("relations", [])
        relations_t2=semantic_schema.get(t2, {}).get("relations", [])

        #check t1-->t2
        for rel in relations_t1:
            if rel.get("ref_table") ==t2:
                join_clause=f" JOIN {t2} ON {t1}.{rel['column']} ={t2}.{rel['ref_column']}"
                break
        #reverse relation check
        if not join_clause:
            for rel in relations_t2:
                if rel.get("ref_table") ==t1:
                    join_clause=f" JOIN {t2} ON {t2}.{rel['column']}= {t1}.{rel['ref_column']}"
                    break
        #if no relation found
        if not join_clause:
            print("DEBUG RELATIONS:")
            print(f"{t1} relations:",relations_t1)
            print(f"{t2} relations:",relations_t2)
            raise ValueError(f"No relation found between {t1} and {t2} tables")

    #count query
    if operation == "count":
        base_query=f"SELECT COUNT(*) AS count FROM {base_table}{join_clause}"
    elif operation in ["avg","sum","min","max"]:
        if not aggregation_column:
            for t in tables:
                cols=semantic_schema.get(t, {}).get("columns", {})
                for col_name, col_type in cols.items():
                    if col_type in ["integer", "float", "numeric"]:
                        aggregation_column=col_name
                        break
                if aggregation_column:
                    break

        col = aggregation_column

        if not col:
            raise ValueError("aggregation column missing")

        column_table = None
        for t in tables:
            if col in semantic_schema.get(t, {}).get("columns", {}):
                column_table = t
                break
        

        if not column_table:
            raise ValueError(f"Column '{col}' not found for aggregation")

        agg_alias = f"{operation}_{col}"

        # ✅ GROUP BY CASE
        if group_by:
            group_col = group_by

            group_table = None
            for t in tables:
                if group_col in semantic_schema.get(t, {}).get("columns", {}):
                    group_table = t
                    break

            if not group_table:
                raise ValueError(f"group_by column '{group_col}' not found")
            
            display_column=None
            relations=semantic_schema.get(group_table, {}).get("relations", [])
            
            for rel in relations:
                if rel["column"]==group_col:
                    ref_table=rel["ref_table"]

                    ref_columns=semantic_schema.get(ref_table, {}).get("columns", {})

                    if "name" in ref_columns:
                        display_column=f"{ref_table}.name"
                    elif "title" in ref_columns:
                        display_column=f"{ref_table}.title"
                    else:
                        display_column=f"{ref_table}.{rel['ref_column']}"
                    break
            if display_column:
                select_group=f"{display_column} AS display_value"
                group_by_clause=f"{group_table}.{group_col}, {display_column}"
            else:
                select_group=f"{group_table}.{group_col}"
                group_by_clause=f"{group_table}.{group_col}"


            base_query = f"""
                SELECT {select_group}, {operation.upper()}({column_table}.{col}) AS {agg_alias}
                FROM {base_table}{join_clause}
                GROUP BY {group_by_clause}
            """

        # ✅ NORMAL AGGREGATION
        else:
            base_query = f"""
                SELECT {operation.upper()}({column_table}.{col}) AS {agg_alias}
                FROM {base_table}{join_clause}
            """ 
 
    else:
        select_columns=[]
        for table in tables:
            cols=semantic_schema.get(table, {}).get("columns", {}).keys()
            for col in cols:
                alias=f"{table}_{col}"
                select_columns.append(f"{table}.{col} AS {alias}")
        select_clause=", ".join(select_columns)
        base_query= f"SELECT {select_clause} FROM {base_table}{join_clause}"

    #where clause query
    params={}
    if filters:
        conditions=[]
        for f in filters:
            col=f["column"]
            op=f["operator"]
            val=f["value"]
            column_table=None
            #find correct table for column
            for t in tables:
                if col in semantic_schema.get(t, {}).get("columns", {}):
                    column_table=t
                    break
            if not column_table:
               raise ValueError(f"Column '{col}' not in any table")


            param_key=f"{column_table}_{col}" #avoid duplicate param names
            conditions.append(f"{column_table}.{col} {op} :{param_key}")
            params[param_key] = val

        base_query += " WHERE " + " AND ".join(conditions) + " "

    #order by
    
    if operation in ["avg","sum","min","max"]:
        base_query+=f" ORDER BY {operation}_{aggregation_column} {order.upper()} "
    elif order_by:
        order_table=None
        for t in tables:
            if order_by in semantic_schema.get(t, {}).get("columns", {}):
                order_table=t
                break
        if order_table:
            base_query+=f" ORDER BY {order_table}.{order_by} {order.upper()} "

    #no limit for aggregation or group by 
    if operation not in ["count","avg","sum","min","max"]:
        base_query+= " LIMIT :limit"
        params["limit"]=limit
    #limit for grouped queries
    if group_by and limit:
        base_query+=" LIMIT :limit"
        params["limit"]= limit

    print("FINAL QUERY:",base_query)
    print("PARAMS:",params)

    return text(base_query), params



