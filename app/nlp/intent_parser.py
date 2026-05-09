import re

def parse_intent(user_input:str,semantic_schema:dict):
    '''converts nlp to structured intent'''
    user_input=user_input.lower()

    intent={
        "tables":[],
        "limit":10,
        "filters":[],
        "operation":"read",
        "columns":[],
        "aggregation_column":None,
        "group_by":None,
        "order_by":None,
        "order":"desc" #default

    }
    #aggregation detection
    if "total" in user_input or "sum" in user_input:
        intent["operation"]="sum"

    elif "average" in user_input or "avg" in user_input:
        intent["operation"]="avg"

    elif "count" in user_input:
        intent["operation"]="count"

    elif "maximum" in user_input or "max" in user_input:
        intent["operation"]="max"

    elif "minimum" in user_input or "min" in user_input:
        intent["operation"]="min"
        
    elif "spent" in user_input or "money" in user_input:
            intent["operation"]="sum"
            intent["aggregation_column"]="amount"

    #Finding table using semantic aliases

    for table, meta in semantic_schema.items():
        #match table name 
        if table in user_input:
            intent["tables"].append(table)
            continue
        for alias in meta["aliases"]:
            if alias in user_input:
                intent["tables"].append(table)
                break
    #remove duplicates
    intent["tables"]=list(set(intent["tables"]))

    #if no table found
    if not intent["tables"]:
        for table,meta in semantic_schema.items():
            for col in meta["columns"]:
                if col in user_input:
                    intent["tables"].append(table)
    intent["tables"]=list(set(intent["tables"]))

    if not intent["tables"]:
        return {}


   
    for table,meta in semantic_schema.items():
            for col in meta["columns"]:
                if col in user_input:
                    intent["columns"].append(col)
                    #auto add table if column found
                    if table not in intent["tables"]:
                        intent["tables"].append(table)
    
    intent["columns"]=list(set(intent["columns"]))
    intent["tables"]=list(set(intent["tables"]))

    #aggregation column
    if intent["operation"] in ["avg","sum","min","max"]:
        if intent["columns"]:
            intent["aggregation_column"] = intent["columns"][0]
        else:
            intent["aggregation_column"]= "amount"
    if intent["aggregation_column"]:
        for table, meta in semantic_schema.items():
            if intent["aggregation_column"] in meta["columns"]:
                if table not in intent["tables"]:
                    intent["tables"].append(table)

    if intent["operation"] in ["avg","sum","min","max","count"]:
        if "per user" in user_input or "by user" in user_input:
            intent["group_by"] = "user_id"
        elif "users" in user_input or "user" in user_input:
            intent["group_by"] = "user_id"
        

    top_match=re.search(r"top\s+(\d+)", user_input)
    if top_match:
        intent["limit"]=int(top_match.group(1))
        intent["order"]="desc"

    #general number fallback
    elif re.search(r"\b(\d+)\b", user_input):
        intent["limit"]=int(re.search(r"\b(\d+)\b", user_input).group(1))

    if "all" in user_input:
        intent["limit"]=100

    if "highest" in user_input or "top" in user_input or "max" in user_input:
        intent["order"]="desc"
    elif "lowest" in user_input or "minimum" in user_input or "min" in user_input:
        intent["order"]="asc"

    order_match=re.search(r"by (\w+)", user_input)
    if order_match:
        col=order_match.group(1)
        for table in intent["tables"]:
            if col in semantic_schema[table]["columns"]:
                intent["order_by"]=col
                break

     #aggregation order fix
    if intent["operation"] in ["sum","avg","min","max"]:
        intent["order_by"]=intent["aggregation_column"]
    #default order by
    if not intent["order_by"]:
        if intent["aggregation_column"]:
            intent["order_by"]=intent["aggregation_column"]
        elif intent["columns"]:
            intent["order_by"]=intent["columns"][0]

    #convert text to operators 
    user_input=user_input.replace("greater than", ">")
    user_input=user_input.replace("less than", "<")
    user_input=user_input.replace("equal to", "=")


    #filter detection(eg-amount>1000)
    filter_pattern=r"(\w+)\s*(=|>|<|>=|<=)\s*(\d+)"
    matches=re.findall(filter_pattern,user_input)

    all_columns=[]
    for table in intent["tables"]:
        all_columns.extend(semantic_schema[table]["columns"])

    for col,op,val in matches:
        #validating columns
        if col not in all_columns:
            continue #ignore invalid column
        intent["filters"].append({
            "column":col,
            "operator":op,
            "value":int(val)
        })

    if intent["operation"] in ["sum","avg","min","max"]:
        if intent["group_by"] is None and "user" in user_input:
            intent["group_by"] = "user_id"
    if not intent.get("tables"):
        return {}

    print(intent)
    return intent

def detect_tables(query:str,semantic_schema:dict):
    detected_tables=[]

    query=query.lower()

    for table,meta in semantic_schema.items():
        #checks table name
        if table in query:
            detected_tables.append(table)
            continue

        #check for aliases
        for alias in meta["aliases"]:
            if alias in query:
                detected_tables.append(table)
                break

    return list(set(detected_tables))


    # ntic_schema.items():
    #         if "user_id" in meta["columns"]:
    #             if table not in intent["tables"]:
    #                 intent["tables"].append(table)
    
    # top_match=re.search(r"top\s+(\d+)",user_input)
    # if top_match:
    #     intent["limit"]=int(top_match.group(1))
    #     intent["order"]="desc"

    

    # group_patterns=["per","by","group_by"]

    # for pattern in group_patterns:
    #     if pattern in user_input:
    #         words=user_input.split(pattern)

    #         if len(words) >1:
    #             possible_col=words[1].strip().split()[0]

    #             #check if column exists
    #             for table in intent["tables"]:
    #                 if possible_col in semantic_schema[table]["columns"]:
    #                     intent["group_by"]=possible_col
    #                     break
    

    # #aggregation order fix
    # if intent["operation"] in ["sum","avg","min","max"]:
    #     if "by total" in user_input or "by sum" in user_input:
    #         intent["order_by"]=intent["aggregation_column"]
    # #default order by
    # if not intent["order_by"]:
    #     if intent["aggregation_column"]:
    #         intent["order_by"]=intent["aggregation_column"]
    #     elif intent["columns"]:
    #         intent["order_by"]=intent["columns"][0]

    # #convert text to operators 
    # user_input=user_input.replace("greater than", ">")
    # user_input=user_input.replace("less than", "<")
    # user_input=user_input.replace("equal to", "=")


    # #filter detection(eg-amount>1000)
    # filter_pattern=r"(\w+)\s*(=|>|<|>=|<=)\s*(\d+)#Finding limit of the query
    # limit_match=re.search(r"\b(\d+)\b",user_input)
    # if limit_match:
    #     intent["limit"]= int(limit_match.group(1))


    # #handle all  type query
    # if "all" in user_input:
    #     intent["limit"]=100 # can also change this

    # if "per user" in user_input or "by user" in user_input:
    #     intent["group_by"]="user_id"

    #     for table, meta in sema"
    



    