# ir
amazon_sender.py

To install:	```pip install ir```

## Overview
The `ir` package provides a Python helper class named `AmazonSender` for sending emails using Amazon's Simple Email Service (SES) through the `boto` library. This class handles encodings properly and supports sending both text and HTML emails. It is designed to be flexible, allowing users to specify various email parameters such as sender, recipient, and message content.

## Features
- **Email Encoding**: Proper handling of different encodings ensuring that text and HTML emails are correctly displayed.
- **Multiple Recipients**: Ability to send emails to multiple recipients.
- **HTML and Text Emails**: Support for both HTML and plain text parts in emails.
- **Customizable Sender and Reply-To**: Custom sender and reply-to addresses can be specified.
- **AWS Credentials Management**: Automatic fetching of AWS credentials from environment variables if not provided.

## Installation
To install the package, use the following pip command:
```bash
pip install ir
```

## Usage

### Initializing the AmazonSender
You can initialize the `AmazonSender` object by providing AWS credentials directly or letting the class fetch them from environment variables:
```python
from ir import AmazonSender

# Initialize with direct credentials
amazon_sender = AmazonSender(aws_key='your_aws_access_key', aws_secret='your_aws_secret_key')

# Initialize with environment variables
amazon_sender = AmazonSender()
```

### Sending an Email
To send an email, you can use the `send_email` method. This method allows you to specify the sender, recipient, subject, and body of the email in both text and HTML formats:
```python
response = amazon_sender.send_email(
    sender='Me <me@example.com>',
    to_addresses=['recipient1@example.com', 'recipient2@example.com'],
    subject='Greetings',
    text='Hello, this is a plain text message.',
    html='<h1>Hello</h1><p>This is an HTML message.</p>'
)
```

### Verifying an Email Address
Before sending an email, you might want to verify the email address using Amazon SES:
```python
verification_status = amazon_sender.verify_email('test@example.com')
```

## Class and Method Documentation

### `class AmazonSender`
A class to send emails using Amazon SES.

#### `__init__(self, to_addresses=None, sender=None, aws_key=None, aws_secret=None)`
Constructor to initialize the AmazonSender with optional AWS credentials, sender, and recipient addresses.

- **Parameters**:
  - `to_addresses`: The default recipient address(es). Can be a string or a list of strings.
  - `sender`: The default sender email address.
  - `aws_key`: AWS access key.
  - `aws_secret`: AWS secret key.

#### `send_email(self, subject='', text='', html=None, reply_addresses=None, sender_ascii=None)`
Sends an email with the specified subject, text, and/or HTML content.

- **Parameters**:
  - `subject`: Subject of the email.
  - `text`: Plain text content of the email.
  - `html`: HTML content of the email.
  - `reply_addresses`: Email address(es) to which replies should be sent.
  - `sender_ascii`: ASCII representation of the sender's email address, used in the email header.

#### `verify_email(self, email)`
Requests Amazon SES to verify an email address.

- **Parameters**:
  - `email`: The email address to verify.

#### `get_client(self)`
Initializes or retrieves the SESConnection client.

## License
This project is licensed under the BSD license.