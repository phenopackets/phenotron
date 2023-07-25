import pytest
from phenotron import ClickValidator

@pytest.mark.parametrize('value', ("0000-0002-2157-3591", "0000-0002-0736-9199"))
def test_click_validator_orcid_passes(value):
    assert ClickValidator.is_orcid(None, None, value) == value

@pytest.mark.parametrize('value', ("not an orcid", "you wish this was an orcid"))
def test_click_validator_orcid_fails(value):
    with pytest.raises(Exception) as e_info:
        ClickValidator.is_orcid(None, None, value)

@pytest.mark.parametrize('value', ("\t", ","))
def test_click_validator_orcid_passes(value):
    assert ClickValidator.is_sep(None, None, value) == value

@pytest.mark.parametrize('value', (";", "|"))
def test_click_validator_orcid_fails(value):
    with pytest.raises(Exception) as e_info:
        ClickValidator.is_sep(None, None, value)
