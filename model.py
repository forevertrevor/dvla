from datetime import date

from pydantic import BaseModel


class Loan(BaseModel):
    id: str
    member_id: str
    member_name: str
    branch: str
    title: str
    genre: str
    # date type is automatically validated for iso format in pydantic
    loan_date: date
    due_date: date
    returned_date: date | None

    def report_loan(self, show_due_date: bool = False):
        output_fields = [self.id, self.title, self.member_name, self.branch]
        if show_due_date:
            output_fields.append(self.due_date.isoformat())
        print(" | ".join(output_fields))
