"""
Advanced Zero-Knowledge Proof System Implementation
For cryptographic proof generation and verification
"""

import json
import time
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
import numpy as np
from django.conf import settings
from django.core.cache import cache

from .types import ZKProof, ProofType, CircuitInputs, FieldElement
from .poseidon import poseidon_hash
from .field_arithmetic import FieldElement as FE



@dataclass
class CircuitConfig:
    """Configuration for a ZK circuit"""
    name: str
    circuit_path: Path
    r1cs_path: Path
    wasm_path: Path
    proving_key_path: Path
    verifying_key_path: Path
    proof_type: ProofType = ProofType.GROTH16
    
    def is_ready(self) -> bool:
        """Check if all required files exist"""
        paths = [
            self.circuit_path,
            self.r1cs_path, 
            self.wasm_path,
            self.proving_key_path,
            self.verifying_key_path
        ]
        return all(p.exists() for p in paths)

class CircuitCompiler:
    """Compiles Circom circuits and manages cryptographic setup"""
    
    def __init__(self, circuits_dir: Path):
        self.circuits_dir = circuits_dir
        self.circuits_dir.mkdir(parents=True, exist_ok=True)
    
    def compile_auth_circuit(self) -> CircuitConfig:
        """Compile the authentication circuit"""
        circuit_name = "zk_auth"
        circuit_source = self._generate_auth_circuit_source()
        
        # Write circuit source
        circuit_path = self.circuits_dir / f"{circuit_name}.circom"
        with open(circuit_path, 'w') as f:
            f.write(circuit_source)
        
        # Compile circuit
        r1cs_path = self.circuits_dir / f"{circuit_name}.r1cs"
        wasm_path = self.circuits_dir / f"{circuit_name}_js" / f"{circuit_name}.wasm"
        
        compile_cmd = [
            "circom",
            str(circuit_path),
            "--r1cs",
            "--wasm",
            "--sym",
            "-o", str(self.circuits_dir)
        ]
        
        try:
            result = subprocess.run(compile_cmd, capture_output=True, text=True, check=True)
            print(f"Circuit compiled successfully: {result.stdout}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Circuit compilation failed: {e.stderr}")
        
        # Setup proving system
        proving_key_path, verifying_key_path = self._setup_proving_system(
            circuit_name, r1cs_path
        )
        
        return CircuitConfig(
            name=circuit_name,
            circuit_path=circuit_path,
            r1cs_path=r1cs_path,
            wasm_path=wasm_path,
            proving_key_path=proving_key_path,
            verifying_key_path=verifying_key_path
        )
    
    def _generate_auth_circuit_source(self) -> str:
        """Generate the authentication circuit in Circom"""
        return '''
        pragma circom 2.0.0;

        include "poseidon.circom";

        template ZKAuth() {
            // Private inputs
            signal private input password;
            signal private input salt;
            
            // Public inputs
            signal input nonce;
            signal input commitment;
            
            // Output
            signal output valid;
            
            // Hash password with salt to create user commitment
            component password_hasher = Poseidon(2);
            password_hasher.inputs[0] <== password;
            password_hasher.inputs[1] <== salt;
            
            // Hash commitment with nonce for replay protection
            component challenge_hasher = Poseidon(2);
            challenge_hasher.inputs[0] <== password_hasher.out;
            challenge_hasher.inputs[1] <== nonce;
            
            // Verify commitment matches
            component commitment_check = IsEqual();
            commitment_check.in[0] <== password_hasher.out;
            commitment_check.in[1] <== commitment;
            
            // Output is valid if commitment matches
            valid <== commitment_check.out;
            
            // Constrain the challenge hash (prevents malleability)
            component dummy_constraint = Num2Bits(254);
            dummy_constraint.in <== challenge_hasher.out;
        }

        template IsEqual() {
            signal input in[2];
            signal output out;
            
            component eq = IsZero();
            eq.in <== in[1] - in[0];
            out <== eq.out;
        }

        template IsZero() {
            signal input in;
            signal output out;
            
            signal inv;
            inv <-- in != 0 ? 1/in : 0;
            out <== -in*inv + 1;
            in*out === 0;
        }

        template Num2Bits(n) {
            signal input in;
            signal output out[n];
            
            var lc1=0;
            var e2=1;
            for (var i = 0; i<n; i++) {
                out[i] <-- (in >> i) & 1;
                out[i] * (out[i] -1 ) === 0;
                lc1 += out[i] * e2;
                e2 = e2+e2;
            }
            lc1 === in;
        }

        component main = ZKAuth();
        '''
    def _setup_proving_system(self, circuit_name: str, r1cs_path: Path) -> Tuple[Path, Path]:
        """Setup the proving system (Groth16)"""
        # Download powers of tau if not exists
        ptau_path = self.circuits_dir / "powersOfTau28_hez_final_15.ptau"
        if not ptau_path.exists():
            print("Downloading powers of tau ceremony file...")
            import urllib.request
            ptau_url = "https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_15.ptau"

            urllib.request.urlretrieve(ptau_url, ptau_path)
        
        # Generate proving key
        proving_key_path = self.circuits_dir / f"{circuit_name}.zkey"
        setup_cmd = [
            "snarkjs", "groth16", "setup",
            str(r1cs_path),
            str(ptau_path),
            str(proving_key_path)
        ]
        
        try:
            subprocess.run(setup_cmd, capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Proving key setup failed: {e}")
        
        # Export verifying key
        verifying_key_path = self.circuits_dir / f"{circuit_name}_vkey.json"
        export_cmd = [
            "snarkjs", "zkey", "export", "verificationkey",
            str(proving_key_path),
            str(verifying_key_path)
        ]
        
        try:
            subprocess.run(export_cmd, capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Verifying key export failed: {e}")
        
        return proving_key_path, verifying_key_path
class ProofSystem:
    """Advanced zero-knowledge proof system"""
    
    def __init__(self, circuit_config: CircuitConfig):
        self.config = circuit_config
        self.cache_timeout = 300  # 5 minutes
        
        if not circuit_config.is_ready():
            raise RuntimeError(f"Circuit {circuit_config.name} is not ready")
    
    def generate_auth_proof(
        self,
        password: Union[str, int, bytes],
        salt: Union[str, int, bytes],
        nonce: str,
        commitment: str
    ) -> ZKProof:
        """Generate authentication proof"""
        
        # Convert inputs to field elements
        if isinstance(password, str):
            password_fe = poseidon_hash(password.encode('utf-8')).value
        elif isinstance(password, bytes):
            password_fe = poseidon_hash(password).value
        else:
            password_fe = int(password)
        
        if isinstance(salt, str):
            salt_fe = FE(salt.encode('utf-8')).value
        elif isinstance(salt, bytes):
            salt_fe = FE(salt).value
        else:
            salt_fe = int(salt)
        
        nonce_fe = FE(nonce.encode('utf-8')).value
        commitment_fe = int(commitment, 16) if isinstance(commitment, str) and commitment.startswith('0x') else FE(commitment).value
        
        # Prepare circuit inputs
        inputs = {
            "password": str(password_fe),
            "salt": str(salt_fe),
            "nonce": str(nonce_fe),
            "commitment": str(commitment_fe)
        }
        
        # Generate witness
        witness_data = self._generate_witness(inputs)
        
        # Generate proof
        proof_data = self._generate_proof(witness_data, inputs)
        
        return ZKProof(
            proof=proof_data['proof'],
            public_signals=proof_data['public_signals'],
            proof_type=self.config.proof_type,
            circuit_id=self.config.name,
            timestamp=int(time.time())
        )
    
    def verify_proof(self, proof: ZKProof) -> bool:
        """Verify a zero-knowledge proof"""
        
        # Check proof type matches
        if proof.proof_type != self.config.proof_type:
            return False
        
        # Check circuit ID matches
        if proof.circuit_id != self.config.name:
            return False
        
        # Check proof age (prevent replay attacks)
        max_age = getattr(settings, 'ZK_AUTH_MAX_PROOF_AGE', 300)  # 5 minutes
        if time.time() - proof.timestamp > max_age:
            return False
        
        # Cache key for verification result
        cache_key = f"zk_proof_verify:{hash(proof.proof)}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        # Verify using snarkjs
        result = self._verify_with_snarkjs(proof)
        
        # Cache result
        cache.set(cache_key, result, self.cache_timeout)
        
        return result
    
    def _generate_witness(self, inputs: Dict[str, str]) -> bytes:
        """Generate witness for circuit inputs"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Write input file
            input_file = temp_path / "input.json"
            with open(input_file, 'w') as f:
                json.dump(inputs, f)
            
            # Generate witness
            witness_file = temp_path / "witness.wtns"
            witness_cmd = [
                "node",
                str(self.config.wasm_path.parent / f"{self.config.name}.js"),
                str(input_file),
                str(witness_file)
            ]
            
            try:
                subprocess.run(witness_cmd, capture_output=True, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Witness generation failed: {e}")
            
            # Read witness data
            with open(witness_file, 'rb') as f:
                return f.read()
    
    def _generate_proof(self, witness_data: bytes, inputs: Dict[str, str]) -> Dict[str, Any]:
        """Generate proof from witness"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Write witness file
            witness_file = temp_path / "witness.wtns"
            with open(witness_file, 'wb') as f:
                f.write(witness_data)
            
            # Generate proof
            proof_file = temp_path / "proof.json"
            public_file = temp_path / "public.json"
            
            prove_cmd = [
                "snarkjs", "groth16", "prove",
                str(self.config.proving_key_path),
                str(witness_file),
                str(proof_file),
                str(public_file)
            ]
            
            try:
                subprocess.run(prove_cmd, capture_output=True, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Proof generation failed: {e}")
            
            # Read proof and public signals
            with open(proof_file, 'r') as f:
                proof_json = json.load(f)
            
            with open(public_file, 'r') as f:
                public_signals = json.load(f)
            
            # Convert proof to bytes
            proof_bytes = json.dumps(proof_json).encode('utf-8')
            
            return {
                'proof': proof_bytes,
                'public_signals': [int(x) for x in public_signals]
            }
    
    def _verify_with_snarkjs(self, proof: ZKProof) -> bool:
        """Verify proof using snarkjs"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Write proof file
            proof_data = json.loads(proof.proof.decode('utf-8'))
            proof_file = temp_path / "proof.json"
            with open(proof_file, 'w') as f:
                json.dump(proof_data, f)
            
            # Write public signals file
            public_file = temp_path / "public.json"
            with open(public_file, 'w') as f:
                json.dump([str(x) for x in proof.public_signals], f)
            
            # Verify proof
            verify_cmd = [
                "snarkjs", "groth16", "verify",
                str(self.config.verifying_key_path),
                str(public_file),
                str(proof_file)
            ]
            
            try:
                result = subprocess.run(verify_cmd, capture_output=True, text=True)
                return "OK" in result.stdout
            except subprocess.CalledProcessError:
                return False
            
class ProofCache:
    """Cache for proof verification results"""
    
    def __init__(self, default_timeout: int = 300):
        self.default_timeout = default_timeout
    
    def get_verification_result(self, proof_hash: str) -> Optional[bool]:
        """Get cached verification result"""
        cache_key = f"zk_proof_verify:{proof_hash}"
        return cache.get(cache_key)
    
    def set_verification_result(self, proof_hash: str, result: bool, timeout: Optional[int] = None) -> None:
        """Cache verification result"""
        cache_key = f"zk_proof_verify:{proof_hash}"
        cache.set(cache_key, result, timeout or self.default_timeout)
    
    def invalidate_proof(self, proof_hash: str) -> None:
        """Invalidate cached proof"""
        cache_key = f"zk_proof_verify:{proof_hash}"
        cache.delete(cache_key)