import itertools
import logging
from datetime import date
from pathlib import Path
from typing import List, Dict, Any

import xmltodict
from pydantic import ValidationError

import model

PATH_TO_DATA_FILE = Path(__file__).parent / "data" / "coding-part1.xml"


def is_out_on_loan(loan: model.Loan, date_to_analyse: date):
    return loan.loan_date <= date_to_analyse and (
        loan.returned_date is None or loan.returned_date > date_to_analyse
    )


def read_data_from_file(_path_to_data_file: Path) -> Any | None:
    try:
        with open(_path_to_data_file) as file:
            xml = file.read()
        xml_data_as_dict = xmltodict.parse(xml, attr_prefix="")
        return xml_data_as_dict["loans"]["loan"]
    except OSError:
        logging.exception("Could not load file from path provided")
        raise
    except KeyError:
        logging.exception(
            "Unexpected xml structure.  Wanted child elements called 'loan' wrapped by root element of 'loans'"
        )
        raise
    except Exception:
        logging.exception(f"Failed to parse the XML file")
        raise


class DataLoader:

    def __init__(self, path_to_data_file: Path = PATH_TO_DATA_FILE):
        self._path_to_data_file = path_to_data_file

    def load_data(self) -> List[model.Loan]:
        loans_as_dict = read_data_from_file(self._path_to_data_file)

        result = []

        for idx, item in enumerate(loans_as_dict):
            try:
                result.append(model.Loan.model_validate(item))
            except ValidationError as validation_error:
                logging.warn(
                    f"There was a validation error at record {idx + 1}/{len(loans_as_dict)}: {validation_error}"
                )
        logging.info(f"Successfully loaded {len(result)} records.")
        return result


class LoanAnalyzer:

    def __init__(self, loan_data: List[model.Loan]):
        self._all_loans = loan_data

    @property
    def all_loans(self):
        return self._all_loans

    def get_books_out_on_loan_for_date(self, date_to_analyse: date) -> List[model.Loan]:
        return [
            loan for loan in self._all_loans if is_out_on_loan(loan, date_to_analyse)
        ]

    def get_overdue_books(self) -> List[model.Loan]:
        return [loan for loan in self._all_loans if not loan.returned_date]

    def group_loans_by_branch(self) -> Dict[str, int]:
        result: Dict[str, int] = {}
        for loan in self._all_loans:
            if count := result.get(loan.branch):
                result[loan.branch] = count + 1
            else:
                result[loan.branch] = 1
        return result

    def group_loans_by_branch_alternative_approach(
        self,
    ) -> Dict[str, int]:
        result: Dict[str, int] = {}
        sorted_loans = sorted(self._all_loans, key=lambda loan: loan.branch)
        for k, g in itertools.groupby(sorted_loans, lambda loan: loan.branch):
            result[k] = len(list(g))
        return result

    def report_books_on_loan_for_date(self, date_to_analyse: date):
        loans = self.get_books_out_on_loan_for_date(date_to_analyse)
        for loan in loans:
            loan.report_loan()

    def report_overdue_books(self):
        overdue_loans = self.get_overdue_books()
        for loan in overdue_loans:
            loan.report_loan(show_due_date=True)

    def report_loans_by_branch(self, sort_asc: bool = True):
        kv_list = self.group_loans_by_branch().items()
        sorted_by_count = sorted(kv_list, key=lambda x: x[1], reverse=not sort_asc)
        for record in sorted_by_count:
            branch, count = record
            print(f"{branch} | {count}")
