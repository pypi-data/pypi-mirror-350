import pytest
import time
from datetime import datetime, timedelta
from types import SimpleNamespace
import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import django_zk_auth.crypto.types as zk_types

def test_zkproof_to_from_dict():
    proof_bytes = b"\x01\x02\x03\x04"
    public_signals = [123, 456, 789]
    proof_type = zk_types.ProofType.GROTH16
    circuit_id = "test_circuit"
    timestamp = int(time.time())
    version = "v1"

    zk_proof = zk_types.ZKProof(
        proof=proof_bytes,
        public_signals=public_signals,
        proof_type=proof_type,
        circuit_id=circuit_id,
        timestamp=timestamp,
        version=version,
    )

    d = zk_proof.to_dict()
    assert d["proof"] == proof_bytes.hex()
    assert d["public_signals"] == public_signals
    assert d["proof_type"] == proof_type.value
    assert d["circuit_id"] == circuit_id
    assert d["timestamp"] == timestamp
    assert d["version"] == version

    zk_proof_restored = zk_types.ZKProof.from_dict(d)
    assert zk_proof_restored == zk_proof
    assert repr(zk_proof_restored).startswith("<ZKProof")

def test_auth_challenge_expiry():
    nonce = "nonce123"
    session_id = "sess456"
    timestamp = int(time.time())
    expires_at = int(time.time()) + 1  # expires in 1 second

    challenge = zk_types.AuthChallenge(
        nonce=nonce,
        session_id=session_id,
        timestamp=timestamp,
        expires_at=expires_at,
    )

    assert challenge.nonce == nonce
    assert challenge.session_id == session_id
    assert not challenge.is_expired()

    # Wait for expiry
    time.sleep(1.1)
    assert challenge.is_expired()

    # Metadata default
    assert isinstance(challenge.metadata, dict)


def test_auth_response_validity():
    proof = zk_types.ZKProof(
        proof=b"\x00\x01",
        public_signals=[1],
        proof_type=zk_types.ProofType.PLONK,
        circuit_id="circuit",
        timestamp=int(time.time()),
    )
    challenge = zk_types.AuthChallenge(
        nonce="nonce",
        session_id="session",
        timestamp=int(time.time()),
    )
    commitment = "commitmentstring"

    response = zk_types.AuthResponse(
        proof=proof,
        challenge=challenge,
        commitment=commitment,
    )

    assert response.is_valid()

    # Invalid commitment
    response.commitment = ""
    assert not response.is_valid()


def test_pydantic_zkproofmodel_validation():
    proof_hex = "010203"
    public_signals = [10, 20]
    proof_type = zk_types.ProofType.STARK
    circuit_id = "circuitX"
    timestamp = int(time.time())

    model = zk_types.ZKProofModel(
        proof=proof_hex,
        public_signals=public_signals,
        proof_type=proof_type,
        circuit_id=circuit_id,
        timestamp=timestamp,
    )
    # validate hex returns same string
    assert model.proof == proof_hex

    # to_internal returns a ZKProof instance with matching data
    internal = model.to_internal()
    assert internal.proof == bytes.fromhex(proof_hex)
    assert internal.proof_type == proof_type

    # from_internal returns model with same data
    back_to_model = zk_types.ZKProofModel.from_internal(internal)
    assert back_to_model.dict() == model.dict()


def test_pydantic_auth_challenge_model_defaults():
    challenge = zk_types.AuthChallengeModel(
        nonce="nonceX",
        session_id="sessionX",
        timestamp=int(time.time()),
    )
    assert challenge.metadata == {}
    assert challenge.user_id is None
    assert challenge.expires_at is None


def test_pydantic_auth_response_model_is_valid():
    zkproof_model = zk_types.ZKProofModel(
        proof="abcdef",
        public_signals=[1],
        proof_type=zk_types.ProofType.GROTH16,
        circuit_id="cid",
        timestamp=int(time.time()),
    )
    challenge_model = zk_types.AuthChallengeModel(
        nonce="nonce",
        session_id="session",
        timestamp=int(time.time()),
    )
    response_model = zk_types.AuthResponseModel(
        proof=zkproof_model,
        challenge=challenge_model,
        commitment="commit123",
    )
    assert response_model.is_valid()

    response_model.commitment = ""
    assert not response_model.is_valid()


def test_circuit_protocol_type():
    class DummyCircuit:
        def generate_witness(self, inputs):
            return "witness"

        def prove(self, witness):
            return zk_types.ZKProof(
                proof=b"p",
                public_signals=[1],
                proof_type=zk_types.ProofType.GROTH16,
                circuit_id="cid",
                timestamp=int(time.time()),
            )

        def verify(self, proof):
            return isinstance(proof, zk_types.ZKProof)

    circuit: zk_types.CircuitProtocol = DummyCircuit()
    witness = circuit.generate_witness({})
    proof = circuit.prove(witness)
    assert circuit.verify(proof)