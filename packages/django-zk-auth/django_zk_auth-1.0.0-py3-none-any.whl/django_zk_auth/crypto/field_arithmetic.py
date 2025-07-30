"""Finite field arithmetic for ZK proofs"""
import galois
from typing import Union, List
from functools import lru_cache


# BN254 curve field (commonly used in ZK systems)
BN254_FIELD_SIZE = 21888242871839275222246405745257275088548364400416034343698204186575808495617

_FIELD_INSTANCE = None

def get_field() -> galois.GF:
    """Lazy load the Galois field only when first needed"""
    global _FIELD_INSTANCE
    if _FIELD_INSTANCE is None:
        _FIELD_INSTANCE = galois.GF(BN254_FIELD_SIZE)
    return _FIELD_INSTANCE


class FieldElement:
    """Wrapper for finite field elements with type safety and convenience"""
    
    def __init__(self, value: Union[int, str, bytes]):
        self._field = get_field()
        if isinstance(value, str):
            if value.startswith("0x"):
                value = int(value, 16)
            else:
                value = int(value)
        elif isinstance(value, bytes):
            value = int.from_bytes(value, "big")
        elif isinstance(value, int):
            pass
        else:
            raise TypeError(f"Unsupported type for FieldElement: {type(value)}")
        
        self._value = self._field(value % BN254_FIELD_SIZE)
    
    def _is_valid(self) -> bool:
        return 0 <= self.value < BN254_FIELD_SIZE
    
    @property
    def value(self) -> int:
        """Get the integer value"""
        return int(self._value)
    
    def __add__(self, other: 'FieldElement') -> 'FieldElement':
        """Addition in the finite field"""
        if isinstance(other, FieldElement):
            result = self._value + other._value
        else:
            result = self._value + self._field(other)
        return FieldElement(int(result))
    
    def __sub__(self, other: 'FieldElement') -> 'FieldElement':
        """Subtraction in the finite field"""
        if isinstance(other, FieldElement):
            result = self._value - other._value
        else:
            result = self._value - self._field(other)
        return FieldElement(int(result))
    
    def __mul__(self, other: 'FieldElement') -> 'FieldElement':
        """Multiplication in the finite field"""
        if isinstance(other, FieldElement):
            result = self._value * other._value
        else:
            result = self._value * self._field(other)
        return FieldElement(int(result))
    
    def __truediv__(self, other: 'FieldElement') -> 'FieldElement':
        """Division in the finite field (multiplication by inverse)"""
        if isinstance(other, FieldElement):
            result = self._value / other._value
        else:
            result = self._value / self._field(other)
        return FieldElement(int(result))
    
    def __pow__(self, exponent: int) -> 'FieldElement':
        """Exponentiation in the finite field"""
        result = self._value ** exponent
        return FieldElement(int(result))
    
    def __neg__(self) -> 'FieldElement':
        """Negation in the finite field"""
        return FieldElement(int(-self._value))
    
    def __eq__(self, other) -> bool:
        """Equality comparison"""
        if isinstance(other, FieldElement):
            return self._value == other._value
        elif isinstance(other, (int, str, bytes)):
            return self._value == self._field(other)
        return False
    
    def __repr__(self) -> str:
        """String representation"""
        return f"FieldElement({self.value})"
    
    def __str__(self) -> str:
        """String representation"""
        return str(self.value)
    
    def __hash__(self) -> int:
        """Hash function for use in sets/dicts"""
        return hash(self.value)
    
    def inverse(self) -> 'FieldElement':
        """Multiplicative inverse in the finite field"""
        result = self._value ** -1
        return FieldElement(int(result))
    
    def is_zero(self) -> bool:
        """Check if element is zero"""
        return self.value == 0
    
    def to_bytes(self, length: int = 32, byteorder: str = 'big') -> bytes:
        """Convert to bytes representation"""
        return self.value.to_bytes(length, byteorder)
    
    def to_hex(self) -> str:
        """Convert to hexadecimal string"""
        return hex(self.value)

# Utility functions for common operations
def batch_multiply(elements: List[FieldElement]) -> FieldElement:
    """Multiply a list of field elements"""
    result = FieldElement(1)
    for elem in elements:
        result = result * elem
    return result

def batch_add(elements: List[FieldElement]) -> FieldElement:
    """Add a list of field elements"""
    result = FieldElement(0)
    for elem in elements:
        result = result + elem
    return result

def polynomial_evaluate(coefficients: List[FieldElement], x: FieldElement) -> FieldElement:
    """Evaluate polynomial at point x using Horner's method"""
    if not coefficients:
        return FieldElement(0)
    
    result = coefficients[-1]  # Start with highest degree coefficient
    for i in range(len(coefficients) - 2, -1, -1):
        result = result * x + coefficients[i]
    return result

def lagrange_interpolation(points: List[tuple], x: FieldElement) -> FieldElement:
    """
    Lagrange interpolation for points [(x0, y0), (x1, y1), ...]
    Returns the polynomial value at point x
    """
    if not points:
        return FieldElement(0)
    
    result = FieldElement(0)
    n = len(points)
    
    for i in range(n):
        xi, yi = points[i]
        xi = FieldElement(xi) if not isinstance(xi, FieldElement) else xi
        yi = FieldElement(yi) if not isinstance(yi, FieldElement) else yi
        
        # Calculate Lagrange basis polynomial L_i(x)
        numerator = FieldElement(1)
        denominator = FieldElement(1)
        
        for j in range(n):
            if i != j:
                xj = FieldElement(points[j][0]) if not isinstance(points[j][0], FieldElement) else points[j][0]
                numerator = numerator * (x - xj)
                denominator = denominator * (xi - xj)
        
        # Add y_i * L_i(x) to result
        basis = numerator / denominator
        result = result + yi * basis
    
    return result

# Random field element generation (for testing/simulation)
def random_field_element() -> FieldElement:
    """Generate a random field element (requires random module)"""
    import random
    return FieldElement(random.randint(0, BN254_FIELD_SIZE - 1))

# Zero and One constants
ZERO = FieldElement(0)
ONE = FieldElement(1)


def field_elements_from_bytes(data: bytes, chunk_size: int = 31) -> List[FieldElement]:
    """Convert bytes to list of field elements"""
    elements = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        if len(chunk) < chunk_size:
            chunk = chunk + b'\x00' * (chunk_size - len(chunk))
        elements.append(FieldElement(int.from_bytes(chunk, "big")))
    return elements


def field_elements_to_bytes(elements: List[FieldElement], chunk_size: int = 31) -> bytes:
    """Convert list of field elements to bytes"""
    result = b""
    for element in elements:
        result += element.to_bytes(chunk_size)
    return result.rstrip(b'\x00')  # Remove padding
