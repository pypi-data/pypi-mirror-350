import pytest
from decimal import Decimal
from ostium_python_sdk.formulae import GetTradeLiquidationPrice

# Global list of all test cases
test_cases = [
    # CASE-0
    {
        'openPrice': Decimal('92961.71'),
        'isLong': True,
        'collateral': Decimal('98'),
        'leverage': Decimal('20'),
        'rollover_fee': Decimal('0'),
        'current_funding_fee': Decimal('2757.79'),
        'expected_liq_price': Decimal('219578.879081')
    },
    # CASE-1
    {
        "openPrice":  Decimal("1823.52"),
        "isLong": False,
        "collateral": Decimal("1000"),
        "leverage":   Decimal("100"),
        "rollover_fee": Decimal("10"),
        "current_funding_fee": Decimal("-4"),
        "expected_liq_price": Decimal("1839.8222688"),
    },
    # CASE-2
    {
        "openPrice":  Decimal("129.4"),
        "isLong": True,
        "collateral": Decimal("250"),
        "leverage":   Decimal("20"),
        "rollover_fee": Decimal("5"),
        "current_funding_fee": Decimal("2"),
        "expected_liq_price": Decimal("123.75816"),
    },
    # CASE-3
    {
        "openPrice":  Decimal("27.2"),
        "isLong": False,
        "collateral": Decimal("100"),
        "leverage":   Decimal("2"),
        "rollover_fee": Decimal("2"),
        "current_funding_fee": Decimal("-0.5"),
        "expected_liq_price": Decimal("39.236"),
    },
    # CASE-4
    {
        "openPrice":  Decimal("1.34"),
        "isLong": False,
        "collateral": Decimal("1000"),
        "leverage":   Decimal("50"),
        "rollover_fee": Decimal("23"),
        "current_funding_fee": Decimal("1"),
        "expected_liq_price": Decimal("1.3634768"),
    },
    {
        "openPrice":  Decimal("8704.50"),
        "isLong": True,
        "collateral": Decimal("99"),
        "leverage":   Decimal("20"),
        "rollover_fee": Decimal("0"),
        "current_funding_fee": Decimal("0"),
        "expected_liq_price": Decimal("8312.7975"),
    },
]


@pytest.mark.parametrize("case", test_cases)
def test_trade_liquidation_price(case):
    """Test multiple scenarios for GetTradeLiquidationPrice with Pytest."""

    # Optionally print the case for debugging
    print(f"\n\n===> case: {case}")

    liq_price = GetTradeLiquidationPrice(
        open_price=case['openPrice'],
        long=case['isLong'],
        collateral=case['collateral'],
        leverage=case['leverage'],
        rollover_fee=case['rollover_fee'],
        funding_fee=case['current_funding_fee']
    )

    # Equivalent to assertAlmostEqual(..., places=5) is approx with abs=1e-5
    # or thereabouts. Adjust as needed for your precision.
    assert liq_price == pytest.approx(case['expected_liq_price'], abs=1e-5), \
        f"Failed for case: {case}"
