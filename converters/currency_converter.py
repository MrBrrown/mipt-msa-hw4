from abc import ABC, abstractmethod
import json
import logging
import time

import requests

CACHE_EXPIRE = 3600

class CurrencyConverter(ABC):
    def __init__(self, max_retries=3, retry_delay=2):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = self._setup_logger()
        self.last_cache_time = 0
        self.rates = {}
        self.API_URL = ""


    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger


    def _fetch_rates(self):
        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.API_URL, timeout=10)
                response.raise_for_status()
                data = response.json()
                self.rates = data['rates']
                self.last_cache_time = time.time()
                return
            
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    self.logger.error("Max retries reached.  Unable to fetch rates.")
                    self.rates = {}
                    self.last_cache_time = 0
                    return

            except (json.JSONDecodeError, KeyError) as e:
                self.logger.error(f"Error processing JSON response: {e}")
                self.rates = {}
                self.last_cache_time = 0
                return

    def _get_actual_rates(self) -> dict:
        current_time = time.time()
        if current_time - self.last_cache_time > CACHE_EXPIRE:
            self._fetch_rates()
            
        return self.rates


    @abstractmethod
    def convert(self, target_currency: str, amount: float) -> float:
        pass