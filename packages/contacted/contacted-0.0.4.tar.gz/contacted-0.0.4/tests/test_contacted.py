"""
Tests for Contacted Python SDK
"""

import pytest
from contacted import ContactedAI
from contacted.validation import (
    validate_send_options,
    validate_prompt,
    validate_data,
    validate_emails,
    is_valid_email
)


class TestEmailValidation:
    """Test email validation functions"""

    def test_should_validate_correct_email_formats(self):
        """Test valid email formats"""
        assert is_valid_email('test@example.com') == True
        assert is_valid_email('user.name@domain.co.uk') == True
        assert is_valid_email('test+label@example.org') == True
        assert is_valid_email('user123@test-domain.com') == True
        assert is_valid_email('valid.email@example123.co') == True

    def test_should_reject_invalid_email_formats(self):
        """Test invalid email formats"""
        assert is_valid_email('invalid-email') == False
        assert is_valid_email('test@') == False
        assert is_valid_email('@example.com') == False
        assert is_valid_email('test..test@example.com') == False  # consecutive dots
        assert is_valid_email('test@example') == False  # no TLD
        assert is_valid_email('.test@example.com') == False  # leading dot
        assert is_valid_email('test.@example.com') == False  # trailing dot
        assert is_valid_email('test@.example.com') == False  # dot after @
        assert is_valid_email('test@example.com.') == False  # trailing dot
        assert is_valid_email('') == False  # empty string
        assert is_valid_email('test @example.com') == False  # space in email

    def test_should_validate_required_email_fields(self):
        """Test required email validation"""
        with pytest.raises(ValueError, match='Both "from" and "to" email addresses are required'):
            validate_emails('', 'test@example.com')

        with pytest.raises(ValueError, match='Both "from" and "to" email addresses are required'):
            validate_emails('test@example.com', '')

    def test_should_validate_email_format_in_validate_emails(self):
        """Test email format validation in validate_emails function"""
        with pytest.raises(ValueError, match='Invalid "from" email address format'):
            validate_emails('invalid-email', 'test@example.com')

        with pytest.raises(ValueError, match='Invalid "to" email address format'):
            validate_emails('test@example.com', 'invalid-email')


class TestPromptValidation:
    """Test prompt validation functions"""

    def test_should_validate_prompt_is_required(self):
        """Test prompt is required"""
        with pytest.raises(ValueError, match='Prompt is required'):
            validate_prompt(None)

    def test_should_validate_prompt_is_string(self):
        """Test prompt must be string"""
        with pytest.raises(ValueError, match='Prompt must be a string'):
            validate_prompt(123)

        with pytest.raises(ValueError, match='Prompt must be a string'):
            validate_prompt({})

    def test_should_validate_prompt_length(self):
        """Test prompt length validation"""
        with pytest.raises(ValueError, match='Prompt must be at least 10 characters long'):
            validate_prompt('short')

        long_prompt = 'a' * 251
        with pytest.raises(ValueError, match='Prompt must be no more than 250 characters long'):
            validate_prompt(long_prompt)

    def test_should_accept_valid_prompts(self):
        """Test valid prompts are accepted"""
        # This should not raise any exception
        validate_prompt('This is a valid prompt with enough characters')


class TestDataValidation:
    """Test data validation functions"""

    def test_should_allow_optional_data(self):
        """Test data is optional"""
        # These should not raise exceptions
        validate_data(None)

    def test_should_validate_data_is_dict(self):
        """Test data must be dictionary"""
        with pytest.raises(ValueError, match='Data must be an object'):
            validate_data('string')

        with pytest.raises(ValueError, match='Data must be an object'):
            validate_data([])

        with pytest.raises(ValueError, match='Data must be an object'):
            validate_data(123)

    def test_should_validate_data_keys_are_strings(self):
        """Test data keys must be strings"""
        with pytest.raises(ValueError, match='All data keys must be non-empty strings'):
            validate_data({'': 'value'})

        with pytest.raises(ValueError, match='All data keys must be non-empty strings'):
            validate_data({'   ': 'value'})

    def test_should_validate_data_keys_have_no_spaces(self):
        """Test data keys cannot have spaces"""
        with pytest.raises(ValueError, match='Data keys cannot contain spaces'):
            validate_data({'key with space': 'value'})

        with pytest.raises(ValueError, match='Data keys cannot contain spaces'):
            validate_data({'key\twith\ttab': 'value'})

    def test_should_accept_valid_data_objects(self):
        """Test valid data objects are accepted"""
        # This should not raise any exception
        validate_data({
            'name': 'John Doe',
            'age': 30,
            'active': True,
            'link': 'https://example.com'
        })


class TestCompleteSendOptionsValidation:
    """Test complete send options validation"""

    def setUp(self):
        self.valid_options = {
            'from': 'sender@example.com',
            'to': 'receiver@example.com',
            'prompt': 'This is a valid prompt with enough characters',
            'data': {
                'name': 'John',
                'link': 'https://example.com'
            }
        }

    def test_should_validate_complete_valid_options(self):
        """Test complete valid options"""
        valid_options = {
            'from': 'sender@example.com',
            'to': 'receiver@example.com',
            'prompt': 'This is a valid prompt with enough characters',
            'data': {
                'name': 'John',
                'link': 'https://example.com'
            }
        }
        # This should not raise any exception
        validate_send_options(valid_options)

    def test_should_fail_on_invalid_email(self):
        """Test invalid email validation"""
        options = {
            'from': 'invalid-email',
            'to': 'receiver@example.com',
            'prompt': 'This is a valid prompt with enough characters'
        }
        with pytest.raises(ValueError, match='Invalid "from" email address format'):
            validate_send_options(options)

    def test_should_fail_on_invalid_prompt(self):
        """Test invalid prompt validation"""
        options = {
            'from': 'sender@example.com',
            'to': 'receiver@example.com',
            'prompt': 'short'
        }
        with pytest.raises(ValueError, match='Prompt must be at least 10 characters long'):
            validate_send_options(options)

    def test_should_fail_on_invalid_data(self):
        """Test invalid data validation"""
        options = {
            'from': 'sender@example.com',
            'to': 'receiver@example.com',
            'prompt': 'This is a valid prompt with enough characters',
            'data': {'key with space': 'value'}
        }
        with pytest.raises(ValueError, match='Data keys cannot contain spaces'):
            validate_send_options(options)

    def test_should_work_without_data_field(self):
        """Test options work without data field"""
        options = {
            'from': 'sender@example.com',
            'to': 'receiver@example.com',
            'prompt': 'This is a valid prompt with enough characters'
        }
        # This should not raise any exception
        validate_send_options(options)


class TestContactedAIClient:
    """Test ContactedAI client class"""

    def test_should_initialize_with_api_key(self):
        """Test client initialization"""
        client = ContactedAI(api_key='test-api-key')
        assert client.api_key == 'test-api-key'

    def test_should_throw_error_without_api_key(self):
        """Test client requires API key"""
        with pytest.raises(ValueError, match='API key is required'):
            ContactedAI(api_key='')

        with pytest.raises(ValueError, match='API key is required'):
            ContactedAI(api_key=None)