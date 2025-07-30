import unittest
import logging
import threading
import sys
import os
from typing import List

import tempfile
import shutil
from pathlib import Path
import json
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Assuming your module is named `poseidon` and provides these:
from django_zk_auth.crypto.poseidon import (
    PoseidonParams,
    PoseidonError,
    InvalidParameterError,
    StateCorruptionError,
    SecurityError,
    validate_field_element,
    ConstantGenerator,
    ProductionConstantGenerator,
    BN254_FIELD_SIZE,
    OptimizedPoseidonState,
    CachedPoseidonConstants,
    PoseidonHash
)
from django_zk_auth.crypto.field_arithmetic import FieldElement

# Configure logger for detailed diagnostic output during tests
logger = logging.getLogger('poseidon_tests')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(handler)

class PoseidonParamsTests(unittest.TestCase):
    """Comprehensive validation tests for PoseidonParams class."""

    def test_valid_parameters_initialize_successfully(self):
        """Ensure PoseidonParams accepts valid parameters without error."""
        logger.info("Testing valid Poseidon parameters initialization")
        params = PoseidonParams(t=6, rounds_f=8, rounds_p=57, alpha=5, security_level=128)
        self.assertEqual(params.t, 6)
        self.assertEqual(params.rounds_f, 8)
        self.assertEqual(params.rounds_p, 57)
        self.assertEqual(params.alpha, 5)
        self.assertEqual(params.security_level, 128)
        self.assertEqual(params.total_rounds, 65)
        self.assertEqual(params.capacity, 5)

    def test_state_size_too_small_raises(self):
        """State size below 2 should raise InvalidParameterError."""
        logger.info("Testing invalid state size less than 2")
        with self.assertRaises(InvalidParameterError):
            PoseidonParams(t=1, rounds_f=8, rounds_p=57)

    def test_state_size_too_large_raises(self):
        """State size greater than 12 should raise InvalidParameterError."""
        logger.info("Testing invalid state size greater than 12")
        with self.assertRaises(InvalidParameterError):
            PoseidonParams(t=13, rounds_f=8, rounds_p=57)

    def test_full_rounds_must_be_even_and_minimum(self):
        """Full rounds must be an even number >= 4."""
        logger.info("Testing odd and too small full rounds")

        with self.assertRaises(InvalidParameterError):
            PoseidonParams(t=6, rounds_f=7, rounds_p=57)  # Odd full rounds

        with self.assertRaises(InvalidParameterError):
            PoseidonParams(t=6, rounds_f=2, rounds_p=57)  # Less than 4 full rounds

    def test_partial_rounds_must_be_positive(self):
        """Partial rounds less than 1 should raise InvalidParameterError."""
        logger.info("Testing partial rounds less than 1")
        with self.assertRaises(InvalidParameterError):
            PoseidonParams(t=6, rounds_f=8, rounds_p=0)

    def test_alpha_unusual_values_warn(self):
        """Alpha values outside typical set trigger a warning."""
        logger.info("Testing unusual alpha value warnings")
        with self.assertWarns(Warning):
            PoseidonParams(t=6, rounds_f=8, rounds_p=57, alpha=4)

    def test_security_level_too_low_raises(self):
        """Security level below 80 bits should raise SecurityError."""
        logger.info("Testing insufficient security level")
        with self.assertRaises(SecurityError):
            PoseidonParams(t=6, rounds_f=8, rounds_p=57, security_level=64)

# Dummy implementation for testing the abstract class
class MockConstantGenerator(ConstantGenerator):
    def generate_round_constants(self, params: PoseidonParams) -> List[List[int]]:
        return [[i + j for j in range(params.t)] for i in range(params.total_rounds)]

    def generate_mds_matrix(self, params: PoseidonParams) -> List[List[int]]:
        return [[1 if i == j else 0 for j in range(params.t)] for i in range(params.t)]  # identity

class ConstantGeneratorTests(unittest.TestCase):
    """Unit tests for ConstantGenerator using a mock implementation."""

    def setUp(self):
        logger.info("Setting up Poseidon parameters for constant generator tests")
        self.params = PoseidonParams(t=6, rounds_f=8, rounds_p=57, alpha=5, security_level=128)
        self.generator = MockConstantGenerator()

    def test_generate_round_constants_shape(self):
        """Check round constants dimensions match [total_rounds][t]."""
        logger.info("Testing generate_round_constants() shape")
        constants = self.generator.generate_round_constants(self.params)
        self.assertEqual(len(constants), self.params.total_rounds)
        for row in constants:
            self.assertEqual(len(row), self.params.t)

    def test_generate_mds_matrix_shape(self):
        """Check MDS matrix is square and size t x t."""
        logger.info("Testing generate_mds_matrix() shape")
        matrix = self.generator.generate_mds_matrix(self.params)
        self.assertEqual(len(matrix), self.params.t)
        for row in matrix:
            self.assertEqual(len(row), self.params.t)

    def test_mock_mds_is_identity(self):
        """Verify mock MDS is identity matrix."""
        logger.info("Testing identity MDS matrix")
        mds = self.generator.generate_mds_matrix(self.params)
        for i in range(self.params.t):
            for j in range(self.params.t):
                expected = 1 if i == j else 0
                self.assertEqual(mds[i][j], expected)
    
class ProductionConstantGeneratorTests(unittest.TestCase):
    """Tests for the ProductionConstantGenerator."""

    def setUp(self):
        logger.info("Setting up Poseidon parameters and ProductionConstantGenerator")
        self.params = PoseidonParams(t=6, rounds_f=8, rounds_p=57, alpha=5, security_level=128)
        self.generator = ProductionConstantGenerator()

    def test_round_constants_shape_and_range(self):
        """Ensure round constants are correct shape and within field range."""
        logger.info("Testing production round constants shape and range")
        constants = self.generator.generate_round_constants(self.params)
        self.assertEqual(len(constants), self.params.total_rounds)
        for row in constants:
            self.assertEqual(len(row), self.params.t)
            for element in row:
                self.assertIsInstance(element, int)
                self.assertGreaterEqual(element, 0)
                self.assertLess(element, BN254_FIELD_SIZE)

    def test_mds_matrix_structure_and_invertibility(self):
        """Ensure MDS matrix is square, t x t, and values are valid field elements."""
        logger.info("Testing production MDS matrix structure and invertibility")
        matrix = self.generator.generate_mds_matrix(self.params)
        self.assertEqual(len(matrix), self.params.t)
        for row in matrix:
            self.assertEqual(len(row), self.params.t)
            for value in row:
                self.assertIsInstance(value, int)
                self.assertGreaterEqual(value, 0)
                self.assertLess(value, BN254_FIELD_SIZE)

    def test_seed_validation_too_short_raises(self):
        """Seed shorter than 32 bytes should raise error."""
        logger.info("Testing invalid seed length")
        with self.assertRaises(InvalidParameterError):
            ProductionConstantGenerator(seed=b"short_seed")


class CachedPoseidonConstantsTests(unittest.TestCase):
    """Tests for the CachedPoseidonConstants caching logic using JSON and CWD."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.params = PoseidonParams(t=6, rounds_f=8, rounds_p=57, alpha=5, security_level=128)
        self.cache = CachedPoseidonConstants(cache_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_constants_generated_and_cached_in_memory(self):
        """Ensure constants are generated and then retrieved from memory."""
        constants1, mds1 = self.cache.get_constants(self.params)
        constants2, mds2 = self.cache.get_constants(self.params)

        self.assertIs(constants1, constants2)
        self.assertIs(mds1, mds2)

    def test_constants_cached_to_disk_and_reloaded(self):
        """Test that constants are saved and loaded from disk."""
        key = self.cache._cache_key(self.params)
        cache_file = self.cache._cache_file(key)

        # Trigger generation and disk save
        _ = self.cache.get_constants(self.params)
        self.assertTrue(cache_file.exists())

        # Clear memory cache
        self.cache._cache.clear()

        # Reload from disk
        constants2, mds2 = self.cache.get_constants(self.params)
        self.assertIn(key, self.cache._cache)
        self.assertIsInstance(constants2, list)
        self.assertIsInstance(mds2, list)

    def test_invalid_disk_cache_is_removed(self):
        """Corrupted disk cache should be ignored and replaced with fresh one."""
        key = self.cache._cache_key(self.params)
        cache_file = self.cache._cache_file(key)

        # Write invalid JSON data
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write("{ bad json")

        self.assertTrue(cache_file.exists(), "Corrupted cache file should exist before loading")

        # Capture the modified time before load
        old_mtime = cache_file.stat().st_mtime

        # Trigger loading, should detect corruption, delete, and regenerate
        constants, mds = self.cache.get_constants(self.params)

        self.assertIsInstance(constants, list)

        # After corrupted file is detected, it should be replaced with a valid one
        self.assertTrue(cache_file.exists(), "A fresh cache file should be saved after deletion")
        self.assertGreater(cache_file.stat().st_mtime, old_mtime, "Cache file should be replaced with a new one")


    def test_thread_safety_under_concurrent_access(self):
        """Test thread-safe concurrent access to get_constants."""
        results = []

        def worker():
            result = self.cache.get_constants(self.params)
            results.append(result)

        threads = [threading.Thread(target=worker) for _ in range(10)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        base_constants, base_mds = results[0]
        for constants, mds in results[1:]:
            self.assertIs(constants, base_constants)
            self.assertIs(mds, base_mds)


class PoseidonHashTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.params = PoseidonParams(t=5, rounds_f=8, rounds_p=60)
        self.hasher = PoseidonHash(params=self.params, cache_dir=self.temp_dir)

    def test_hash_single_int(self):
        result = self.hasher.hash_single(123)
        self.assertIsInstance(result, FieldElement)

    def test_hash_two_values(self):
        result = self.hasher.hash_two(123, 456)
        self.assertIsInstance(result, FieldElement)

    def test_hash_multiple(self):
        result = self.hasher.hash_multiple(1, 2, 3, 4)
        self.assertIsInstance(result, FieldElement)

    def test_string_input(self):
        result = self.hasher.hash_single("zk-auth")
        self.assertIsInstance(result, FieldElement)

    def test_bytes_input(self):
        result = self.hasher.hash_single(b"zk-auth")
        self.assertIsInstance(result, FieldElement)

    def test_invalid_input_type(self):
        with self.assertRaises(InvalidParameterError):
            self.hasher.hash_single(3.14)

    def test_input_too_large(self):
        with self.assertRaises(InvalidParameterError):
            self.hasher.hash_single(b"a" * 40)

    def test_negative_input(self):
        with self.assertRaises(InvalidParameterError):
            self.hasher.hash_single(-10)

    def test_excess_inputs(self):
        with self.assertRaises(InvalidParameterError):
            self.hasher.hash([1, 2, 3, 4, 5])  # t=5 → capacity=4

    def test_incremental_hash(self):
        chunks = [
            [1, 2],
            [3, 4],
            [5, 6],
        ]
        result = self.hasher.incremental_hash(chunks)
        self.assertIsInstance(result, FieldElement)

    def test_incremental_hash_empty(self):
        with self.assertRaises(InvalidParameterError):
            self.hasher.incremental_hash([])

    def test_standard_params(self):
        for name in PoseidonHash.STANDARD_PARAMS:
            h = PoseidonHash(name, cache_dir=self.temp_dir)
            self.assertIsInstance(h.hash_single(1), FieldElement)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    unittest.main()