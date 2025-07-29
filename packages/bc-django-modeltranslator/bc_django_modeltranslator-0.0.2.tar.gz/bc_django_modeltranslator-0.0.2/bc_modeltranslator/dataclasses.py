from typing import Dict, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class BcTranslationFieldParams:
	verbose_name: Optional[str] = None
	default: Optional[str] = None
	blank: Optional[bool] = None
	help_text: Optional[str] = None
	max_length: Optional[int] = None
	null: Optional[bool] = None
	unique: Optional[bool] = None

	def dict(self, nullable: bool = False) -> dict:		
		return dict(
			filter(
				lambda item: True if item[-1] != None else False, self.__dict__.items()
				)
			) if not nullable else self.__dict__


@dataclass(frozen=True)
class BcTranslationField:
	field_name: str
	params: Optional[Dict[str, BcTranslationFieldParams]] = None
