# bc-model-translator

This is a lightweight and extensible Django app for model field translations based on the current active language.

Supports dynamic field registration, localized querying, and transparent field access using Python magic.

## ✨ Features

- Automatic creation of translated fields (`name_en`, `name_ru`, etc.)
- Transparent access to localized values via model attributes
- Language-aware `filter()`, `get()`, and `exclude()` on QuerySets
- Simple registration system via decorators
- Integration-ready: autodiscovery of `translation.py` files
- Per-language field customization — configure attributes like verbose_name, max_length, default, etc., per field and language via BcTranslationFieldParams

## 🚀 Installation

```bash
pip install bc-django-modeltranslator
```

Add the app to INSTALLED_APPS:

# ⚙️ Configuration

## 1. Add the app to INSTALLED_APPS 


```python
INSTALLED_APPS = [
    ...
    "bc_modeltranslator",
]
```

## 2. Available settings:

```python
# Temporarily disable translation registration if needed
MODELTRANSLATION_ENABLE_REGISTRATIONS = True

# Filename to look for in each app (default: "translation")
TRANS_FILENAME = "translation"
```

The TRANS_FILENAME setting defines the file name (without .py) that the app will look for in each Django app to discover translation registration.

# 🛠️ Usage

## Create a translation.py file inside your Django app.

This file is automatically discovered on startup.

```python
# your_app/translation.py

from bc_modeltranslater import register, BcTranslationOptions, BcTranslationField, BcTranslationFieldParams
from .models import TestModel

@register(TestModel)
class SymptomTranslationOptions(BcTranslationOptions):
    fields = [
        BcTranslationField(field_name="name"),
        BcTranslationField(
            field_name="desc",
            params={
                "fr": BcTranslationFieldParams(verbose_name="Description in French"),
                "kk": BcTranslationFieldParams(verbose_name="Kazakh description"),
            }
        )
    ]
```

## 🛠️ Available field parameters

```python
BcTranslationFieldParams(
    verbose_name: str | None = None,
    default: str | None = None,
    blank: bool | None = None,
    help_text: str | None = None,
    max_length: int | None = None,
    null: bool | None = None,
    unique: bool | None = None
)
```

You can define different attributes per language using the params dictionary, where each key is a language code ("en", "ru", "fr", etc.).

## 🔍 Querying

All query methods automatically use the active language:

```python
from django.utils.translation import activate

activate("ru")
TestModel.objects.filter(name="Имя")  # Filters by name_ru
```

## 🧠 Field Access

You can access localized values through normal attribute access:

```python
obj = TestModel.objects.first()
print(obj.name)  # Returns name_ru or name_en depending on current language
```
