"""Tests for finite field arithmetic implementation"""
import pytest
import sys
import os
import logging


# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from django_zk_auth.crypto.field_arithmetic import (
    FieldElement, 
    BN254_FIELD_SIZE,
    ZERO,
    ONE,
    batch_multiply,
    batch_add,
    polynomial_evaluate,
    lagrange_interpolation,
    field_elements_from_bytes,
    field_elements_to_bytes
)


class TestFieldElement:
    """Test cases for FieldElement class"""
    
    def test_initialization(self):
        """Test different ways to initialize FieldElement"""
        # Integer initialization
        a = FieldElement(42)
        assert a.value == 42
        
        # String initialization
        b = FieldElement("123")
        assert b.value == 123
        
        # Hex string initialization
        c = FieldElement("0x1a")
        assert c.value == 26
        
        # Bytes initialization
        d = FieldElement(b'\x00\x01')
        assert d.value == 1
    
    def test_modular_reduction(self):
        """Test that values are properly reduced modulo field size"""
        # Test with value larger than field size
        large_val = BN254_FIELD_SIZE + 100
        a = FieldElement(large_val)
        assert a.value == 100
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic operations"""
        a = FieldElement(10)
        b = FieldElement(5)
        
        # Addition
        c = a + b
        assert c.value == 15
        
        # Subtraction
        d = a - b
        assert d.value == 5
        
        # Multiplication
        e = a * b
        assert e.value == 50
        
        # Division
        f = a / b
        assert f.value == 2
    
    def test_modular_arithmetic(self):
        """Test arithmetic operations respect field modulus"""
        # Test subtraction that would go negative
        a = FieldElement(5)
        b = FieldElement(10)
        c = a - b
        # Should wrap around: 5 - 10 = -5 ≡ (field_size - 5) mod field_size
        expected = BN254_FIELD_SIZE - 5
        assert c.value == expected
    
    def test_exponentiation(self):
        """Test exponentiation"""
        a = FieldElement(2)
        b = a ** 3
        assert b.value == 8
        
        # Test with larger exponent
        c = a ** 10
        assert c.value == 1024
    
    def test_inverse(self):
        """Test multiplicative inverse"""
        a = FieldElement(7)
        a_inv = a.inverse()
        
        # a * a^(-1) should equal 1
        product = a * a_inv
        assert product.value == 1
    
    def test_zero_element(self):
        """Test zero element properties"""
        zero = FieldElement(0)
        a = FieldElement(42)
        
        # Addition with zero
        assert (a + zero).value == a.value
        assert (zero + a).value == a.value
        
        # Multiplication with zero
        assert (a * zero).value == 0
        assert (zero * a).value == 0
        
        # Check is_zero method
        assert zero.is_zero()
        assert not a.is_zero()
    
    def test_one_element(self):
        """Test one element properties"""
        one = FieldElement(1)
        a = FieldElement(42)
        
        # Multiplication with one
        assert (a * one).value == a.value
        assert (one * a).value == a.value
    
    def test_equality(self):
        """Test equality comparison"""
        a = FieldElement(42)
        b = FieldElement(42)
        c = FieldElement(43)
        
        assert a == b
        assert not (a == c)
        
        # Test equality with integer
        assert a == 42
        assert not (a == 43)
    
    def test_string_representation(self):
        """Test string representation"""
        a = FieldElement(42)
        assert str(a) == "42"
        assert "FieldElement(42)" in repr(a)
    
    def test_hash(self):
        """Test hash function"""
        a = FieldElement(42)
        b = FieldElement(42)
        c = FieldElement(43)
        
        # Equal elements should have equal hashes
        assert hash(a) == hash(b)
        
        # Different elements should (likely) have different hashes
        assert hash(a) != hash(c)
        
        # Should be usable in sets and dicts
        s = {a, b, c}
        assert len(s) == 2  # a and b are the same
    
    def test_byte_conversion(self):
        """Test conversion to bytes"""
        a = FieldElement(0x1234)
        bytes_repr = a.to_bytes()
        
        # Should be 32 bytes by default
        assert len(bytes_repr) == 32
        
        # Convert back and check
        b = FieldElement(bytes_repr)
        assert a == b
    
    def test_hex_conversion(self):
        """Test conversion to hex"""
        a = FieldElement(255)
        hex_repr = a.to_hex()
        assert hex_repr == "0xff"

class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_batch_multiply(self):
        """Test batch multiplication"""
        elements = [FieldElement(2), FieldElement(3), FieldElement(4)]
        result = batch_multiply(elements)
        assert result.value == 24
    
    def test_batch_add(self):
        """Test batch addition"""
        elements = [FieldElement(2), FieldElement(3), FieldElement(4)]
        result = batch_add(elements)
        assert result.value == 9
    
    def test_polynomial_evaluate(self):
        """Test polynomial evaluation"""
        # Polynomial: 2x^2 + 3x + 1
        coefficients = [FieldElement(1), FieldElement(3), FieldElement(2)]  # constant term first
        x = FieldElement(2)
        
        # Should be: 2*4 + 3*2 + 1 = 8 + 6 + 1 = 15
        result = polynomial_evaluate(coefficients, x)
        assert result.value == 15
    
    def test_lagrange_interpolation(self):
        """Test Lagrange interpolation"""
        # Simple case: interpolate through points (0,1), (1,2), (2,5)
        # This should give us the polynomial x^2 + 1
        points = [(0, 1), (1, 2), (2, 5)]
        
        # Evaluate at x = 3: should be 3^2 + 1 = 10
        x = FieldElement(3)
        result = lagrange_interpolation(points, x)
        assert result.value == 10
        
        # Check that it passes through the original points
        for point_x, point_y in points:
            x_elem = FieldElement(point_x)
            interpolated = lagrange_interpolation(points, x_elem)
            assert interpolated.value == point_y
    
    def test_constants(self):
        """Test predefined constants"""
        assert ZERO.value == 0
        assert ONE.value == 1
        assert ZERO.is_zero()
        assert not ONE.is_zero()

class TestZKSpecificOperations:
    """Test operations commonly used in ZK proofs"""
    
    def test_field_properties(self):
        """Test that field operations satisfy expected properties"""
        a = FieldElement(17)
        b = FieldElement(23)
        c = FieldElement(31)
        
        # Commutativity
        assert a + b == b + a
        assert a * b == b * a
        
        # Associativity
        assert (a + b) + c == a + (b + c)
        assert (a * b) * c == a * (b * c)
        
        # Distributivity
        assert a * (b + c) == (a * b) + (a * c)
    
    def test_polynomial_operations(self):
        """Test polynomial operations for ZK applications"""
        # Test that polynomial evaluation is consistent
        coeffs = [FieldElement(1), FieldElement(2), FieldElement(3)]  # 3x^2 + 2x + 1
        
        x1 = FieldElement(5)
        x2 = FieldElement(7)
        
        y1 = polynomial_evaluate(coeffs, x1)
        y2 = polynomial_evaluate(coeffs, x2)
        
        # Values should be different for different inputs
        assert y1 != y2
        
        # Should be deterministic
        y1_again = polynomial_evaluate(coeffs, x1)
        assert y1 == y1_again
    
    def test_large_numbers(self):
        """Test operations with large numbers typical in ZK"""
        # Use numbers close to field size
        large1 = FieldElement(BN254_FIELD_SIZE - 1)
        large2 = FieldElement(BN254_FIELD_SIZE - 2)
        
        # Should handle arithmetic correctly
        sum_result = large1 + large2
        # (p-1) + (p-2) = 2p - 3 ≡ -3 ≡ p-3 (mod p)
        expected = BN254_FIELD_SIZE - 3
        assert sum_result.value == expected
        
        # Test multiplication
        prod_result = large1 * large2
        # Should not overflow and should be reduced properly
        assert isinstance(prod_result.value, int)
        assert 0 <= prod_result.value < BN254_FIELD_SIZE

class TestByteConversionFunctions:
    """Test byte conversion utility functions"""
    
    def test_field_elements_from_bytes_basic(self):
        """Test basic conversion from bytes to field elements"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes
        
        # Test with simple data
        data = b"Hello World!"
        elements = field_elements_from_bytes(data)
        
        # Should create at least one element
        assert len(elements) > 0
        
        # Each element should be valid
        for elem in elements:
            assert isinstance(elem, FieldElement)
            assert 0 <= elem.value < BN254_FIELD_SIZE
    
    def test_field_elements_from_bytes_chunk_size(self):
        """Test conversion with different chunk sizes"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes
        
        data = b"A" * 100  # 100 bytes of 'A'
        
        # Test with default chunk size (31)
        elements_31 = field_elements_from_bytes(data, chunk_size=31)
        expected_chunks_31 = (len(data) + 30) // 31  # Ceiling division
        assert len(elements_31) == expected_chunks_31
        
        # Test with smaller chunk size
        elements_16 = field_elements_from_bytes(data, chunk_size=16)
        expected_chunks_16 = (len(data) + 15) // 16
        assert len(elements_16) == expected_chunks_16
        
        # More chunks with smaller size
        assert len(elements_16) > len(elements_31)
    
    def test_field_elements_from_bytes_padding(self):
        """Test that padding works correctly for incomplete chunks"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes
        
        # Data that doesn't divide evenly by chunk size
        data = b"ABC"  # 3 bytes
        chunk_size = 5
        
        elements = field_elements_from_bytes(data, chunk_size=chunk_size)
        assert len(elements) == 1  # Should create one padded chunk
        
        # The element should represent the padded data
        expected_bytes = b"ABC\x00\x00"  # Padded to 5 bytes
        expected_value = int.from_bytes(expected_bytes, "big")
        assert elements[0].value == expected_value
    
    def test_field_elements_to_bytes_basic(self):
        """Test basic conversion from field elements to bytes"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_to_bytes
        
        # Create some field elements
        elements = [FieldElement(0x41), FieldElement(0x42), FieldElement(0x43)]  # 'A', 'B', 'C'
        
        result = field_elements_to_bytes(elements, chunk_size=1)
        assert result == b"ABC"
    
    def test_field_elements_to_bytes_padding_removal(self):
        """Test that trailing zeros are properly removed"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_to_bytes
        
        # Create elements that will have trailing zeros when converted
        elements = [FieldElement(0x4142)]  # Will be padded when converted to bytes
        
        result = field_elements_to_bytes(elements, chunk_size=4)
        # Should remove trailing zeros
        assert not result.endswith(b'\x00')
        assert b'AB' in result or result == b'\x00\x00AB'  # Depending on endianness handling
    
    def test_roundtrip_conversion(self):
        """Test that bytes -> field elements -> bytes roundtrip works"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes, field_elements_to_bytes
        
        # Test with various data types
        test_cases = [
            b"Hello, World!",
            b"",  # Empty bytes
            b"A",  # Single byte
            b"X" * 100,  # Long data
            bytes(range(256)),  # All possible byte values
            b"ZK Proofs are cool! \x00\x01\x02\xff",  # Mixed content with special bytes
        ]
        
        for original_data in test_cases:
            # Convert to field elements and back
            elements = field_elements_from_bytes(original_data)
            recovered_data = field_elements_to_bytes(elements)
            
            # Should recover original data (accounting for padding removal)
            if original_data.endswith(b'\x00'):
                # If original had trailing zeros, they might be stripped
                assert recovered_data == original_data.rstrip(b'\x00')
            else:
                assert recovered_data == original_data
    
    def test_roundtrip_with_different_chunk_sizes(self):
        """Test roundtrip with various chunk sizes"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes, field_elements_to_bytes
        
        original_data = b"The quick brown fox jumps over the lazy dog"
        # Use chunk sizes that are safe for the BN254 field (max 31 bytes to avoid overflow)
        chunk_sizes = [1, 4, 8, 16, 31]
        
        for chunk_size in chunk_sizes:
            elements = field_elements_from_bytes(original_data, chunk_size=chunk_size)
            recovered_data = field_elements_to_bytes(elements, chunk_size=chunk_size)
            
            assert recovered_data == original_data, f"Failed with chunk_size={chunk_size}"
    
    def test_empty_data_handling(self):
        """Test handling of empty data"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes, field_elements_to_bytes
        
        # Empty bytes should return empty list
        elements = field_elements_from_bytes(b"")
        assert elements == []
        
        # Empty list should return empty bytes
        result = field_elements_to_bytes([])
        assert result == b""
    
    def test_large_chunk_size_handling(self):
        """Test with chunk sizes that approach field element capacity"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes, field_elements_to_bytes
        
        # Test with 32-byte chunk size (which can exceed field capacity)
        data = b"A" * 50
        
        # Should handle gracefully even with large chunk size
        elements = field_elements_from_bytes(data, chunk_size=32)  # 32 bytes = 256 bits
        
        for elem in elements:
            # All elements should be within field bounds
            assert 0 <= elem.value < BN254_FIELD_SIZE
        
        # Note: 32-byte chunks may not roundtrip perfectly due to field modular reduction
        # This is expected behavior when chunk values exceed the field modulus
        
    def test_chunk_size_32_modular_reduction(self):
        """Test that 32-byte chunks are properly reduced modulo field size"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes
        
        # Create data that will definitely exceed field size when interpreted as 32-byte integer
        large_data = b'\xff' * 32  # Maximum 32-byte value
        
        elements = field_elements_from_bytes(large_data, chunk_size=32)
        
        # The resulting field element should be reduced
        assert len(elements) == 1
        assert elements[0].value < BN254_FIELD_SIZE
        
        # The original large value should be greater than field size
        original_value = int.from_bytes(large_data, "big")
        assert original_value >= BN254_FIELD_SIZE
        
        # The field element should be the reduced version
        expected_reduced = original_value % BN254_FIELD_SIZE
        assert elements[0].value == expected_reduced
    
    def test_field_element_values_preservation(self):
        """Test that field element values are correctly preserved in conversion"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes, field_elements_to_bytes
        
        # Create known data
        data = b"\x01\x02\x03\x04\x05"
        chunk_size = 2
        
        elements = field_elements_from_bytes(data, chunk_size=chunk_size)
        
        # Check individual element values
        expected_values = [
            int.from_bytes(b"\x01\x02", "big"),  # First chunk
            int.from_bytes(b"\x03\x04", "big"),  # Second chunk  
            int.from_bytes(b"\x05\x00", "big"),  # Third chunk (padded)
        ]
        
        assert len(elements) == len(expected_values)
        for elem, expected in zip(elements, expected_values):
            assert elem.value == expected
    
    def test_max_value_handling(self):
        """Test handling of values near field maximum"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_to_bytes
        
        # Create field element with large value
        large_elem = FieldElement(BN254_FIELD_SIZE - 1)
        elements = [large_elem]
        
        # Should convert without error
        result = field_elements_to_bytes(elements, chunk_size=32)
        assert isinstance(result, bytes)
        assert len(result) <= 32  # Should fit in specified chunk size
    
    def test_consistency_with_existing_methods(self):
        """Test that new functions are consistent with existing FieldElement methods"""
        from django_zk_auth.crypto.field_arithmetic import field_elements_from_bytes, field_elements_to_bytes
        
        # Test with single field element
        original_elem = FieldElement(0x123456)
        
        # Convert using new batch method
        batch_bytes = field_elements_to_bytes([original_elem], chunk_size=4)
        
        # Convert using existing method
        individual_bytes = original_elem.to_bytes(4)
        
        # Should produce same result (accounting for padding removal)
        assert batch_bytes.ljust(4, b'\x00') == individual_bytes or batch_bytes == individual_bytes.rstrip(b'\x00')

if __name__ == "__main__":
    pytest.main([__file__])