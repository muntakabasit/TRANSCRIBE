#!/usr/bin/env python3
"""
migrate_job_schema.py — standalone runner for the job-schema migration.

Usage:
    python migrate_job_schema.py [--db PATH]

Adds nine columns required by the background-job contract to the
transcription_jobs table.  Safe to run multiple times (idempotent).
"""

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Migrate transcription_jobs schema")
    parser.add_argument(
        "--db",
        default=str(Path(__file__).with_name("dawt_transcriber.db")),
        help="Path to SQLite database file (default: dawt_transcriber.db next to this script)",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        logger.error(f"Database not found: {db_path}")
        sys.exit(1)

    logger.info(f"Target database: {db_path}")

    import os
    os.environ.setdefault("DATABASE_URL", f"sqlite:///{db_path}")

    from database import migrate_schema, engine

    logger.info("Running schema migration...")
    added = migrate_schema(bind=engine)

    if added:
        logger.info(f"Migration complete. Columns added: {added}")
    else:
        logger.info("Migration complete. Schema already up to date.")

    import sqlite3
    with sqlite3.connect(str(db_path)) as conn:
        cur = conn.execute("PRAGMA table_info(transcription_jobs)")
        cols = [row[1] for row in cur.fetchall()]
        logger.info(f"Final column count: {len(cols)}")
        logger.info(f"Columns: {cols}")

        row_count = conn.execute("SELECT COUNT(*) FROM transcription_jobs").fetchone()[0]
        logger.info(f"Existing rows preserved: {row_count}")


if __name__ == "__main__":
    main()
