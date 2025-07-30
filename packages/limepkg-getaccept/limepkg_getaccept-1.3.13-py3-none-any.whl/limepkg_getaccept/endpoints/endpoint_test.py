import lime_test.app
import lime_test.db
import lime_test.web_app
import pytest


def test_dummy():
    assert True


@pytest.fixture
def webapp(limeapp, database, plugins_path, monkeypatch):
    """An in-memory web application where you're authenticated as a user"""
    web_app = lime_test.web_app.create_web_app(database,
                                               plugins_path=plugins_path,
                                               monkeypatch=monkeypatch)

    return lime_test.web_app.create_authenticated_web_client(web_app=web_app,
                                                             app=limeapp,
                                                             username='kenny',
                                                             password='kenny')


@pytest.fixture
def acme_company(limeapp):
    """A company that gets added to `limeapp`"""
    uow = limeapp.unit_of_work()
    acme = limeapp.limetypes.company(name='Acme Inc.')
    acme_idx = uow.add(acme)
    res = uow.commit()
    return res.get(acme_idx)
