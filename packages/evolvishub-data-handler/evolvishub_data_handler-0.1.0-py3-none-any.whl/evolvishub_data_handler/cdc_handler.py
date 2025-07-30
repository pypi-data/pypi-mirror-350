"""CDC handler implementation."""
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from .adapters.base import BaseAdapter
from .config import DatabaseConfig, DatabaseType, SyncConfig, WatermarkConfig, CDCConfig
from .adapters.postgresql import PostgreSQLAdapter
from .adapters.factory import AdapterFactory


class CDCHandler:
    """Change Data Capture handler for data synchronization."""

    def __init__(self, config: CDCConfig):
        """Initialize the CDC handler.

        Args:
            config: CDC configuration object.
        """
        self.config = config
        self.source_adapter: BaseAdapter = AdapterFactory.create(config.source)
        self.destination_adapter: BaseAdapter = AdapterFactory.create(config.destination)

        self._setup_logging()

    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        logger.add(
            "logs/cdc.log",
            rotation="10 MB",
            retention="10 days",
            level="INFO",
        )

    def _create_adapter(self, config: DatabaseConfig) -> BaseAdapter:
        """Create a database adapter based on configuration.

        Args:
            config: Database configuration

        Returns:
            BaseAdapter: Configured database adapter

        Raises:
            ValueError: If database type is not supported
        """
        if config.type == DatabaseType.POSTGRESQL:
            from .adapters.postgresql import PostgreSQLAdapter
            return PostgreSQLAdapter(config)
        elif config.type == DatabaseType.MYSQL:
            from .adapters.mysql import MySQLAdapter
            return MySQLAdapter(config)
        elif config.type == DatabaseType.SQLITE:
            from .adapters.sqlite import SQLiteAdapter
            return SQLiteAdapter(config)
        elif config.type == DatabaseType.ORACLE:
            from .adapters.oracle import OracleAdapter
            return OracleAdapter(config)
        elif config.type == DatabaseType.SQLSERVER:
            from .adapters.sqlserver import SQLServerAdapter
            return SQLServerAdapter(config)
        elif config.type == DatabaseType.MONGODB:
            from .adapters.mongodb import MongoDBAdapter
            return MongoDBAdapter(config)
        else:
            raise ValueError(f"Unsupported database type: {config.type}")

    def _create_adapters(self) -> Tuple[BaseAdapter, BaseAdapter]:
        """Create source and destination adapters.

        Returns:
            Tuple[BaseAdapter, BaseAdapter]: Source and destination adapters
        """
        source_adapter = self._create_adapter(self.config.source)
        dest_adapter = self._create_adapter(self.config.destination)
        return source_adapter, dest_adapter

    def _process_batch(self, changes: List[Dict[str, Any]]) -> None:
        """Process a batch of changes.

        Args:
            changes: List of changes to process.
        """
        for change in changes:
            try:
                operation = change.get("operation", "INSERT")
                if operation == "INSERT":
                    self.destination_adapter.insert_data(self.config.destination.table, [change])
                elif operation == "UPDATE":
                    self.destination_adapter.update_data(
                        self.config.destination.table,
                        [change],
                        ["id"]  # Assuming 'id' is the primary key
                    )
                elif operation == "DELETE":
                    self.destination_adapter.delete_data(
                        self.config.destination.table,
                        {"id": change["id"]}
                    )
            except Exception as e:
                logger.error(f"Error processing change: {str(e)}")
                raise

    def _get_watermark_value(
        self, watermark_type: str, current_value: str, new_value: str
    ) -> str:
        """Get the appropriate watermark value based on type.

        Args:
            watermark_type: Type of watermark (timestamp, integer, string)
            current_value: Current watermark value
            new_value: New watermark value

        Returns:
            str: Selected watermark value
        """
        if watermark_type == "timestamp":
            return max(current_value, new_value)
        elif watermark_type == "integer":
            return str(max(int(current_value), int(new_value)))
        else:  # string
            return max(current_value, new_value)

    def sync(self) -> None:
        """Perform a single synchronization cycle."""
        try:
            # Connect to databases
            self.source_adapter.connect()
            self.destination_adapter.connect()

            # Get the current watermark value
            watermark = self.source_adapter.get_last_sync_timestamp()

            # Query for changes since the last watermark
            query = f"""
                SELECT * FROM {self.config.source.table}
                WHERE {self.config.sync.watermark_table} > %s
                ORDER BY {self.config.sync.watermark_table}
                LIMIT %s
            """
            changes = self.source_adapter.execute_query(query, [watermark, self.config.sync.batch_size])

            if changes:
                self._process_batch(changes)

        except Exception as e:
            logger.error(f"Error during sync: {str(e)}")
            raise
        finally:
            # Disconnect from databases
            self.source_adapter.disconnect()
            self.destination_adapter.disconnect()

    def run_continuous(self) -> None:
        """Run continuous synchronization."""
        try:
            while True:
                self.sync()
                time.sleep(self.config.sync.interval_seconds)
        except KeyboardInterrupt:
            logger.info("Continuous sync stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous sync: {str(e)}")
            raise 