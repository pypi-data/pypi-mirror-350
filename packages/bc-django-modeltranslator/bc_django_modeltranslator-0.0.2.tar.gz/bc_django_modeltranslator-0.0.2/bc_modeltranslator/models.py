import os
from typing import Any
from pathlib import Path
from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.utils.module_loading import module_has_submodule 

def autodiscover() -> None:
	from .settings import TRANS_FILENAME

	for app_config in apps.get_app_configs():
		trans_file = Path(app_config.path) / "{0}{1}".format(TRANS_FILENAME, ".py")

		if not trans_file.is_file():
			continue

		module_name = "{0}.{1}".format(app_config.name, TRANS_FILENAME)

		try:
			import_module(module_name)
		
		except ImportError as e:
			# If the module physically exists, but the error still exists, we raise it
			if module_has_submodule(app_config.module, TRANS_FILENAME):
				raise

			# If DEBUG — we log, but don’t crash
			if settings.DEBUG:
				print(f"[autodiscover] translation.py для '{app_config.name}' найден, "
					f"но не удалось импортировать: {e}")

	if settings.DEBUG:
		print(f"[autodiscover] All available translation.py loaded. [pid: {os.getpid()}]")


def handle_translation_registrations(*args: Any, **kwargs: Any) -> None:
	from .settings import ENABLE_REGISTRATIONS
	
	if not ENABLE_REGISTRATIONS:
		# If the user really wants to disable this, they can, possibly at their
		# own expense. This is generally only required in cases where other
		# apps generate import errors and requires extra work on the user's
		# part to make things work.
		return

	# Trigger autodiscover, causing any TranslationOption initialization
	# code to execute.
	autodiscover()