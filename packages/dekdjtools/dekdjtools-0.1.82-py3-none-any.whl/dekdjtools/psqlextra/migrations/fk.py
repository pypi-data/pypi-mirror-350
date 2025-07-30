from django.db import migrations, models


def psqlextra_partitioning_fk(app_label, model_name, field_name, primary_keys, kwargs):
    model_label = model_name.lower()
    table_name = f"{app_label}_{model_label}"
    fk_from = ', '.join(field_name + '_' + x for x in primary_keys)
    fk_to = ', '.join(primary_keys)
    return migrations.SeparateDatabaseAndState(
        state_operations=[
            migrations.AddField(
                model_name=model_label,
                name=field_name,
                field=models.ForeignKey(**kwargs),
            ),
        ],
        database_operations=[
            # Create the field without the db constraint
            migrations.AddField(
                model_name=model_label,
                name=field_name,
                field=models.ForeignKey(**kwargs, db_constraint=False),
            ),
            # Create the constraint manually
            migrations.RunSQL(
                f"ALTER TABLE {table_name} ADD CONSTRAINT {model_label}_pk_{field_name} FOREIGN KEY ({fk_from}) REFERENCES {kwargs['to'].replace('.', '_')} ({fk_to})",
                f"ALTER TABLE {table_name} DROP CONSTRAINT {model_label}_pk_{field_name}",
            ),
        ],
    )
