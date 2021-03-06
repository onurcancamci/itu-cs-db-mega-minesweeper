import os
import sys
import psycopg2 as dbapi2
from .selectBuilder import *
from .insertBuilder import *
from .deleteBuilder import *
from .updateBuilder import *

url = os.getenv("DATABASE_URL")
connection = dbapi2.connect(url)


class QueryBuilder:
    def __init__(self):
        cursor = connection.cursor()
        self.data = {"cursor": cursor, "connection": connection}

    def Select(self, table, asName, cols):
        self.data["method"] = "SELECT"
        self.data["cols"] = cols
        self.data["table"] = table
        self.data["joins"] = []
        self.data["accessories"] = []
        self.data["shid"] = asName
        self.data["where"] = []
        return SelectBuilder(self.data)

    def Insert(self, table, values, retId=True):
        self.data["method"] = "INSERT INTO"
        self.data["table"] = table
        self.data["values"] = values
        self.data["retId"] = retId
        return InsertBuilder(self.data)

    def Delete(self, table):
        self.data["method"] = "DELETE"
        self.data["table"] = table
        self.data["where"] = []
        return DeleteBuilder(self.data)

    def Update(self, table, sets):
        self.data["method"] = "UPDATE"
        self.data["table"] = table
        self.data["where"] = []
        self.data["sets"] = sets
        return UpdateBuilder(self.data)


# QueryBuilder().Update("test_b", ["b = b + 1"]).AndWhere("id = 1").Execute()

# QueryBuilder().Insert("test_b", {"b": 10}).Execute()
# QueryBuilder().Delete("test_b").AndWhere("b > 2").Execute()

# QueryBuilder() \
#     .Select("migration_version", "m", ["version"]) \
#     .AndWhere( "m.version = {ver}", {
#         "ver": 2
#     }) \
#     .AndWhere("1 = 1") \
#     .OrderBy([("m.version", "ASC")]) \
#     .Limit(1) \
#     .Build() \
#     .Explain() \
#     .Execute()

# QueryBuilder() \
#     .Select("test_a", "ta", ["id", "a", "b_id"]) \
#     .InnerJoin("test_b", "tb", ["id", "b"], "ta.b_id = tb.id") \
#     .Build() \
#     .Explain() \
#     .Execute() \

# print(QueryBuilder().Insert("test_b", {"b": 42}).Execute())
