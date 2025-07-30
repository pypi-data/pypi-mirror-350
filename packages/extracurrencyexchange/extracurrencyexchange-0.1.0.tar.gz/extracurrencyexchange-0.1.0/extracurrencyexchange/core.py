"""Currency Exchange plugin with more supported currency"""

import structlog
import json

from plugin import InvenTreePlugin
from plugin.mixins import CurrencyExchangeMixin, APICallMixin

from . import PLUGIN_VERSION

logger = structlog.get_logger('extracurrencyexchange')


class ExtraCurrencyExchange(APICallMixin, CurrencyExchangeMixin, InvenTreePlugin):
    """ExtraCurrencyExchange - custom InvenTree plugin using exchangerate.host."""

    # Plugin metadata
    TITLE = "ExtraCurrencyExchange"
    NAME = "ExtraCurrencyExchange"
    SLUG = "extracurrencyexchange"
    DESCRIPTION = "Currency Exchange plugin with more supported currency (exchangerate.host)"
    VERSION = PLUGIN_VERSION

    AUTHOR = "Alex Le"
    LICENSE = "MIT"

    # Optionally specify supported InvenTree versions
    # MIN_VERSION = '0.18.0'
    # MAX_VERSION = '2.0.0'

    # Plugin settings (from SettingsMixin)
    SETTINGS = {
        'CUSTOM_VALUE': {
            'name': 'Custom Value',
            'description': 'A custom value',
            'validator': int,
            'default': 42,
        }
    }

    def update_exchange_rates(self, base_currency: str, symbols: list[str]) -> dict:
        """Request exchange rate data from external API."""
        response = self.api_call(
            f'currencies/{base_currency.lower()}.json',
            simple_response=False,
        )

        print("API response:", response.json())

        if response.status_code == 200:
            rates = response.json().get(f'{base_currency.lower()}', {})
            print("Rates:", rates)

            rates = {
                symbol: rates.get(symbol.lower())
                for symbol in symbols
                if symbol.lower() in rates
            }
            print("Rates after:", rates)

            rates[base_currency] = 1.00

            return rates
        logger.warning(
            'Failed to update exchange rates from %s: Server returned status %s',
            self.api_url,
            response.status_code,
        )
        return {}

    @property
    def api_url(self):
        """Return the API URL for this plugin."""
        return 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1'
