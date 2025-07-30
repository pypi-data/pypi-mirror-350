from typing import List

from bellameta import constants as bmconst

from bellasplit import constants as bsconst


def validate_table_name(table: str):
    '''
    Validates the table name to be contained either in METADATA_TABLES or SPLIT_TABLES.
    '''

    valid_table_names = bmconst.METADATA_TABLES + bsconst.SPLIT_TABLES
    if table not in valid_table_names:
        raise ValueError(f'No matching table named {table} found in database.')
    return table

def validate_table_names(tables: List[str]):
    for table in tables:
        validate_table_name(table)
    return tables
