from pypika import Query, Column
from yoyo import step

steps = [
   step(
       Query.create_table("repositories") \
        .columns(
            Column("id", "INT", nullable=False),
            Column("name", "VARCHAR(100)", nullable=False),
            Column("onboarding_date", "VARCHAR(100)", nullable=False),
            Column("team", "VARCHAR(20)", nullable=True),
            Column("status", "VARCHAR(20)", nullable=False)) \
        .primary_key("id").get_sql(),
        Query.drop_table("repositories").get_sql()
   )
]