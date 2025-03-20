from typing import Dict, Any
from sqlalchemy.orm import Query

def paginate_query(query: Query, page: int, limit: int) -> Dict[str, Any]:
    offset = (page - 1) * limit
    total_records = query.count()
    total_pages = (total_records + limit - 1) // limit  # Calculate total pages
    results = query.offset(offset).limit(limit).all()
    return {
        "total_records": total_records,
        "current_page": page,
        "total_pages": total_pages,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None,
        "results": results
    }
