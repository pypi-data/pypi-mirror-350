from modeltranslation.translator import translator, TranslationOptions
from cookie_consent.models import CookieGroup

class CookieGroupTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(CookieGroup, CookieGroupTranslationOptions)
