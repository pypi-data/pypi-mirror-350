from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator, field_validator
from enum import Enum


class DatabaseType(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    ORACLE = "oracle"
    SQLSERVER = "sqlserver"
    MONGODB = "mongodb"
    FILE = "file"
    S3 = "s3"
    GCS = "gcs"
    AZURE_BLOB = "azure_blob"


class WatermarkType(str, Enum):
    TIMESTAMP = "timestamp"
    INTEGER = "integer"
    STRING = "string"


class CompressionType(str, Enum):
    GZIP = "gzip"
    SNAPPY = "snappy"
    LZ4 = "lz4"
    ZSTD = "zstd"
    NONE = "none"


class WatermarkConfig(BaseModel):
    column: str
    type: WatermarkType
    initial_value: Optional[str] = None
    increment_value: Optional[str] = None


class CloudStorageConfig(BaseModel):
    region: Optional[str] = None
    endpoint_url: Optional[str] = None
    use_ssl: bool = True
    verify_ssl: bool = True
    max_retries: int = 3
    timeout: int = 30
    chunk_size: int = 8 * 1024 * 1024  # 8MB


class DatabaseConfig(BaseModel):
    """Database configuration."""
    type: DatabaseType
    host: Optional[str] = None
    port: Optional[int] = None
    database: str
    username: Optional[str] = None
    password: Optional[str] = None
    file_path: Optional[str] = None  # For file-based data sources
    table: Optional[str] = None
    watermark: Optional[WatermarkConfig] = None
    ssl_mode: Optional[str] = None
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    ssl_root_cert: Optional[str] = None
    connection_timeout: int = Field(default=30, gt=0)
    pool_size: int = Field(default=5, gt=0)
    max_overflow: int = Field(default=10, gt=0)
    cloud_storage: Optional[CloudStorageConfig] = None  # For cloud storage services
    additional_params: Dict[str, Any] = Field(default_factory=dict)  # Additional connection parameters

    @field_validator("port")
    def validate_port(cls, v: Optional[int]) -> Optional[int]:
        """Validate port number."""
        if v is not None and not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v

    @field_validator("host", "username", "password")
    def validate_required_fields(cls, v: Optional[str], info) -> Optional[str]:
        """Validate required fields based on database type."""
        if info.data.get("type") != DatabaseType.SQLITE and v is None:
            raise ValueError(f"{info.field_name} is required for {info.data.get('type')} database")
        return v


class SyncConfig(BaseModel):
    batch_size: int = Field(default=1000, gt=0)
    interval_seconds: int = Field(default=60, gt=0)
    watermark_table: str = "sync_watermark"
    error_retry_attempts: int = Field(default=3, gt=0)
    error_retry_delay: int = Field(default=5, gt=0)
    compression: Optional[CompressionType] = None
    encryption: Optional[Dict[str, Any]] = None  # Encryption settings


class CDCConfig(BaseModel):
    source: DatabaseConfig
    destination: DatabaseConfig
    sync: SyncConfig = Field(default_factory=SyncConfig)
    tables: List[str] = Field(default_factory=list)
    exclude_tables: List[str] = Field(default_factory=list)
    include_schemas: List[str] = Field(default_factory=list)
    exclude_schemas: List[str] = Field(default_factory=list) 