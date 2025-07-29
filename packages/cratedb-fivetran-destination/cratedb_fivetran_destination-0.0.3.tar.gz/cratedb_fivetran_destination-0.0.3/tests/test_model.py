from cratedb_fivetran_destination.model import SqlBag


def test_sqlbag(engine):
    bag = SqlBag().add("SELECT 23").add("SELECT 42")
    with engine.connect() as connection:
        bag.execute(connection)
