from unittest.mock import patch

import pytest
from atlantisfastapi import AtlantisFinder


def test_atlantis_finder_find_spec_not_atlantisfastapi():
    assert AtlantisFinder.find_spec("test") is None


def test_atlantis_finder_find_spec_found_in_atlantisfastapi(mocker):
    AtlantisFinder.finding_in_atlantis = False
    with patch("atlantisfastapi.find_spec", return_value=mocker.MagicMock()):
        assert AtlantisFinder.find_spec("atlantisfastapi.test") is None
        assert not AtlantisFinder.finding_in_atlantis


def test_atlantis_finder_dont_recurse():
    AtlantisFinder.finding_in_atlantis = True
    assert AtlantisFinder.find_spec("atlantisfastapi.test") is None


def test_atlantis_finder_find_spec_found_in_coderfastapi():
    AtlantisFinder.finding_in_atlantis = False
    name = "atlantisfastapi.test"
    with patch("atlantisfastapi.find_spec", return_value=None):
        spec = AtlantisFinder.find_spec(name)
        assert spec.name == name
        assert spec.loader == AtlantisFinder
        assert not AtlantisFinder.finding_in_atlantis


def test_atlantis_finder_create_module(mocker):
    module = mocker.MagicMock()
    spec = mocker.MagicMock()
    spec.name = "atlantisfastapi"
    with patch("atlantisfastapi.import_module", return_value=module) as import_mock:
        created_module = AtlantisFinder.create_module(spec)
        assert created_module == module
        import_mock.assert_called_once_with("coderfastapi")


def test_atlantis_finder_create_module_with_attr(mocker):
    module = mocker.MagicMock()
    spec = mocker.MagicMock()
    spec.name = "atlantisfastapi.test"
    with patch(
        "atlantisfastapi.import_module",
        side_effect=(ModuleNotFoundError, module),
    ) as import_mock:
        created_module = AtlantisFinder.create_module(spec)
        assert created_module == module.test
        import_mock.assert_called_with("coderfastapi")


def test_atlantis_finder_create_module_not_found(mocker):
    spec = mocker.MagicMock()
    spec.name = "atlantisfastapi"
    exception = ModuleNotFoundError()
    with (
        patch("atlantisfastapi.import_module", side_effect=exception),
        pytest.raises(ModuleNotFoundError) as e,
    ):
        AtlantisFinder.create_module(spec)
    assert e.value == exception


def test_atlantis_finder_exec_module(mocker):
    AtlantisFinder.exec_module(mocker.MagicMock())
