import unittest
from datetime import datetime

from caplib.fxmarket import *

class TestFxMarket(unittest.TestCase):

    def setUp(self):
        
        hol_serial_numbers =[44654, 44954]
        sbd_serial_numbers = [44655]
        # Convert list of serial numbers to datetime objects
        holidays = [datetime.fromordinal(sn) for sn in hol_serial_numbers]
        specials = [datetime.fromordinal(sn) for sn in sbd_serial_numbers]
        create_calendar('CAL_CFETS', holidays, specials)
        
        self.fx_ndf_template = create_fx_ndf_template(inst_name="TestFxNdf",
                                                      fixing_offset="180d",
                                                      currency_pair="EURUSD",
                                                      delivery_day_convention="MODIFIED_PRECEDING",
                                                      fixing_day_convention="MODIFIED_PRECEDING",
                                                      calendars=["CAL_CFETS"],
                                                      settlement_currency="USD")
        self.fx_swap_template = create_fx_swap_template(inst_name="TestFxSwap",
                                                        start_convention="INVALID_INSTRUMENT_START_CONVENTION",
                                                        currency_pair="EURUSD",
                                                        calendars=["CAL_CFETS"],
                                                        start_day_convention="MODIFIED_PRECEDING",
                                                        end_day_convention="MODIFIED_PRECEDING",
                                                        fixing_offset="180d",
                                                        fixing_day_convention="MODIFIED_PRECEDING")
        self.fx_fwd_template = create_fx_forward_template(inst_name="TestFxForward",
                                                          fixing_offset="180d",
                                                          currency_pair="EURUSD",
                                                          delivery_day_convention="MODIFIED_PRECEDING",
                                                          fixing_day_convention="MODIFIED_PRECEDING",
                                                          calendars=["CAL_CFETS"])

    def test_create_fx_forward_template(self):
        expected1 = b'\x08\xba\x17\x12\rTestFxForward\x1a\x05\x08\xb4\x01\x10\x01"\x0e\n\x05\n\x03EUR\x12\x05\n\x03USD(\x040\x04:\tCAL_CFETS'
        test1 = create_fx_forward_template(inst_name="TestFxForward",
                                           fixing_offset="180d",
                                           currency_pair="EURUSD",
                                           delivery_day_convention="MODIFIED_PRECEDING",
                                           fixing_day_convention="MODIFIED_PRECEDING",
                                           calendars=["CAL_CFETS"])
        self.assertEqual(test1.SerializeToString(), expected1)

        expected2 = b'\x08\xba\x17\x12\rTestFxForward\x1a\x05\x08\xb4\x01\x10\x01"\x0e\n\x05\n\x03USD\x12\x05\n\x03CNY(\x040\x04:\tCAL_CFETS'
        test2 = create_fx_forward_template(inst_name="TestFxForward",
                                           fixing_offset="180d",
                                           currency_pair="USDCNY",
                                           delivery_day_convention="MODIFIED_PRECEDING",
                                           fixing_day_convention="MODIFIED_PRECEDING",
                                           calendars=["CAL_CFETS"])
        self.assertEqual(test2.SerializeToString(), expected2)

    def test_create_fx_swap_template(self):
        expected1 = b'\x08\xbc\x17\x12\nTestFxSwap"\x0e\n\x05\n\x03EUR\x12\x05\n\x03USD*\tCAL_CFETS0\x048\x04B\x05\x08\xb4\x01\x10\x01H\x04'
        test1 = create_fx_swap_template(inst_name="TestFxSwap",
                                        start_convention="INVALID_INSTRUMENT_START_CONVENTION",
                                        currency_pair="EURUSD",
                                        calendars=["CAL_CFETS"],
                                        start_day_convention="MODIFIED_PRECEDING",
                                        end_day_convention="MODIFIED_PRECEDING",
                                        fixing_offset="180d",
                                        fixing_day_convention="MODIFIED_PRECEDING")
        self.assertEqual(test1.SerializeToString(), expected1)

        expected2 = b'\x08\xbc\x17\x12\nTestFxSwap"\x0e\n\x05\n\x03USD\x12\x05\n\x03CNY*\tCAL_CFETS0\x048\x04B\x05\x08\xb4\x01\x10\x01H\x04'
        test2 = create_fx_swap_template(inst_name="TestFxSwap",
                                        start_convention="INVALID_INSTRUMENT_START_CONVENTION",
                                        currency_pair="USDCNY",
                                        calendars=["CAL_CFETS"],
                                        start_day_convention="MODIFIED_PRECEDING",
                                        end_day_convention="MODIFIED_PRECEDING",
                                        fixing_offset="180d",
                                        fixing_day_convention="MODIFIED_PRECEDING")
        self.assertEqual(test2.SerializeToString(), expected2)

    def test_create_fx_ndf_template(self):
        expected = b'\x08\xbb\x17\x12\tTestFxNdf\x1a\x05\x08\xb4\x01\x10\x01"\x0e\n\x05\n\x03EUR\x12\x05\n\x03USD(\x040\x04:\tCAL_CFETSB\x03USD'
        test = create_fx_ndf_template(inst_name="TestFxNdf",
                                      fixing_offset="180d",
                                      currency_pair="EURUSD",
                                      delivery_day_convention="MODIFIED_PRECEDING",
                                      fixing_day_convention="MODIFIED_PRECEDING",
                                      calendars=["CAL_CFETS"],
                                      settlement_currency="USD")
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_fx_non_deliverable_forwad(self):
        expected1 = b'\n\x03USD\x11\x00\x00\x00\x00\x00\x81\xc4@\x1a\x03EUR!\x00\x00\x00\x00\x00\x88\xc3@*\x07\x08\xe6\x0f\x10\x0c\x18\x152\x07\x08\xed\x0e\x10\x01\x18\x01:\x03USD'
        test1 = create_fx_non_deliverable_forwad(buy_currency="USD",
                                                 buy_amount=10498,
                                                 sell_currency="EUR",
                                                 sell_amount=10000,
                                                 delivery_date=datetime(2022, 12, 21),
                                                 expiry_date=None,
                                                 settlement_currency="USD")
        self.assertEqual(test1.SerializeToString(), expected1)

        expected2 = b'\n\x03USD\x11\x00\x00\x00\x00\x00\x81\xc4@\x1a\x03EUR!\x00\x00\x00\x00\x00\x88\xc3@*\x07\x08\xe6\x0f\x10\x0c\x18\x152\x07\x08\xe6\x0f\x10\x0c\x18\x13:\x03USD'
        test2 = create_fx_non_deliverable_forwad(buy_currency="USD",
                                                 buy_amount=10498,
                                                 sell_currency="EUR",
                                                 sell_amount=10000,
                                                 delivery_date=datetime(2022, 12, 21),
                                                 expiry_date=datetime(2022, 12, 19),
                                                 settlement_currency="USD")
        self.assertEqual(test2.SerializeToString(), expected2)

    def test_create_fx_swap(self):
        expected1 = b'\n\x03USD\x11\x00\x00\x00\x00\x00\x82\xc4@\x1a\x03EUR!\x00\x00\x00\x00\x00\x88\xc3@*\x07\x08\xe6\x0f\x10\x0c\x18\x152\x07\x08\xed\x0e\x10\x01\x18\x01:\x03USDA\x00\x00\x00\x00\x00\x82\xc4@J\x03EURQ\x00\x00\x00\x00\x00\x88\xc3@Z\x07\x08\xe7\x0f\x10\x0c\x18\x15b\x07\x08\xed\x0e\x10\x01\x18\x01'
        test1 = create_fx_swap(near_buy_currency="USD",
                               near_buy_amount=10500,
                               near_sell_currency="EUR",
                               near_sell_amount=10000,
                               near_delivery_date=datetime(2022, 12, 21),
                               near_expiry_date=None,
                               far_buy_currency="USD",
                               far_buy_amount=10500,
                               far_sell_currency="EUR",
                               far_sell_amount=10000,
                               far_delivery_date=datetime(2023, 12, 21),
                               far_expiry_date=None)
        #print(test1.SerializeToString())
        self.assertEqual(test1.SerializeToString(), expected1)

        expected2 = b'\n\x03USD\x11\x00\x00\x00\x00\x00\x82\xc4@\x1a\x03EUR!\x00\x00\x00\x00\x00\x88\xc3@*\x07\x08\xe6\x0f\x10\x0c\x18\x152\x07\x08\xe6\x0f\x10\x0c\x18\x13:\x03USDA\x00\x00\x00\x00\x00\x82\xc4@J\x03EURQ\x00\x00\x00\x00\x00\x88\xc3@Z\x07\x08\xe7\x0f\x10\x0c\x18\x15b\x07\x08\xe7\x0f\x10\x0c\x18\x13'
        test2 = create_fx_swap(near_buy_currency="USD",
                               near_buy_amount=10500,
                               near_sell_currency="EUR",
                               near_sell_amount=10000,
                               near_delivery_date=datetime(2022, 12, 21),
                               near_expiry_date=datetime(2022, 12, 19),
                               far_buy_currency="USD",
                               far_buy_amount=10500,
                               far_sell_currency="EUR",
                               far_sell_amount=10000,
                               far_delivery_date=datetime(2023, 12, 21),
                               far_expiry_date=datetime(2023, 12, 19)
        )
        self.assertEqual(test2.SerializeToString(), expected2)

    def test_create_fx_forward(self):
        expected1 = b'\n\x03USD\x11\x00\x00\x00\x00\x00\x82\xc4@\x1a\x03EUR!\x00\x00\x00\x00\x00\x88\xc3@*\x07\x08\xe6\x0f\x10\x0c\x18\x152\x07\x08\xed\x0e\x10\x01\x18\x01'
        test1 = create_fx_forward(buy_currency="USD",
                                  buy_amount=10500,
                                  sell_currency="EUR",
                                  sell_amount=10000,
                                  delivery=datetime(2022, 12, 21),
                                  expiry=None)
        
        self.assertEqual(test1.SerializeToString(), expected1)

        expected2 = b'\n\x03USD\x11\x00\x00\x00\x00\x00\x82\xc4@\x1a\x03EUR!\x00\x00\x00\x00\x00\x88\xc3@*\x07\x08\xe6\x0f\x10\x0c\x18\x152\x07\x08\xe6\x0f\x10\x0c\x18\x13'
        test2 = create_fx_forward(buy_currency="USD",
                                  buy_amount=10500,
                                  sell_currency="EUR",
                                  sell_amount=10000,
                                  delivery=datetime(2022, 12, 21),
                                  expiry=datetime(2022, 12, 19))
        #print(test2.SerializeToString())
        self.assertEqual(test2.SerializeToString(), expected2)


if __name__ == "__main__":
    unittest.main()
