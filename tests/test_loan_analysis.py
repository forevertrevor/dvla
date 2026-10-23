from datetime import date


from loan_analysis import LoanAnalyzer, DataLoader


def test_loans_on_specific_date():

    # GIVEN
    data = DataLoader().load_data()
    date_to_analyse = date(2026, 4, 21)
    loan_analyzer = LoanAnalyzer(data)

    # WHEN
    results = loan_analyzer.get_books_out_on_loan_for_date(date_to_analyse)

    # THEN
    assert len(results) == 6

    expected_result_ids = {"L002", "L003", "L004", "L005", "L006", "L007"}
    actual_result_ids = [loan.id for loan in results]

    assert expected_result_ids == set(actual_result_ids)


def test_loans_that_are_overdue():

    # GIVEN
    data = DataLoader().load_data()
    loan_analyzer = LoanAnalyzer(data)

    # WHEN
    results = loan_analyzer.get_overdue_books()

    # THEN
    assert len(results) == 10


def test_group_loan_count_by_branch():
    # GIVEN
    data = DataLoader().load_data()
    loan_analyzer = LoanAnalyzer(data)

    # WHEN
    results = loan_analyzer.group_loans_by_branch()

    # THEN
    assert results["Central"] == 8
    assert results["Riverside"] == 7
    assert results["Hillside"] == 5
