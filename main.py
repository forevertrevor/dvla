from typing import List

import model
from loan_analysis import LoanAnalyzer, DataLoader
from datetime import date

if __name__ == "__main__":
    # Feature 1. load and parse records
    data_loader = DataLoader()
    data: List[model.Loan] = data_loader.load_data()

    # Feature 2. list books on loan for a given date
    loan_analyzer = LoanAnalyzer(data)
    loan_analyzer.report_books_on_loan_for_date(date(2026, 4, 21))

    # Feature 3. report overdue books
    loan_analyzer.report_overdue_books()

    # Feature 4. report loans by branch
    loan_analyzer.report_loans_by_branch(sort_asc=False)
