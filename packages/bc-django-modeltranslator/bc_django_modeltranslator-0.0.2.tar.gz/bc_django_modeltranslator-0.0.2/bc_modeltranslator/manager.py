from django.db.models import Manager

from .queryset import BcTranslatedQuerySet

class BcTranslatedManager(Manager):
	def get_queryset(self) -> BcTranslatedQuerySet:
		return BcTranslatedQuerySet(self.model, using=self._db)
	
	def filter(self, *args, **kwargs):
		return self.get_queryset().filter(*args, **kwargs)
