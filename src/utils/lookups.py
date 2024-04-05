from django.db.models import Field
from django.db.models import Lookup


@Field.register_lookup
class SearchLookup(Lookup):
    lookup_name = "search"

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "MATCH (%s) AGAINST (+%s IN BOOLEAN MODE)" % (lhs, rhs), params
