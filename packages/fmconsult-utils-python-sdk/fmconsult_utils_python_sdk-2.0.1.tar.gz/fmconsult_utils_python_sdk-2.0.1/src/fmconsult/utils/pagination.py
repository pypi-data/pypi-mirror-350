class PaginationUtil:
    @staticmethod
    def paginate(queryset, page, limit):
        try:
            offset = (page - 1) * limit
            paginated_items = queryset[offset:offset + limit]
            total_items = len(queryset)

            return {
                'items': paginated_items,
                'total': total_items,
                'page': page,
                'limit': limit,
                'pages': (total_items // limit) + (1 if total_items % limit != 0 else 0),
                'prev': page - 1 if page > 1 else None,
                'next': page + 1 if page < (total_items // limit) + (1 if total_items % limit != 0 else 0) else None
            }
        except Exception as e:
            raise Exception(f"Pagination error: {str(e)}")