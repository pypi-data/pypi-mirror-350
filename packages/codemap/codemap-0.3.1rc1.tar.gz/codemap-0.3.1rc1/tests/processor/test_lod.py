"""Test LOD (Level of Detail) functionality."""

from pathlib import Path

import pytest

from codemap.processor.lod import LODGenerator, LODLevel
from codemap.processor.tree_sitter.base import EntityType


@pytest.fixture
def sample_py_file(tmp_path: Path) -> Path:
	"""Create a sample Python file for testing."""
	sample_code = """
'''Module level docstring.'''

import os
import sys
from typing import List, Dict

class SampleClass:
    '''A sample class for testing.'''

    def __init__(self, name: str):
        '''Initialize the class.

        Args:
            name: Name of the sample
        '''
        self.name = name

    def get_name(self) -> str:
        '''Get the name of the sample.'''
        return self.name


def sample_function(a: int, b: int) -> int:
    '''Calculate the sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    '''
    return a + b

# A constant
CONSTANT_VALUE = 42
"""
	file_path = tmp_path / "sample.py"
	with file_path.open("w") as f:
		f.write(sample_code)
	return file_path


def test_lod_generator(sample_py_file: Path) -> None:
	"""Test that LODGenerator can process a file at different levels."""
	generator = LODGenerator()

	# Test LOD level 1 (names/signatures)
	entity_l1 = generator.generate_lod(sample_py_file, LODLevel.SIGNATURES)
	assert entity_l1 is not None
	assert entity_l1.entity_type == EntityType.MODULE
	assert len(entity_l1.children) > 0

	# Find class
	class_entity = None
	for child in entity_l1.children:
		if child.entity_type == EntityType.CLASS and child.name == "SampleClass":
			class_entity = child
			break

	assert class_entity is not None
	assert class_entity.docstring == ""  # Empty at level 1

	# Test LOD level 2 (with docstrings)
	entity_l2 = generator.generate_lod(sample_py_file, LODLevel.DOCS)
	assert entity_l2 is not None

	# Find class again
	class_entity_l2 = None
	for child in entity_l2.children:
		if child.entity_type == EntityType.CLASS and child.name == "SampleClass":
			class_entity_l2 = child
			break

	assert class_entity_l2 is not None
	assert "sample class for testing" in class_entity_l2.docstring.lower()

	# Find function
	function_entity = None
	for child in entity_l2.children:
		if child.entity_type == EntityType.FUNCTION and child.name == "sample_function":
			function_entity = child
			break

	assert function_entity is not None
	assert "sum of two numbers" in function_entity.docstring.lower()

	# Test LOD level 3 (with signatures)
	entity_l3 = generator.generate_lod(sample_py_file, LODLevel.SIGNATURES)
	assert entity_l3 is not None

	# Find function again
	function_entity_l3 = None
	for child in entity_l3.children:
		if child.entity_type == EntityType.FUNCTION and child.name == "sample_function":
			function_entity_l3 = child
			break

	assert function_entity_l3 is not None
	assert "a: int, b: int" in function_entity_l3.signature
	assert "-> int" in function_entity_l3.signature

	# Test LOD level 4 (full content)
	entity_l4 = generator.generate_lod(sample_py_file, LODLevel.FULL)
	assert entity_l4 is not None

	# Find function again
	function_entity_l4 = None
	for child in entity_l4.children:
		if child.entity_type == EntityType.FUNCTION and child.name == "sample_function":
			function_entity_l4 = child
			break

	assert function_entity_l4 is not None
	assert "return a + b" in function_entity_l4.content


if __name__ == "__main__":
	# Create a temporary directory
	import tempfile

	with tempfile.TemporaryDirectory() as tmp_dir:
		tmp_path = Path(tmp_dir)
		# Create a sample file
		file_path = sample_py_file(tmp_path)

		# Run tests
		test_lod_generator(file_path)
