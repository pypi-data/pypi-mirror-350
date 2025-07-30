import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os
import subprocess
import time
from django.core.cache import cache


# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from django_zk_auth.crypto.proof_system import CircuitCompiler, CircuitConfig, ProofSystem, ProofCache
from django_zk_auth.crypto.types import ProofType , ZKProof
import tempfile



def test_circuit_config_is_ready(tmp_path):
    # Create temporary files to simulate the circuit files
    circuit_path = tmp_path / "circuit.json"
    r1cs_path = tmp_path / "circuit.r1cs"
    wasm_path = tmp_path / "circuit.wasm"
    proving_key_path = tmp_path / "proving.key"
    verifying_key_path = tmp_path / "verifying.key"
    
    # Initially, files don't exist, so is_ready() should be False
    config = CircuitConfig(
        name="test_circuit",
        circuit_path=circuit_path,
        r1cs_path=r1cs_path,
        wasm_path=wasm_path,
        proving_key_path=proving_key_path,
        verifying_key_path=verifying_key_path,
        proof_type=ProofType.GROTH16,
    )
    assert not config.is_ready()
    
    # Create all required files
    for path in [circuit_path, r1cs_path, wasm_path, proving_key_path, verifying_key_path]:
        path.write_text("dummy content")
    
    # Now is_ready() should return True
    assert config.is_ready()
    
    # Remove one file and check is_ready() returns False again
    verifying_key_path.unlink()
    assert not config.is_ready()

class TestCircuitCompiler:
    @pytest.fixture
    def tmp_circuits_dir(self, tmp_path):
        return tmp_path

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    @patch("django_zk_auth.crypto.proof_system.Path.exists")
    @patch("urllib.request.urlretrieve")
    def test_compile_auth_circuit_success(self, mock_urlretrieve, mock_path_exists, mock_subproc_run, tmp_circuits_dir):
        # Setup mocks
        # Simulate powersOfTau file does NOT exist initially, so it triggers download
        def path_exists_side_effect():
            # Exists only if the filename does not contain 'powersOfTau'
            return False
        mock_path_exists.side_effect = path_exists_side_effect
        
        # Mock subprocess.run to always succeed
        mock_subproc_run.return_value = MagicMock(stdout="success", returncode=0)
        mock_urlretrieve.return_value = None
        
        compiler = CircuitCompiler(tmp_circuits_dir)
        config = compiler.compile_auth_circuit()

        # Check CircuitConfig properties
        assert config.name == "zk_auth"
        assert config.circuit_path == tmp_circuits_dir / "zk_auth.circom"
        assert config.r1cs_path == tmp_circuits_dir / "zk_auth.r1cs"
        assert config.wasm_path == tmp_circuits_dir / "zk_auth_js" / "zk_auth.wasm"
        assert config.proving_key_path == tmp_circuits_dir / "zk_auth.zkey"
        assert config.verifying_key_path == tmp_circuits_dir / "zk_auth_vkey.json"
        assert config.proof_type == ProofType.GROTH16

        # Verify subprocess.run called for compile, setup, and export commands
        assert mock_subproc_run.call_count == 3

        # Verify download called once (for powers of tau file)
        mock_urlretrieve.assert_called_once()

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    @patch("django_zk_auth.crypto.proof_system.Path.exists")
    @patch("urllib.request.urlretrieve")
    def test_compile_auth_circuit_no_download_if_ptau_exists(self, mock_urlretrieve, mock_path_exists, mock_subproc_run, tmp_circuits_dir):
        # Simulate powersOfTau file exists
        def path_exists_side_effect():
            return True
        mock_path_exists.side_effect = path_exists_side_effect

        mock_subproc_run.return_value = MagicMock(returncode=0)
        compiler = CircuitCompiler(tmp_circuits_dir)
        compiler.compile_auth_circuit()

        # No download if file exists
        mock_urlretrieve.assert_not_called()

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    def test_compile_auth_circuit_compile_failure(self, mock_subproc_run, tmp_circuits_dir):
        # Simulate compilation failure
        mock_subproc_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="circom", stderr="Compilation error"
        )
        compiler = CircuitCompiler(tmp_circuits_dir)
        with pytest.raises(RuntimeError, match="Circuit compilation failed"):
            compiler.compile_auth_circuit()

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    @patch("django_zk_auth.crypto.proof_system.Path.exists")
    @patch("urllib.request.urlretrieve")
    def test_setup_proving_system_failure(self, mock_urlretrieve, mock_path_exists, mock_subproc_run, tmp_circuits_dir):
        # Setup file exists
        mock_path_exists.return_value = True

        # Setup returns success on compile, but fail on proving key setup
        def side_effect(*args, **kwargs):
            if "groth16" in args[0]:
                raise subprocess.CalledProcessError(returncode=1, cmd=args[0], stderr="Setup failure")
            return MagicMock(returncode=0)
        
        mock_subproc_run.side_effect = side_effect

        compiler = CircuitCompiler(tmp_circuits_dir)
        with pytest.raises(RuntimeError, match="Proving key setup failed"):
            compiler.compile_auth_circuit()

class DummyFE:
    def __init__(self, val):
        self.value = int(val)

# Mock poseidon_hash and FE conversion
def fake_poseidon_hash(data):
    class Result:
        value = 42
    return Result()

@pytest.fixture
def circuit_config(tmp_path):
    # Create dummy paths for all required files
    files = ["circuit.circom", "circuit.r1cs", "circuit_js/circuit.wasm", "circuit.zkey", "circuit_vkey.json"]
    for file in files:
        path = tmp_path / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("dummy")

    config = CircuitConfig(
        name="circuit",
        circuit_path=tmp_path / "circuit.circom",
        r1cs_path=tmp_path / "circuit.r1cs",
        wasm_path=tmp_path / "circuit_js/circuit.wasm",
        proving_key_path=tmp_path / "circuit.zkey",
        verifying_key_path=tmp_path / "circuit_vkey.json",
        proof_type=ProofType.GROTH16
    )
    return config


class TestProofSystem:

    @patch("django_zk_auth.crypto.proof_system.poseidon_hash", side_effect=fake_poseidon_hash)
    @patch("django_zk_auth.crypto.proof_system.FieldElement", side_effect=DummyFE)
    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    def test_generate_auth_proof_success(self, mock_subproc, mock_fe, mock_poseidon, circuit_config):
        ps = ProofSystem(circuit_config)

        # Mock subprocess.run for witness and proof generation to succeed
        mock_subproc.return_value = MagicMock(returncode=0, stdout="OK", stderr="")

        # Patch the private methods to avoid actual file and subprocess
        with patch.object(ps, "_generate_witness", return_value=b"dummy_witness"), \
             patch.object(ps, "_generate_proof", return_value={
                 "proof": b'{"pi_a": [1,2,3]}',
                 "public_signals": [123, 456]
             }):

            proof = ps.generate_auth_proof("password", "salt", "nonce", "0xabc")

            assert isinstance(proof, ZKProof)
            assert proof.proof_type == circuit_config.proof_type
            assert proof.circuit_id == circuit_config.name
            assert proof.public_signals == [123, 456]
            assert proof.timestamp <= int(time.time())

    def test_init_raises_if_not_ready(self, tmp_path):
        config = CircuitConfig(
            name="bad_circuit",
            circuit_path=tmp_path / "missing.circom",
            r1cs_path=tmp_path / "missing.r1cs",
            wasm_path=tmp_path / "missing_js/missing.wasm",
            proving_key_path=tmp_path / "missing.zkey",
            verifying_key_path=tmp_path / "missing_vkey.json",
        )
        # All files missing, is_ready() is False
        with pytest.raises(RuntimeError, match="is not ready"):
            ProofSystem(config)

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    @patch("django_zk_auth.crypto.proof_system.cache")
    @patch("django_zk_auth.crypto.proof_system.time")
    def test_verify_proof_cache_hit(self, mock_time, mock_cache, mock_subproc, circuit_config):
        ps = ProofSystem(circuit_config)
        proof = ZKProof(
            proof=b'{"pi_a": [1,2,3]}',
            public_signals=[123, 456],
            proof_type=circuit_config.proof_type,
            circuit_id=circuit_config.name,
            timestamp=int(time.time())
        )
        mock_time.time.return_value = proof.timestamp + 10
        mock_cache.get.return_value = True  # Cache hit

        result = ps.verify_proof(proof)
        mock_cache.get.assert_called_once()
        assert result is True
        mock_subproc.assert_not_called()

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    @patch("django_zk_auth.crypto.proof_system.cache")
    @patch("django_zk_auth.crypto.proof_system.time")
    def test_verify_proof_expired(self, mock_time, mock_cache, mock_subproc, circuit_config):
        ps = ProofSystem(circuit_config)
        proof = ZKProof(
            proof=b'{"pi_a": [1,2,3]}',
            public_signals=[123, 456],
            proof_type=circuit_config.proof_type,
            circuit_id=circuit_config.name,
            timestamp=int(time.time()) - 1000  # expired
        )
        mock_time.time.return_value = int(time.time())
        mock_cache.get.return_value = None

        result = ps.verify_proof(proof)
        assert result is False
        mock_subproc.assert_not_called()

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    @patch("django_zk_auth.crypto.proof_system.cache")
    @patch("django_zk_auth.crypto.proof_system.time")
    def test_verify_proof_snarkjs_verification(self, mock_time, mock_cache, mock_subproc, circuit_config):
        ps = ProofSystem(circuit_config)
        proof = ZKProof(
            proof=b'{"pi_a": [1,2,3]}',
            public_signals=[123, 456],
            proof_type=circuit_config.proof_type,
            circuit_id=circuit_config.name,
            timestamp=int(time.time())
        )
        mock_time.time.return_value = proof.timestamp + 10
        mock_cache.get.return_value = None

        mock_subproc.return_value = MagicMock(stdout="OK", returncode=0)

        result = ps.verify_proof(proof)

        assert result is True
        mock_cache.set.assert_called_once()

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    def test_generate_witness_failure(self, mock_subproc, circuit_config):
        ps = ProofSystem(circuit_config)
        mock_subproc.side_effect = subprocess.CalledProcessError(1, "cmd")

        with pytest.raises(RuntimeError, match="Witness generation failed"):
            ps._generate_witness({"password": "1"})

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    def test_generate_proof_failure(self, mock_subproc, circuit_config):
        ps = ProofSystem(circuit_config)
        mock_subproc.side_effect = subprocess.CalledProcessError(1, "cmd")

        with pytest.raises(RuntimeError, match="Proof generation failed"):
            ps._generate_proof(b"witness", {"password": "1"})

    @patch("django_zk_auth.crypto.proof_system.subprocess.run")
    def test_verify_with_snarkjs_failure(self, mock_subproc, circuit_config):
        ps = ProofSystem(circuit_config)
        proof = ZKProof(
            proof=b'{"pi_a": [1]}',
            public_signals=[123],
            proof_type=circuit_config.proof_type,
            circuit_id=circuit_config.name,
            timestamp=int(time.time())
        )
        mock_subproc.side_effect = subprocess.CalledProcessError(1, "cmd")

        result = ps._verify_with_snarkjs(proof)
        assert result is False

@pytest.mark.django_db  # if your tests interact with DB or caching (optional here)
class TestProofCache:
    def setup_method(self):
        # Clear cache before each test
        cache.clear()
        self.cache = ProofCache(default_timeout=2)  # small timeout for tests
    
    def test_set_and_get_verification_result(self):
        proof_hash = "abc123"
        self.cache.set_verification_result(proof_hash, True)
        
        result = self.cache.get_verification_result(proof_hash)
        assert result is True
    
    def test_get_verification_result_none_if_not_set(self):
        result = self.cache.get_verification_result("nonexistent")
        assert result is None
    
    def test_invalidate_proof_removes_cache(self):
        proof_hash = "xyz789"
        self.cache.set_verification_result(proof_hash, True)
        
        assert self.cache.get_verification_result(proof_hash) is True
        
        self.cache.invalidate_proof(proof_hash)
        assert self.cache.get_verification_result(proof_hash) is None
    
    def test_set_verification_result_respects_timeout(self):
        proof_hash = "timeouttest"
        self.cache.set_verification_result(proof_hash, True, timeout=1)
        assert self.cache.get_verification_result(proof_hash) is True
        
        import time
        time.sleep(1.1)
        
        # Cache should have expired
        assert self.cache.get_verification_result(proof_hash) is None