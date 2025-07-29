import pytest
from wilson_wrapper.beta_patch import patch_wilson_beta, configure_patch
import wilson.run.smeft.beta as betamodule

# Save original beta so we can restore after testing
original_beta_function = betamodule.beta

@pytest.fixture(autouse=True)
def patch_dummy_beta():
    # Dummy beta function that mimics the signature of the real one
    def dummy_beta(C, Highscale=1, newphys=True):
        return {'lq1_1221': 42, 'other_key': 7}
    
    betamodule.beta = dummy_beta
    yield
    betamodule.beta = original_beta_function  # Restore after each test

def test_patch_applies_correctly():
    patch_wilson_beta(required_key='lq1_1221')
    configure_patch('lq1_1221', 100)
    result = betamodule.beta(C={})
    assert result['lq1_1221'] == 100
    assert result['other_key'] == 7

def test_key_not_present():
    patch_wilson_beta(required_key='non_existent_key')
    configure_patch('non_existent_key', 999)
    result = betamodule.beta(C={})
    # Should fall back to default dummy_beta result
    assert result['lq1_1221'] == 42
    assert result['other_key'] == 7

def test_reconfigure_patch():
    patch_wilson_beta(required_key='lq1_1221')
    configure_patch('lq1_1221', 200)
    result = betamodule.beta(C={})
    assert result['lq1_1221'] == 200

    configure_patch('lq1_1221', -99)
    result2 = betamodule.beta(C={})
    assert result2['lq1_1221'] == -99

def test_noop_if_key_absent():
    patch_wilson_beta(required_key='nonexistent')
    configure_patch('nonexistent', 123)
    result = betamodule.beta(C={})
    assert 'nonexistent' not in result


def test_empty_beta_dict():
    def empty_beta(C, Highscale=1, newphys=True):
        return {}
    betamodule.beta = empty_beta
    patch_wilson_beta(required_key='lq1_1221')
    configure_patch('lq1_1221', 1)
    result = betamodule.beta(C={})
    assert result == {}
