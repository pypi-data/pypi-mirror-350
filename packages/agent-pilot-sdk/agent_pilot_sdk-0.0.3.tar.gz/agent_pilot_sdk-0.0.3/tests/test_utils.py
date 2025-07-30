import uuid

from agent_pilot.utils import clean_nones, create_uuid_from_string


class TestCleanNones:
    def test_clean_nones_list(self):
        """Test clean_nones with a list containing None values."""
        input_list = [1, None, 2, None, 3]
        expected = [1, 2, 3]

        result = clean_nones(input_list)
        assert result == expected

    def test_clean_nones_dict(self):
        """Test clean_nones with a dictionary containing None values."""
        input_dict = {'a': 1, 'b': None, 'c': 3}
        expected = {'a': 1, 'c': 3}

        result = clean_nones(input_dict)
        assert result == expected

    def test_clean_nones_nested(self):
        """Test clean_nones with nested structures containing None values."""
        input_nested = {'a': 1, 'b': None, 'c': [1, None, 2], 'd': {'x': 1, 'y': None, 'z': [None, 3, None]}}

        expected = {'a': 1, 'c': [1, 2], 'd': {'x': 1, 'z': [3]}}

        result = clean_nones(input_nested)
        assert result == expected

    def test_clean_nones_non_dict_list(self):
        """Test clean_nones with non-dict and non-list values."""
        primitives = ['string', 123, True, False, 1.23]

        for primitive in primitives:
            result = clean_nones(primitive)
            assert result == primitive

    def test_clean_nones_all_nones(self):
        """Test clean_nones with structures full of None values."""
        input_list = [None, None, None]
        input_dict = {'a': None, 'b': None}

        assert clean_nones(input_list) == []
        assert clean_nones(input_dict) == {}

    def test_clean_nones_empty(self):
        """Test clean_nones with empty structures."""
        assert clean_nones([]) == []
        assert clean_nones({}) == {}

    def test_clean_nones_exception_handling(self):
        """Test clean_nones handles exceptions gracefully."""

        # Create an object that raises an exception when accessed
        class ExceptionRaiser:
            def __getitem__(self, key):
                raise Exception('Test exception')

        exception_raiser = ExceptionRaiser()

        # Should return the original object when exception occurs
        result = clean_nones(exception_raiser)
        assert result is exception_raiser


class TestCreateUuidFromString:
    def test_create_uuid_from_string_basic(self):
        """Test the basic functionality of create_uuid_from_string."""
        test_string = 'test_string'
        result = create_uuid_from_string(test_string)

        # Verify result is a UUID
        assert isinstance(result, uuid.UUID)

    def test_create_uuid_from_string_deterministic(self):
        """Test that create_uuid_from_string is deterministic for the same input."""
        test_string = 'deterministic_test'

        result1 = create_uuid_from_string(test_string)
        result2 = create_uuid_from_string(test_string)

        # Same input should produce same UUID
        assert result1 == result2

    def test_create_uuid_from_string_different_inputs(self):
        """Test that different inputs produce different UUIDs."""
        result1 = create_uuid_from_string('input1')
        result2 = create_uuid_from_string('input2')

        # Different inputs should produce different UUIDs
        assert result1 != result2

    def test_create_uuid_from_string_empty(self):
        """Test with empty string input."""
        result = create_uuid_from_string('')

        # Should still return a valid UUID
        assert isinstance(result, uuid.UUID)

    def test_create_uuid_from_string_unicode(self):
        """Test with Unicode characters in input."""
        result = create_uuid_from_string('Unicode 유니코드 测试')

        # Should handle Unicode correctly
        assert isinstance(result, uuid.UUID)

    def test_create_uuid_from_string_long_input(self):
        """Test with a very long input string."""
        long_string = 'x' * 10000
        result = create_uuid_from_string(long_string)

        # Should handle long strings
        assert isinstance(result, uuid.UUID)
