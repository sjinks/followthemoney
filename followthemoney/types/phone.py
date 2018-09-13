from rdflib import URIRef
from banal import ensure_list
from phonenumbers import geocoder
from phonenumbers import parse as parse_number
from phonenumbers import is_possible_number, is_valid_number, format_number
from phonenumbers import PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException

from followthemoney.types.common import PropertyType


class PhoneType(PropertyType):
    name = 'phone'
    group = 'phones'
    prefix = 'tel'

    def _clean_countries(self, countries, country):
        result = set([None])
        countries = ensure_list(countries)
        countries.extend(ensure_list(country))
        for country in countries:
            if isinstance(country, str):
                country = country.strip().upper()
                result.add(country)
        return result

    def clean_text(self, number, countries=None, country=None, **kwargs):
        """Parse a phone number and return in international format.

        If no valid phone number can be detected, None is returned. If
        a country code is supplied, this will be used to infer the
        prefix.

        https://github.com/daviddrysdale/python-phonenumbers
        """
        for code in self._clean_countries(countries, country):
            try:
                num = parse_number(number, code)
                if is_possible_number(num):
                    if is_valid_number(num):
                        return format_number(num, PhoneNumberFormat.E164)
            except NumberParseException:
                pass

    def specificity(self, value):
        return 1

    def country_hint(self, value):
        try:
            number = parse_number(value)
            return geocoder.region_code_for_number(number)
        except NumberParseException:
                pass

    def rdf(self, value):
        return URIRef('tel:%s' % value)
