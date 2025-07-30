"""
Main ZK System coordinator
Manages circuits, proof systems, and cryptographic operations
"""

from typing import Dict, Optional, Any
from pathlib import Path
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .proof_system import ProofSystem, CircuitCompiler, CircuitConfig
from .types import ZKSystemConfig, ProofType, HashFunction


class ZKSystem:
    """Central coordinator for Zero-Knowledge cryptographic operations"""
    
    _instance: Optional['ZKSystem'] = None
    _initialized: bool = False
    
    def __init__(self, config: ZKSystemConfig):
        self.config = config
        self.circuits: Dict[str, CircuitConfig] = {}
        self.proof_systems: Dict[str, ProofSystem] = {}
        self._setup_directories()
    
    @classmethod
    def initialize(cls, config: Optional[Dict[str, Any]] = None) -> 'ZKSystem':
        """Initialize the ZK system with configuration"""
        if cls._initialized:
            return cls._instance
        
        # Default configuration
        default_config: ZKSystemConfig = {
            'proof_system': ProofType.GROTH16,
            'hash_function': HashFunction.POSEIDON,
            'circuit_path': str(Path(settings.BASE_DIR) / 'zk_circuits'),
            'proving_key_path': str(Path(settings.BASE_DIR) / 'zk_keys' / 'proving'),
            'verifying_key_path': str(Path(settings.BASE_DIR) / 'zk_keys' / 'verifying'),
            'field_size': 21888242871839275222246405745257275088548364400416034343698204186575808495617,
            'security_level': 128,
            'enable_audit_logging': True,
            'max_proof_age_seconds': 300,
            'rate_limit_window_seconds': 60,
            'max_requests_per_window': 10,
        }
        
        # Merge with provided config
        if config:
            default_config.update(config)
        
        # Create instance
        cls._instance = cls(default_config)
        cls._instance._initialize_circuits()
        cls._initialized = True
        
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'ZKSystem':
        """Get the singleton instance"""
        if not cls._initialized or cls._instance is None:
            raise RuntimeError("ZK System not initialized. Call initialize() first.")
        return cls._instance
    
    def _setup_directories(self) -> None:
        """Create necessary directories"""
        dirs = [
            Path(self.config['circuit_path']),
            Path(self.config['proving_key_path']),
            Path(self.config['verifying_key_path']),
        ]
        
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _initialize_circuits(self) -> None:
        """Initialize and compile circuits"""
        circuits_dir = Path(self.config['circuit_path'])
        compiler = CircuitCompiler(circuits_dir)
        
        try:
            # Compile authentication circuit
            auth_config = compiler.compile_auth_circuit()
            self.circuits['auth'] = auth_config
            self.proof_systems['auth'] = ProofSystem(auth_config)
            
        except Exception as e:
            # In development, we might not have circom installed
            # Create mock circuit config for testing
            if settings.DEBUG:
                self._create_mock_circuits()
            else:
                raise ImproperlyConfigured(f"Failed to initialize ZK circuits: {e}")
    
    def _create_mock_circuits(self) -> None:
        """Create mock circuits for development/testing"""
        circuits_dir = Path(self.config['circuit_path'])
        
        # Create mock files
        mock_files = [
            'zk_auth.circom',
            'zk_auth.r1cs', 
            'zk_auth_js/zk_auth.wasm',
            'zk_auth.zkey',
            'zk_auth_vkey.json'
        ]
        
        for file_path in mock_files:
            full_path = circuits_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            if not full_path.exists():
                full_path.write_text('mock')
        
        # Create mock circuit config
        mock_config = CircuitConfig(
            name='auth',
            circuit_path=circuits_dir / 'zk_auth.circom',
            r1cs_path=circuits_dir / 'zk_auth.r1cs',
            wasm_path=circuits_dir / 'zk_auth_js' / 'zk_auth.wasm',
            proving_key_path=circuits_dir / 'zk_auth.zkey',
            verifying_key_path=circuits_dir / 'zk_auth_vkey.json'
        )
        
        self.circuits['auth'] = mock_config
        # Don't create ProofSystem for mock - it will fail
    
    def get_auth_system(self) -> Optional[ProofSystem]:
        """Get the authentication proof system"""
        return self.proof_systems.get('auth')
    
    def is_production_ready(self) -> bool:
        """Check if system is ready for production use"""
        return (
            'auth' in self.proof_systems and
            all(circuit.is_ready() for circuit in self.circuits.values()) and
            not settings.DEBUG
        )
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information for diagnostics"""
        return {
            'initialized': self._initialized,
            'production_ready': self.is_production_ready(),
            'circuits': list(self.circuits.keys()),
            'proof_systems': list(self.proof_systems.keys()),
            'config': {
                'proof_system': self.config['proof_system'].value,
                'hash_function': self.config['hash_function'].value,
                'security_level': self.config['security_level'],
            }
        }