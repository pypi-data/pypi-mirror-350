# django_zk_auth/crypto/types.py
"""Enhanced type definitions for ZK cryptographic operations with REST API compatibility"""

from typing import NewType, Union, Optional, List, Dict, Any, Protocol
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import time
from .field_arithmetic import FieldElement
from pydantic import BaseModel, Field, field_validator

# === Type Aliases ===
Proof = bytes
PublicSignals = List[FieldElement]
PrivateInputs = Dict[str, FieldElement]
CircuitInputs = Dict[str, Union[FieldElement, List[FieldElement]]]


# === Enums ===
class ProofType(str, Enum):
    GROTH16 = "groth16"
    PLONK = "plonk"
    STARK = "stark"


class HashFunction(str, Enum):
    POSEIDON = "poseidon"
    PEDERSEN = "pedersen"
    MIMC = "mimc"


# === Core Data Models ===
@dataclass(frozen=True)
class ZKProof:
    """Zero-knowledge proof data structure"""
    proof: bytes
    public_signals: List[FieldElement]
    proof_type: ProofType
    circuit_id: str
    timestamp: int
    version: Optional[str] = "v1"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proof": self.proof.hex(),
            "public_signals": self.public_signals,
            "proof_type": self.proof_type.value,
            "circuit_id": self.circuit_id,
            "timestamp": self.timestamp,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ZKProof':
        return cls(
            proof=bytes.fromhex(data["proof"]),
            public_signals=data["public_signals"],
            proof_type=ProofType(data["proof_type"]),
            circuit_id=data["circuit_id"],
            timestamp=data["timestamp"],
            version=data.get("version", "v1")
        )

    def __repr__(self) -> str:
        return f"<ZKProof type={self.proof_type.value} circuit={self.circuit_id} ts={self.timestamp}>"


class CircuitProtocol(Protocol):
    """Protocol for ZK circuits"""
    def generate_witness(self, inputs: CircuitInputs) -> np.ndarray: ...
    def prove(self, witness: np.ndarray) -> ZKProof: ...
    def verify(self, proof: ZKProof) -> bool: ...


@dataclass
class AuthChallenge:
    """Authentication challenge data"""
    nonce: str
    session_id: str
    timestamp: int
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    expires_at: Optional[int] = None

    def __repr__(self) -> str:
        return f"<AuthChallenge nonce={self.nonce} session={self.session_id}>"

    def is_expired(self) -> bool:
        return self.expires_at is not None and time.time() > self.expires_at


@dataclass
class AuthResponse:
    """Authentication response data"""
    proof: ZKProof
    challenge: AuthChallenge
    commitment: str

    def is_valid(self) -> bool:
        return (
            isinstance(self.proof, ZKProof)
            and isinstance(self.challenge, AuthChallenge)
            and isinstance(self.commitment, str)
            and len(self.commitment) > 0
        )


class ZKSystemConfig(Dict[str, Any]):
    """Configuration for ZK system"""
    proof_system: Optional[ProofType]
    hash_function: Optional[HashFunction]
    circuit_path: Optional[str]
    proving_key_path: Optional[str]
    verifying_key_path: Optional[str]
    field_size: Optional[int]
    security_level: Optional[int]
    enable_audit_logging: Optional[bool]
    max_proof_age_seconds: Optional[int]
    rate_limit_window_seconds: Optional[int]
    max_requests_per_window: Optional[int]


# === Pydantic Models for REST Compatibility ===
class ZKProofModel(BaseModel):
    proof: str = Field(..., description="Hex-encoded zero-knowledge proof")
    public_signals: List[int]
    proof_type: ProofType
    circuit_id: str
    timestamp: int
    version: Optional[str] = "v1"

    @field_validator("proof")
    def validate_hex(cls, v):
        if not isinstance(bytes.fromhex(v), bytes):
            raise ValueError("Proof must be a valid hex string")
        return v

    def to_internal(self) -> ZKProof:
        return ZKProof.from_dict(self.dict())

    @classmethod
    def from_internal(cls, proof: ZKProof) -> "ZKProofModel":
        return cls(**proof.to_dict())

@dataclass
class ZKCommitment:
    commitment: str
    salt: Optional[str] = None


@dataclass
class Nonce:
    value: str
    created_at: float = field(default_factory=time.time)

class AuthChallengeModel(BaseModel):
    nonce: str
    session_id: str
    timestamp: int
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}
    expires_at: Optional[int] = None


class AuthResponseModel(BaseModel):
    proof: ZKProofModel
    challenge: AuthChallengeModel
    commitment: str

    def is_valid(self) -> bool:
        return bool(self.commitment) and self.proof and self.challenge
