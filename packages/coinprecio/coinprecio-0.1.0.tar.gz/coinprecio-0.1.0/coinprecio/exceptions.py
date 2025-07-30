# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

class CoinApiError(Exception):
    pass

class CoinApiFetchError(CoinApiError):
    pass

class CoinApiFactoryError(CoinApiError):
    pass

class CoinApiDataError(CoinApiError):
    pass
