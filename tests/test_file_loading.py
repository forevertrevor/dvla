from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from loan_analysis import DataLoader


def test_loads_xml_as_loans_object():

    # WHEN
    data_loader = DataLoader()
    result = data_loader.load_data()

    # THEN
    assert len(result) == 20


@patch("loan_analysis.logging.exception")
def test_throws_if_invalid_path_is_provided(mock_logger: MagicMock):
    # GIVEN
    path_to_non_existent_file = Path(__file__).parent / "nowhere" / "invalid_xml.xml"

    with pytest.raises(OSError):
        # WHEN
        data_loader = DataLoader(path_to_non_existent_file)
        data_loader.load_data()

    # THEN
    mock_logger.assert_called_once_with("Could not load file from path provided")


@patch("loan_analysis.logging.exception")
def test_throws_if_xml_is_invalid(mock_logger: MagicMock):
    # GIVEN
    path_to_invalid_xml = Path(__file__).parent / "data" / "invalid_xml.xml"

    with pytest.raises(Exception):
        # WHEN
        data_loader = DataLoader(path_to_invalid_xml)
        data_loader.load_data()

    # THEN
    mock_logger.assert_called_once_with("Failed to parse the XML file")


@patch("loan_analysis.logging.exception")
def test_throws_if_xml_has_unexpected_structure(mock_logger: MagicMock):
    # GIVEN
    path_to_incorrectly_structured_xml = (
        Path(__file__).parent / "data" / "incorrect_structure.xml"
    )

    with pytest.raises(KeyError):
        # WHEN
        data_loader = DataLoader(path_to_incorrectly_structured_xml)
        data_loader.load_data()

    # THEN
    mock_logger.assert_called_once_with(
        "Unexpected xml structure.  Wanted child elements called 'loan' wrapped by root element of 'loans'"
    )


@patch("loan_analysis.logging.warn")
def test_rejects_records_with_invalid_data(mock_logger: MagicMock):
    # GIVEN
    path_to_xml_with_invalid_data = (
        Path(__file__).parent / "data" / "xml_with_invalid_data.xml"
    )

    # WHEN
    data_loader = DataLoader(path_to_xml_with_invalid_data)
    result = data_loader.load_data()

    # THEN
    logged_message = mock_logger.call_args_list[0][0][0]
    assert "There was a validation error at record 1/20" in logged_message
    assert len(result) == 19


@patch("loan_analysis.logging.warn")
def test_reject_record_if_date_is_not_iso_format(mock_logger: MagicMock):
    # GIVEN
    path_to_xml_with_incorrectly_formatted_date = (
        Path(__file__).parent / "data" / "xml_with_incorrectly_formatted_date.xml"
    )

    # WHEN
    data_loader = DataLoader(path_to_xml_with_incorrectly_formatted_date)
    result = data_loader.load_data()

    # THEN
    logged_message = mock_logger.call_args_list[0][0][0]
    assert "There was a validation error at record 1/20" in logged_message
    assert len(result) == 19
