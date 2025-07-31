import re

with open('SamsTech/settings.py', 'r') as f:
    content = f.read()

# Fix the email configuration
email_config = '''
# Email Configuration - Conditional based on environment
if 'DEVELOPMENT' in os.environ:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = 'samtech10101010@gmail.com'
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
'''

# Replace the email configuration section
pattern = r'# Email Configuration.*?ACCOUNT_EMAIL_VERIFICATION = "none"'
content = re.sub(pattern, email_config.strip(), content, flags=re.DOTALL)

with open('SamsTech/settings.py', 'w') as f:
    f.write(content)
