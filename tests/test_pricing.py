import unittest
from datetime import date

from checkout import CouponError, apply_coupon


class ApplyCouponTests(unittest.TestCase):
    def test_valid_coupon_applies_discount(self):
        coupon = {"code": "FALL20", "percent_off": 20, "expires": "30/11/2026"}
        self.assertEqual(apply_coupon(10_000, coupon, today=date(2026, 11, 1)), 8_000)

    def test_coupon_expired_earlier_same_month_is_rejected(self):
        coupon = {"code": "OLD10", "percent_off": 10, "expires": "01/11/2026"}
        with self.assertRaises(CouponError):
            apply_coupon(10_000, coupon, today=date(2026, 11, 20))

    def test_coupon_expired_in_earlier_month_is_rejected(self):
        coupon = {"code": "SEPT25", "percent_off": 25, "expires": "30/09/2026"}
        with self.assertRaises(CouponError):
            apply_coupon(10_000, coupon, today=date(2026, 11, 5))

    def test_coupon_expired_in_earlier_year_is_rejected(self):
        coupon = {"code": "DEC25", "percent_off": 25, "expires": "15/12/2025"}
        with self.assertRaises(CouponError):
            apply_coupon(10_000, coupon, today=date(2026, 1, 1))

    def test_coupon_valid_in_later_month_with_smaller_day_is_accepted(self):
        coupon = {"code": "DEC10", "percent_off": 10, "expires": "05/12/2026"}
        self.assertEqual(apply_coupon(10_000, coupon, today=date(2026, 11, 20)), 9_000)

    def test_coupon_is_valid_on_its_expiry_date(self):
        coupon = {"code": "LAST", "percent_off": 10, "expires": "20/11/2026"}
        self.assertEqual(apply_coupon(10_000, coupon, today=date(2026, 11, 20)), 9_000)

    def test_invalid_percentage_is_rejected(self):
        coupon = {"code": "BROKEN", "percent_off": 0, "expires": "30/11/2026"}
        with self.assertRaises(CouponError):
            apply_coupon(10_000, coupon, today=date(2026, 11, 1))


if __name__ == "__main__":
    unittest.main()
