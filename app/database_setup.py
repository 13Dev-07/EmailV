"""Database setup and initialization module."""

import os
from pathlib import Path
from typing import List
import asyncio
from app.supabase_client import DatabaseClient

class DatabaseSetup:
    """Handles database initialization and migrations."""
    
    def __init__(self, db_client: DatabaseClient):
        self.db = db_client
        self.migrations_dir = Path(__file__).parent.parent / 'migrations'
    
    async def init_database(self):
        """Initialize database with required tables and policies."""
        migration_files = sorted(self.migrations_dir.glob('*.sql'))
        for migration_file in migration_files:
            await self._run_migration(migration_file)
    
    async def _run_migration(self, migration_file: Path):
        """Execute a single migration file."""
        try:
            with open(migration_file, 'r') as f:
                sql = f.read()
                
            # Execute the SQL file directly
            await self.db.supabase.execute_sql(sql)
                    
        except Exception as e:
            raise Exception(f"Migration failed: {migration_file.name} - {str(e)}")

async def setup_database():
    """Main function to set up the database."""
    db_client = DatabaseClient()
    setup = DatabaseSetup(db_client)
    await setup.init_database()

if __name__ == "__main__":
    asyncio.run(setup_database())