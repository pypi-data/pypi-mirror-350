from .client import VectorDBCloud
from .models import (
    Context,
    QueryResult,
    Subscription,
    UsageLimits,
    DeploymentResult,
    GraphRAGResult,
    OCRResult,
)
from .ecp import ecp_handler

__version__ = "0.3.1"

__all__ = [
    "VectorDBCloud",
    "Context",
    "QueryResult",
    "Subscription",
    "UsageLimits",
    "DeploymentResult",
    "GraphRAGResult",
    "OCRResult",
    "ecp_handler",
]

# ECP flags
ECP_ENABLED = True
ECP_EMBEDDED = True
ECP_NATIVE = True
ECP_PROTOCOL_VERSION = "1.0"
ECP_COMPLIANCE_LEVEL = "enterprise"
ECP_ENCRYPTION = "AES-256-GCM"
ECP_COMPRESSION = True
ECP_AUDIT_LOGGING = True
ECP_CACHE_STRATEGY = "distributed"

# Performance flags
LOW_LATENCY_MODE = True
HIGH_CONCURRENCY_MODE = True
WORKERS = 32
TIMEOUT = 300
MAX_RETRIES = 3
BATCH_SIZE = 20
PARALLEL_PROCESSING = True
CACHE_ENABLED = True
CACHE_TTL = 3600
PRELOAD_MODELS = True
OPTIMIZE_MEMORY = True
ASYNC_PROCESSING = True
COMPRESSION_ENABLED = True
RESULT_CACHE_SIZE = 10000
MODEL_CACHE_SIZE = 1000
ENTERPRISE_MODE = True
PRODUCTION_READY = True



