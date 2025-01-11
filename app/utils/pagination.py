def paginate(query, limit: int = 10, offset: int = 0):
    return query.limit(limit).offset(offset)