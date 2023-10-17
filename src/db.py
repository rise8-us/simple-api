from pypika import Query, Criterion, Table
from psycopg import connect
from psycopg.rows import dict_row

def execute(query, loader=None):
    print(query)
    with connect("dbname=postgres user=postgres password=example host=localhost port=5432", row_factory=dict_row) as conn:
        if loader:
            conn.adapters.register_loader("custom-loader", loader)
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            if cur.description is not None:
                return cur.fetchall()
            else:
                return "SUCCESS"
        

def select(table_name, fields=["*"], search={}):
    print(search)
    table = Table(table_name)
    q = Query.from_(table_name).select(*fields).where( Criterion.all([table[k] == v for k, v in search.items()]) )
    return execute(q.get_sql())

def insert(table, item: dict):
    fields = item.keys()
    values = item.values()
    q = Query.into(table).columns(*fields).insert(*values)
    return execute(q.get_sql())

def update(table_name, item: dict, where: dict):
    table = Table(table_name)
    q = set_multi(Query.update(table), item).where(Criterion.all([table[k] == v for k, v in where.items()]))
    return execute(q.get_sql())

def set_multi(query_builder, item : dict):
    new_query_builder = query_builder
    for k, v in item.items():
        new_query_builder = new_query_builder.set(k, v)
    return new_query_builder
