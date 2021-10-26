from pydantic import BaseModel

class BankNote(BaseModel):
    gender :str
    married :str
    dependents : str
    education : str
    employeed :str
    credithistory :str
    propertyarea :str
    applicantincome :float
    coapplicantIncome :float
    LoanAmount :float