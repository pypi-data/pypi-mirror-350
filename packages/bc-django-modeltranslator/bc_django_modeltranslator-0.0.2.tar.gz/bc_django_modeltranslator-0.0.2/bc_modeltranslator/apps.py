from django.apps import AppConfig

class BcModeltranslaterConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'bc_modeltranslator'

	verbose_name = "Bibizyanki core modeltranslator"

	def ready(self) -> None:
		from .models import handle_translation_registrations

		handle_translation_registrations()