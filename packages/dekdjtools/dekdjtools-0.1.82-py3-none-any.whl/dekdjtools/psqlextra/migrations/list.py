from psqlextra.backend.migrations.operations import PostgresAddListPartition


def psqlextra_partitioning_add_list(model_name, values_list):
    for index, values in enumerate(values_list):
        if not isinstance(values, (list, tuple)):
            values = [values]
        yield PostgresAddListPartition(
            model_name=model_name,
            name=str(index),
            values=values,
        )
