"""Checkout pricing for the demo store.

Coupons come from the promotions service as plain dicts, for example

    {"code": "FALL20", "percent_off": 20, "expires": "15/11/2026"}

Expiry dates are stored in the promotions service's display format (DD/MM/YYYY).
"""

from datetime import date, datetime


class CouponError(ValueError):
    """Raised when a coupon cannot be applied to an order."""


EXPIRY_FORMAT = "%d/%m/%Y"


def _parse_expiry(coupon: dict) -> date:
    try:
        return datetime.strptime(coupon["expires"], EXPIRY_FORMAT).date()
    except (KeyError, TypeError, ValueError):
        raise CouponError(f"invalid expiry date on coupon {coupon.get('code')}") from None


def apply_coupon(subtotal_cents: int, coupon: dict, today: date) -> int:
    """Return the new subtotal in cents after applying the coupon."""
    if subtotal_cents < 0:
        raise ValueError("subtotal cannot be negative")

    percent = coupon.get("percent_off", 0)
    if not 0 < percent <= 100:
        raise CouponError(f"invalid discount on coupon {coupon.get('code')}")

    # Reject coupons that have already expired.
    if _parse_expiry(coupon) < today:
        raise CouponError(f"coupon {coupon['code']} has expired")

    discount = subtotal_cents * percent // 100
    return subtotal_cents - discount
