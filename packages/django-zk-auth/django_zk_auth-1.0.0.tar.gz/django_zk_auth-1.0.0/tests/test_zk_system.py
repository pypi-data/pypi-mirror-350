import os
import sys
import shutil
import tempfile
from pathlib import Path
from unittest import mock, TestCase

import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from django_zk_auth.crypto.zk_system import ZKSystem
from django_zk_auth.crypto.proof_system import CircuitConfig, ProofSystem

from unittest.mock import patch, MagicMock
import pytest

@pytest.fixture(autouse=True)
def mock_compile_auth_circuit():
    with patch('django_zk_auth.crypto.zk_system.CircuitCompiler.compile_auth_circuit') as mock_compile:
        mock_config = MagicMock()
        mock_config.name = 'auth'
        mock_compile.return_value = mock_config
        yield


# Helper to create a dummy CircuitConfig with .is_ready() stubbed
def create_dummy_circuit_config(name='auth'):
    dummy = mock.create_autospec(CircuitConfig, instance=True)
    dummy.name = name
    dummy.is_ready.return_value = True
    dummy.circuit_path = Path('/tmp/dummy.circom')
    dummy.r1cs_path = Path('/tmp/dummy.r1cs')
    dummy.wasm_path = Path('/tmp/dummy.wasm')
    dummy.proving_key_path = Path('/tmp/dummy.zkey')
    dummy.verifying_key_path = Path('/tmp/dummy.vkey.json')
    return dummy


class TestZKSystem(TestCase):
    def setUp(self):
        # Patch settings for base_dir and DEBUG
        self.tmp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp_dir)

        self.patcher_base_dir = mock.patch.object(settings, 'BASE_DIR', self.tmp_dir)
        self.patcher_debug = mock.patch.object(settings, 'DEBUG', False)
        self.mock_base_dir = self.patcher_base_dir.start()
        self.mock_debug = self.patcher_debug.start()
        self.addCleanup(self.patcher_base_dir.stop)
        self.addCleanup(self.patcher_debug.stop)

        # Reset singleton state before each test
        ZKSystem._initialized = False
        ZKSystem._instance = None

    def test_initialize_creates_instance_and_directories(self):
        zk_system = ZKSystem.initialize()
        self.assertIsInstance(zk_system, ZKSystem)
        self.assertTrue(ZKSystem._initialized)
        self.assertIs(ZKSystem._instance, zk_system)

        # Directories exist
        for key in ['circuit_path', 'proving_key_path', 'verifying_key_path']:
            path = Path(zk_system.config[key])
            self.assertTrue(path.exists())
            self.assertTrue(path.is_dir())

    def test_initialize_returns_singleton_instance(self):
        first_instance = ZKSystem.initialize()
        second_instance = ZKSystem.initialize()
        self.assertIs(first_instance, second_instance)

    @mock.patch('django_zk_auth.crypto.zk_system.CircuitCompiler.compile_auth_circuit')
    @mock.patch('django_zk_auth.crypto.zk_system.ProofSystem')
    def test_initialize_compiles_circuit_and_creates_proof_system(self, mock_proof_system, mock_compile):
        dummy_config = create_dummy_circuit_config()
        mock_compile.return_value = dummy_config

        zk_system = ZKSystem.initialize()

        mock_compile.assert_called_once()
        mock_proof_system.assert_called_once_with(dummy_config)

        self.assertIn('auth', zk_system.circuits)
        self.assertIn('auth', zk_system.proof_systems)
        self.assertIs(zk_system.circuits['auth'], dummy_config)

    @mock.patch('django_zk_auth.crypto.zk_system.CircuitCompiler.compile_auth_circuit', side_effect=Exception("fail"))
    def test_initialize_raises_or_creates_mock_circuits_debug_off(self, mock_compile):
        # DEBUG = False raises
        with mock.patch.object(settings, 'DEBUG', False):
            with self.assertRaises(ImproperlyConfigured):
                ZKSystem.initialize()

    @mock.patch('django_zk_auth.crypto.zk_system.CircuitCompiler.compile_auth_circuit', side_effect=Exception("fail"))
    def test_initialize_creates_mock_circuits_debug_on(self, mock_compile):
        with mock.patch.object(settings, 'DEBUG', True):
            zk_system = ZKSystem.initialize()
            self.assertIn('auth', zk_system.circuits)
            circuit = zk_system.circuits['auth']
            self.assertEqual(circuit.name, 'auth')
            # The ProofSystem should NOT be created for mock circuits
            self.assertNotIn('auth', zk_system.proof_systems)

    def test_get_instance_raises_if_not_initialized(self):
        with self.assertRaises(RuntimeError):
            ZKSystem.get_instance()

    def test_get_instance_returns_existing_instance(self):
        instance = ZKSystem.initialize()
        retrieved = ZKSystem.get_instance()
        self.assertIs(instance, retrieved)

    def test_get_auth_system_returns_proof_system(self):
        with mock.patch('django_zk_auth.crypto.zk_system.CircuitCompiler.compile_auth_circuit') as mock_compile, \
             mock.patch('django_zk_auth.crypto.zk_system.ProofSystem') as mock_proof_system:

            dummy_config = create_dummy_circuit_config()
            mock_compile.return_value = dummy_config
            mock_proof_system.return_value = 'proof_system_instance'

            zk_system = ZKSystem.initialize()
            auth_system = zk_system.get_auth_system()
            self.assertEqual(auth_system, 'proof_system_instance')

    def test_is_production_ready_true(self):
        dummy_config = create_dummy_circuit_config()
        zk = ZKSystem({
            'circuit_path': self.tmp_dir,
            'proving_key_path': self.tmp_dir,
            'verifying_key_path': self.tmp_dir,
            'proof_system': None,
            'hash_function': None,
            'security_level': 128,
        })
        zk.circuits['auth'] = dummy_config
        zk.proof_systems['auth'] = mock.Mock()
        dummy_config.is_ready.return_value = True

        with mock.patch.object(settings, 'DEBUG', False):
            self.assertTrue(zk.is_production_ready())

    def test_is_production_ready_false_if_debug(self):
        dummy_config = create_dummy_circuit_config()
        zk = ZKSystem({
            'circuit_path': self.tmp_dir,
            'proving_key_path': self.tmp_dir,
            'verifying_key_path': self.tmp_dir,
            'proof_system': None,
            'hash_function': None,
            'security_level': 128,
        })
        zk.circuits['auth'] = dummy_config
        zk.proof_systems['auth'] = mock.Mock()
        dummy_config.is_ready.return_value = True

        with mock.patch.object(settings, 'DEBUG', True):
            self.assertFalse(zk.is_production_ready())

    def test_is_production_ready_false_if_no_auth(self):
        zk = ZKSystem({
            'circuit_path': self.tmp_dir,
            'proving_key_path': self.tmp_dir,
            'verifying_key_path': self.tmp_dir,
            'proof_system': None,
            'hash_function': None,
            'security_level': 128,
        })
        with mock.patch.object(settings, 'DEBUG', False):
            self.assertFalse(zk.is_production_ready())

    def test_get_system_info_contains_expected_keys(self):
        zk = ZKSystem.initialize()
        info = zk.get_system_info()
        self.assertIn('initialized', info)
        self.assertIn('production_ready', info)
        self.assertIn('circuits', info)
        self.assertIn('proof_systems', info)
        self.assertIn('config', info)
        self.assertIn('proof_system', info['config'])
        self.assertIn('hash_function', info['config'])
        self.assertIn('security_level', info['config'])
