from pathlib import Path
import numpy as np
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]/'app.py'
def app():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception
    return at

def test_liability_and_asset_rollforwards():
    at=app()
    at.slider[2].set_value(3).run()
    ledger=at.dataframe[0].value
    np.testing.assert_allclose(ledger.accrual_balance,(ledger.earned-ledger.cash_paid).cumsum())
    np.testing.assert_allclose(ledger.commission_asset,(ledger.capitalized-ledger.amortization).cumsum())
    assert (ledger.accrual_balance>=0).all()
