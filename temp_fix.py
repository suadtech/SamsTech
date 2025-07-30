import re

# Read the settings file
with open('SamsTech/settings.py', 'r') as f:
    content = f.read()

# Force console backend and mandatory verification
content = re.sub(r'EMAIL_BACKEND = [^\n]+', 'EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"', content)
content = re.sub(r'ACCOUNT_EMAIL_VERIFICATION = [^\n]+', 'ACCOUNT_EMAIL_VERIFICATION = "mandatory"', content)

# Write back
with open('SamsTech/settings.py', 'w') as f:
    f.write(content)
