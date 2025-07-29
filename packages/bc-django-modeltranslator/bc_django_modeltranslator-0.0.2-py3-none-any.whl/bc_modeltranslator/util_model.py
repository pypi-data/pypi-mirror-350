from typing import Any, List

from django.utils.translation import get_language, activate
from django.conf import settings

def get_field(self, field_name):
	try:
		return type(self).get_field(self, field_name)
	
	except Exception:
		localized_name = f"{field_name}_{get_language()}"
		try:
			return type(self).get_field(self, localized_name)
		except Exception:
			raise


class BcTransModel:
	LANGS_LIST: List[str] = [lang[0] for lang in settings.LANGUAGES]
	
	def __getattribute__(self, attr_name: str) -> Any:
		try:
			obj_dict = super().__getattribute__('__dict__')
			localized_name = f"{attr_name}_{get_language()}"
			
			if localized_name in obj_dict:
				return obj_dict[localized_name]

			return super().__getattribute__(attr_name)

		except AttributeError:
			raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr_name}'")
		
	def set_lang_value(self, attr_name: str, value: Any) -> None:
		setattr(self, f"{attr_name}_{get_language()}", value)
		
	def lang_callback(self, callback: callable, *args, **kwargs):
		og_lang: str = get_language()

		for lang, _ in settings.LANGUAGES:
			activate(lang)
			callback(*args, **kwargs)

		activate(og_lang)
