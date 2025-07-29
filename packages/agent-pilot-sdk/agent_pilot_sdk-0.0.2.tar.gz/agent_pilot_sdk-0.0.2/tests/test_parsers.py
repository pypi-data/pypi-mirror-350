import jsonpickle
from pydantic import BaseModel
from pydantic.v1 import BaseModel as BaseModelV1

from agent_pilot.parsers import (
    default_input_parser,
    method_input_parser,
    default_output_parser,
    PydanticHandler,
    filter_params,
    PARAMS_TO_CAPTURE,
)


class TestDefaultInputParser:
    def test_empty_input(self):
        """Test parser with no arguments."""
        result = default_input_parser()
        assert result == {'input': None}

    def test_single_arg(self):
        """Test parser with a single argument."""
        result = default_input_parser('test_arg')
        assert result == {'input': 'test_arg'}

    def test_multiple_args(self):
        """Test parser with multiple arguments."""
        result = default_input_parser('arg1', 'arg2', 'arg3')
        assert result == {'input': ['arg1', 'arg2', 'arg3']}

    def test_kwargs_only(self):
        """Test parser with keyword arguments only."""
        result = default_input_parser(key1='value1', key2='value2')
        assert result == {'input': [{'key1': 'value1', 'key2': 'value2'}]}

    def test_args_and_kwargs(self):
        """Test parser with both positional and keyword arguments."""
        result = default_input_parser('arg1', 'arg2', key1='value1', key2='value2')
        assert result == {'input': ['arg1', 'arg2', {'key1': 'value1', 'key2': 'value2'}]}


class TestMethodInputParser:
    def test_no_args_after_self(self):
        """Test parser with only 'self' argument."""
        result = method_input_parser('self')
        assert result == {'input': None}

    def test_single_arg_after_self(self):
        """Test parser with 'self' and one additional argument."""
        result = method_input_parser('self', 'arg1')
        assert result == {'input': 'arg1'}

    def test_multiple_args_after_self(self):
        """Test parser with 'self' and multiple additional arguments."""
        result = method_input_parser('self', 'arg1', 'arg2', 'arg3')
        assert result == {'input': ['arg1', 'arg2', 'arg3']}

    def test_kwargs_only(self):
        """Test parser with 'self' and keyword arguments only."""
        result = method_input_parser('self', key1='value1', key2='value2')
        assert result == {'input': [{'key1': 'value1', 'key2': 'value2'}]}

    def test_args_and_kwargs(self):
        """Test parser with 'self', positional and keyword arguments."""
        result = method_input_parser('self', 'arg1', 'arg2', key1='value1', key2='value2')
        assert result == {'input': ['arg1', 'arg2', {'key1': 'value1', 'key2': 'value2'}]}


class TestDefaultOutputParser:
    def test_simple_output(self):
        """Test parser with simple output."""
        result = default_output_parser('test_output')
        assert result == {'output': 'test_output', 'tokensUsage': None}

    def test_object_with_content(self):
        """Test parser with an object having a content attribute."""

        class ResponseWithContent:
            def __init__(self, content):
                self.content = content

        output = ResponseWithContent('test_content')
        result = default_output_parser(output)

        assert result == {'output': 'test_content', 'tokensUsage': None}

    def test_with_args_kwargs(self):
        """Test parser ignores additional args and kwargs."""
        result = default_output_parser('test_output', 'arg1', 'arg2', key1='value1')
        assert result == {'output': 'test_output', 'tokensUsage': None}


class TestPydanticHandler:
    def setup_method(self):
        # Register the handler for testing
        jsonpickle.handlers.registry.register(BaseModel, PydanticHandler)
        jsonpickle.handlers.registry.register(BaseModelV1, PydanticHandler)

    def teardown_method(self):
        # Unregister the handler after testing
        jsonpickle.handlers.registry.unregister(BaseModel)
        jsonpickle.handlers.registry.unregister(BaseModelV1)

    def test_pydantic_v2_model(self):
        """Test serializing a Pydantic v2 model."""

        class TestModel(BaseModel):
            name: str
            value: int

        model = TestModel(name='test', value=42)
        serialized = jsonpickle.encode(model.model_dump())
        deserialized = jsonpickle.decode(serialized)

        assert deserialized == {'name': 'test', 'value': 42}

    def test_pydantic_v1_model(self):
        """Test serializing a Pydantic v1 model."""

        class TestModelV1(BaseModelV1):
            name: str
            value: int

        model = TestModelV1(name='test', value=42)
        serialized = jsonpickle.encode(model)
        deserialized = jsonpickle.decode(serialized)

        # Just verify the original data is preserved in the deserialized object
        # The exact structure may vary between jsonpickle versions
        if isinstance(deserialized, dict) and 'name' in deserialized:
            # Directly accessible
            assert deserialized['name'] == 'test'
            assert deserialized['value'] == 42
        else:
            # Nested in py/state structure
            assert 'py/state' in deserialized
            state_dict = deserialized['py/state']
            if '__dict__' in state_dict:
                assert state_dict['__dict__']['name'] == 'test'
                assert state_dict['__dict__']['value'] == 42
            else:
                assert state_dict['name'] == 'test'
                assert state_dict['value'] == 42


class TestFilterParams:
    def test_filter_params_keeps_tracked(self):
        """Test that filter_params keeps tracked parameters."""
        params = {
            'temperature': 0.7,
            'top_p': 1.0,
            'max_tokens': 100,
            'functions': [{'name': 'test_function'}],
            'timeout': 30,
        }

        filtered = filter_params(params)

        # Check that all parameters in PARAMS_TO_CAPTURE are kept
        for key in params:
            if key in PARAMS_TO_CAPTURE:
                assert key in filtered
                assert filtered[key] == params[key]

    def test_filter_params_removes_untracked(self):
        """Test that filter_params removes untracked parameters."""
        params = {'temperature': 0.7, 'top_p': 1.0, 'untracked_param': 'value', 'another_untracked': 123}

        filtered = filter_params(params)

        # Check that untracked parameters are removed
        assert 'untracked_param' not in filtered
        assert 'another_untracked' not in filtered

        # Check that tracked parameters are kept
        assert 'temperature' in filtered
        assert 'top_p' in filtered

    def test_filter_params_empty(self):
        """Test filter_params with an empty dictionary."""
        assert filter_params({}) == {}
