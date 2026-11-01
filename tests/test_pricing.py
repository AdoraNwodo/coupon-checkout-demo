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

    def test_invalid_percentage_is_rejected(self):
        coupon = {"code": "BROKEN", "percent_off": 0, "expires": "30/11/2026"}
        with self.assertRaises(CouponError):
            apply_coupon(10_000, coupon, today=date(2026, 11, 1))


if __name__ == "__main__":
    unittest.main()
