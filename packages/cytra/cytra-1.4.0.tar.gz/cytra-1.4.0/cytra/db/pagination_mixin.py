from sqlalchemy.orm import Query

from cytra.exceptions import PaginationLimitError


class PaginationMixin:
    __take_header_key__ = "HTTP_X_TAKE"
    __skip_header_key__ = "HTTP_X_SKIP"
    __max_take__ = 100

    @classmethod
    def paginate_by_request(cls, query: Query):
        app = cls.__app__
        qs = app.request.query
        env = app.request.environ

        try:
            take = int(qs.get("take") or env.get(cls.__take_header_key__))
            if take > cls.__max_take__:
                raise PaginationLimitError
        except (ValueError, TypeError):
            take = cls.__max_take__

        try:
            skip = int(qs.get("skip") or env.get(cls.__skip_header_key__))
        except (ValueError, TypeError):
            skip = 0

        headers = app.response.headers
        headers["x-pagination-take"] = str(take)
        headers["x-pagination-skip"] = str(skip)
        headers["x-pagination-count"] = str(query.count())
        return query.offset(skip).limit(take)
