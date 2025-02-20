from unittest.mock import patch
from mock import MagicMock
import pytest

from sonic_platform_base.sonic_xcvr.api.credo.aec_800g import CmisAec800gApi
from sonic_platform_base.sonic_xcvr.mem_maps.credo.aec_800g import CmisAec800gMemMap
from sonic_platform_base.sonic_xcvr.xcvr_eeprom import XcvrEeprom
from sonic_platform_base.sonic_xcvr.codes.credo.aec_800g import CmisAec800gCodes
from sonic_platform_base.sonic_xcvr.fields import consts
from sonic_platform_base.sonic_xcvr.xcvr_api_factory import XcvrApiFactory

class BytesMock(bytes):
    def decode(self, encoding='utf-8', errors='strict'):
        return 'DecodedCredo'

class TestXcvrApiFactory(object):
    read_eeprom = MagicMock
    write_eeprom = MagicMock
    api = XcvrApiFactory(read_eeprom, write_eeprom)

    def test_get_vendor_name(self):
        self.api.reader = MagicMock()
        self.api.reader.return_value = b'Credo'
        with patch.object(BytesMock, 'decode', return_value='DecodedCredo'):
            result = self.api._get_vendor_name()
        assert result == 'Credo'.strip()

    def test_get_vendor_part_num(self):
        self.api.reader = MagicMock()
        self.api.reader.return_value = b'CAC81X321M2MC1MS'
        with patch.object(BytesMock, 'decode', return_value='DecodedCAC81X321M2MC1MS'):
            result = self.api._get_vendor_part_num()
        assert result == 'CAC81X321M2MC1MS'.strip()

    def mock_reader(self, start, length):
        return bytes([0x18])

    @patch('sonic_platform_base.sonic_xcvr.xcvr_api_factory.XcvrApiFactory._get_vendor_name', MagicMock(return_value='Credo'))
    @patch('sonic_platform_base.sonic_xcvr.xcvr_api_factory.XcvrApiFactory._get_vendor_part_num', MagicMock(return_value='CAC81X321M2MC1MS'))
    def test_create_xcvr_api(self):
        self.api.reader = self.mock_reader
        CmisAec800gCodes = MagicMock()
        CmisAec800gMemMap = MagicMock()
        XcvrEeprom = MagicMock()
        CmisAec800gApi = MagicMock()
        self.api.create_xcvr_api()

