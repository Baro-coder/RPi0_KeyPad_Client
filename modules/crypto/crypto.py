#!/usr/bin/python
# -- KeyPad_Client/modules/crypto: crypto.py --

from enum import Enum

import modules.crypto.pricer as prc

class CryptoOption(Enum):
    BITCOIN = 0
    ETHERUM = 1


class SectionManager:
    HEADER = 'CRYPTO'
    option_id = 0
    
    @staticmethod
    def next_option():
        SectionManager.option_id += 1
        if SectionManager.option_id == 2:
            SectionManager.option_id = 0
            
    @staticmethod
    def prev_option():
        SectionManager.option_id -= 1
        if SectionManager.option_id == -1:
            SectionManager.option_id = 1
    
    
    @staticmethod
    def get_option_header():
        return f'{CryptoOption(SectionManager.option_id).value + 1}: {CryptoOption(SectionManager.option_id).name}'
    
    
    @staticmethod
    def get_option_output():
        if SectionManager.option_id == CryptoOption.BITCOIN.value:
            output = SectionManager._get_bitcoin_course()
            
        elif SectionManager.option_id == CryptoOption.ETHERUM.value:
            output = SectionManager._get_etherum_course()
        
        if output is None:
            output = '-- Request Error --'.center(24)
        
        return output
    
    
    @staticmethod
    def _get_bitcoin_course():
        return prc.get_BTC_price()
    
    
    @staticmethod
    def _get_etherum_course():
        return prc.get_ETH_price()