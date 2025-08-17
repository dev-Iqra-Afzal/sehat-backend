def paginated_response(*, crud_data: list, page: int, has_more: bool, total: int, limit: int) -> dict:
    return {
        "data": crud_data,
        "total_count": total,
        "has_more": page * limit < total,
        "page": page,
        "limit": limit
    }