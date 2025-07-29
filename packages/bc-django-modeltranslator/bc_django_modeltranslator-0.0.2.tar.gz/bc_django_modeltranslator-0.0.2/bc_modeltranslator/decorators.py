from .registry import BcTranslationOptions, bc_translator

def register(model_or_iterable, **options):
	def wrapper(opts_class):
		if not issubclass(opts_class, BcTranslationOptions):
			raise ValueError("Wrapped class must subclass TranslationOptions.")

		bc_translator.register(model_or_iterable, opts_class, **options)
		return opts_class
	
	return wrapper
