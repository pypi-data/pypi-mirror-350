from psqlextra.backend.migrations.operations import PostgresAddHashPartition


def psqlextra_partitioning_add_hash(model_name, modulus):
    for remainder in range(modulus):
        yield PostgresAddHashPartition(
            model_name=model_name,
            name=str(remainder),
            modulus=modulus,
            remainder=remainder,
        )
