from pathlib import Path
import sqlite3

__all__ = [
    'migrate',
]

ZERO_DATETIME = "'1970-01-01 00:00:00'"


def get_migration_commands(from_version: str) -> list[str]:
    match from_version:
        case 'a':
            return [
                f'ALTER TABLE text_exams add total_pause_time DATETIME NOT NULL default {ZERO_DATETIME}',
                f'ALTER TABLE dialogue_exams add total_pause_time DATETIME NOT NULL default {ZERO_DATETIME}',
            ]
        case 'b':
            return [
                'ALTER TABLE text_exams add scanned BOOLEAN NOT NULL default 0',
                'ALTER TABLE dialogue_exams add scanned BOOLEAN NOT NULL default 0',
            ]
        case 'c':
            # noinspection SqlWithoutWhere
            return [
                'DELETE FROM grammar_cache_sentences',
            ]
        case 'd':
            return [
                'DROP TABLE speakers',
                'DROP TABLE styles',
                'DROP TABLE topics',
            ]
        case _:
            raise ValueError(f'Unknown migration from version {from_version}.')


def migrate(database: Path, from_version: str) -> None:
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    for command in get_migration_commands(from_version):
        cursor.execute(command)
    connection.commit()
    connection.close()
