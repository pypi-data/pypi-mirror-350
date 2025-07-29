"""
Contacted Python SDK - Basic Usage Examples
"""

import os
from contacted import ContactedAI


def basic_example():
    """Basic usage example"""
    # Initialize the client
    contacted = ContactedAI(
        api_key=os.getenv('CONTACTED_API_KEY', 'your-api-key-here')
    )

    try:
        # Send a message (your exact API!)
        result = contacted.send({
            'from': 'sender@example.com',
            'to': 'receiver@example.com',
            'prompt': 'Generate a personalized welcome email for the user',  # 10+ chars
            'data': {
                'name': 'John Doe',
                'plan': 'premium',
                'link': 'https://dashboard.example.com'
            }
        })

        print('Message sent successfully:', result)

    except ValueError as error:
        print('Error:', error)


def validation_examples():
    """Examples showing validation errors"""
    contacted = ContactedAI(api_key="test-key")

    # These will throw validation errors BEFORE hitting your API:

    print("Testing validation errors...")

    try:
        contacted.send({
            'from': 'invalid-email',
            'to': 'user@example.com',
            'prompt': 'Generate email'
        })
    except ValueError as error:
        print('❌ Email validation:', error)
        # "Invalid 'from' email address format"

    try:
        contacted.send({
            'from': 'sender@example.com',
            'to': 'receiver@example.com',
            'prompt': 'short'  # Less than 10 characters
        })
    except ValueError as error:
        print('❌ Prompt validation:', error)
        # "Prompt must be at least 10 characters long"

    try:
        contacted.send({
            'from': 'sender@example.com',
            'to': 'receiver@example.com',
            'prompt': 'This is a valid prompt with enough characters',
            'data': {
                'key with space': 'invalid key'  # Keys can't have spaces
            }
        })
    except ValueError as error:
        print('❌ Data validation:', error)
        # "Data keys cannot contain spaces"

    print('✅ All validation examples completed')


def advanced_example():
    """Advanced usage with error handling"""
    contacted = ContactedAI(
        api_key=os.getenv('CONTACTED_API_KEY'),
        timeout=60  # Custom timeout
    )

    # Example with comprehensive error handling
    try:
        result = contacted.send({
            'from': 'automated@mycompany.com',
            'to': 'customer@example.com',
            'prompt': 'Create a personalized onboarding email with account details',
            'data': {
                'firstName': 'Sarah',
                'lastName': 'Johnson',
                'accountType': 'business',
                'trialDays': 14,
                'loginUrl': 'https://app.mycompany.com/login'
            }
        })

        print(f"✅ Email queued successfully!")
        print(f"   ID: {result.get('id')}")
        print(f"   Status: {result.get('status')}")

    except ValueError as e:
        error_msg = str(e)
        if 'Invalid' in error_msg:
            print(f"❌ Validation Error: {error_msg}")
        elif 'API Error' in error_msg:
            print(f"❌ API Error: {error_msg}")
        else:
            print(f"❌ Network Error: {error_msg}")


if __name__ == '__main__':
    print("=== ContactedAI Python SDK Examples ===\n")

    print("1. Basic Example:")
    basic_example()

    print("\n2. Validation Examples:")
    validation_examples()

    print("\n3. Advanced Example:")
    advanced_example()