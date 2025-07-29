import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

ENABLE_REGISTRATIONS: bool = getattr(
	settings, "MODELTRANSLATION_ENABLE_REGISTRATIONS", settings.USE_I18N
)

TRANS_FILENAME: str = getattr(
	settings, "TRANS_FILENAME", "translation"
)

if os.path.splitext(TRANS_FILENAME)[1]:
	raise ImproperlyConfigured(
		f"TRANS_FILENAME should be specified without file extension, e.g., 'translation', not '{TRANS_FILENAME}'"
	)