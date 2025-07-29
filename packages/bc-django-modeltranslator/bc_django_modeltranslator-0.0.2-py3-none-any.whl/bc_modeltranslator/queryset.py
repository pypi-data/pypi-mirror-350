from typing import Any, Dict
from django.db.models import QuerySet
from django.utils.translation import get_language

class BcTranslatedQuerySet(QuerySet):
	def _translate_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
		from .registry import bc_translator
		from .dataclasses import BcTranslationField
	
		lang: str = get_language()
		model = self.model
		opts = bc_translator._registry.get(model)

		if not opts:
			return kwargs

		fields: tuple[BcTranslationField, ...] = getattr(opts, 'fields', ())
		translated_fields: set[str] = {field.field_name for field in fields}

		new_kwargs: Dict[str, Any] = {}
		for key, value in kwargs.items():
			parts = key.split('__')
			base: str = parts[0].split("_")[0]
			suffix: str = '__'.join(parts[1:]) if len(parts) > 1 else ''

			if base in translated_fields:
				new_key = f"{base}_{lang}"
			
			else:
				new_key = base

			if suffix:
				new_key = f"{new_key}__{suffix}"

			new_kwargs[new_key] = value

		return new_kwargs

	def filter(self, *args: Any, **kwargs: Any) -> "BcTranslatedQuerySet":
		return super().filter(*args, **self._translate_kwargs(kwargs))

	def exclude(self, *args: Any, **kwargs: Any) -> "BcTranslatedQuerySet":
		return super().exclude(*args, **self._translate_kwargs(kwargs))

	def get(self, *args: Any, **kwargs: Any) -> Any:
		return super().get(*args, **self._translate_kwargs(kwargs))
