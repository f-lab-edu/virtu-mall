from django.db.models import Field
from django.db.models import Lookup


@Field.register_lookup
class SearchLookup(Lookup):
    lookup_name = "search"

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        rhs = self.__create_keywords__(rhs)
        params = lhs_params + rhs_params
        return "MATCH (%s) AGAINST (%s IN BOOLEAN MODE)" % (lhs, rhs), params

    @staticmethod
    def __create_keywords__(rhs):
        new_rhs = ""
        for keyword in rhs.split():
            new_rhs += f"+{keyword} "
        return new_rhs[:-1]
