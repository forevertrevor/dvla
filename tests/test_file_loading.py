from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from pydantic import ValidationError

import loan_analysis
from loan_analysis import LoanAnalyzer


def test_loads_xml_as_loans_object():
    # WHEN
    loan_analyzer = LoanAnalyzer()

    # THEN
    assert len(loan_analyzer.all_loans) == 20


@patch("loan_analysis.logging.exception")
def test_throws_if_invalid_path_is_provided(mock_logger: MagicMock):
    # GIVEN
    path_to_non_existent_file = Path(__file__).parent / "nowhere" / "invalid_xml.xml"

    with pytest.raises(OSError):
        # WHEN
        loan_analysis.read_data_from_file(path_to_non_existent_file)

    # THEN
    mock_logger.assert_called_once_with("Could not load file from path provided")


@patch("loan_analysis.logging.exception")
def test_throws_if_xml_is_invalid(mock_logger: MagicMock):
    # GIVEN
    path_to_invalid_xml = Path(__file__).parent / "data" / "invalid_xml.xml"

    with pytest.raises(Exception):
        # WHEN
        loan_analysis.read_data_from_file(path_to_invalid_xml)

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
        loan_analysis.read_data_from_file(path_to_incorrectly_structured_xml)

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
    loan_analyzer = LoanAnalyzer(path_to_xml_with_invalid_data)

    # THEN
    logged_message = mock_logger.call_args_list[0][0][0]
    assert "There was a validation error at record 1/20" in logged_message
    assert len(loan_analyzer.all_loans) == 19


@patch("loan_analysis.logging.warn")
def test_reject_record_if_date_is_not_iso_format(mock_logger: MagicMock):
    # GIVEN
    path_to_xml_with_incorrectly_formatted_date = (
        Path(__file__).parent / "data" / "xml_with_incorrectly_formatted_date.xml"
    )

    # WHEN
    loan_analyzer = LoanAnalyzer(path_to_xml_with_incorrectly_formatted_date)

    # THEN
    logged_message = mock_logger.call_args_list[0][0][0]
    assert "There was a validation error at record 1/20" in logged_message
    assert len(loan_analyzer.all_loans) == 19
