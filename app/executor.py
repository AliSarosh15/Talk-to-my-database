def execute_query(db, query, params):
    try:
        result = db.execute(query, params)
        return result.mappings().all()
    except Exception as e:
        raise ValueError(f"Database execution error: {str(e)}")
