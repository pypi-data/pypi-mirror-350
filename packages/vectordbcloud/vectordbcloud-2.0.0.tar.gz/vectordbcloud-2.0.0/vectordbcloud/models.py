from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass


@dataclass
class Context:
    """Context object for ECP."""
    id: str
    token: str
    metadata: Dict[str, Any]
    created_at: str
    expires_at: str


@dataclass
class QueryResult:
    """Result from a vector query."""
    id: str
    score: float
    metadata: Dict[str, Any]
    vector: Optional[List[float]] = None


@dataclass
class Subscription:
    """Subscription information."""
    plan_id: str
    status: str
    current_period_start: str
    current_period_end: str
    features: Dict[str, Any]


@dataclass
class UsageLimits:
    """Usage limits information."""
    vector_count: int
    vector_limit: int
    api_calls: int
    api_call_limit: int
    storage_used: int
    storage_limit: int
    approaching_limit: bool = False
    approaching_limit_type: Optional[str] = None


@dataclass
class DeploymentResult:
    """Result from a deployment operation."""
    deployment_id: str
    status: str
    resources: List[Dict[str, Any]]


@dataclass
class GraphRAGResult:
    """Result from a GraphRAG query."""
    answer: str
    sources: List[Dict[str, Any]]
    graph: Dict[str, Any]


@dataclass
class OCRResult:
    """Result from OCR processing."""
    text: str
    tables: List[Dict[str, Any]]
    forms: List[Dict[str, Any]]
    pages: List[Dict[str, Any]]
