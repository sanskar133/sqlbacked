table_and_descriptions = {
    "loan_payments": "This table contains loan payment records for individual borrowers. The table is unique at the Loan ID level and includes details about the borrower's demographics, loan principal, interest rates, payment history, and overdue details. It provides insights into loan repayment trends, borrower behavior, and financial risk assessment. Key attributes include borrower information (age, education, gender, etc.), loan details (principal amount, interest rate, due date, etc.), and repayment status (whether the loan is paid off, in collection, or overdue)."
}

table_to_column_mapping = {
    "loan_payments": {
        "Loan_ID": {
            "description": "A unique alphanumeric identifier assigned to each loan. This ID helps track individual loan records across different processing stages.",
            "values_sample": ["xqd20166231", "xqd20160013"],
        },
        "loan_status": {
            "description": "Represents the current state of the loan. Possible values include 'PAIDOFF' (fully repaid), 'COLLECTION' (overdue and in collection phase).",
            "values_sample": ["PAIDOFF", "COLLECTION", "COLLECTION_PAIDOFF"],
        },
        "Principal": {
            "description": "The total amount borrowed by the customer when the loan was issued. This forms the basis for interest calculation.",
            "values_sample": [1000, 800],
        },
        "terms": {
            "description": "The number of days for which the loan is issued. Common values are 7, 15, or 30 days.",
            "values_sample": [7, 15, 30],
        },
        "effective_date": {
            "description": "The official start date of the loan agreement, used to calculate the due date and interest accrual.",
            "values_sample": ["9/8/2016", "9/12/2016"],
        },
        "due_date": {
            "description": "The date by which the loan must be fully repaid to avoid penalties or collection status.",
            "values_sample": ["10/7/2016", "10/9/2016"],
        },
        "paid_off_time": {
            "description": "The exact timestamp when the loan was fully repaid, including principal and accrued interest. If empty, the loan is not paid off.",
            "values_sample": ["9/14/2016 19:31", "9/24/2016 16:00"],
        },
        "past_due_days": {
            "description": "The number of days the loan payment was overdue beyond the due date. NULL if paid on time.",
            "values_sample": [None, 60, 75],
        },
        "age": {
            "description": "The borrower's age at the time of loan application, used in risk assessment models.",
            "values_sample": [28, 35, 45],
        },
        "education": {
            "description": "The highest educational qualification of the borrower, categorized as 'High School or Below', 'Bachelor', or 'College'.",
            "values_sample": ["High School or Below", "College", "Bachelor"],
        },
        "Gender": {
            "description": "The gender of the borrower, categorized as 'male' or 'female', used for demographic analysis.",
            "values_sample": ["male", "female"],
        },
    }
}
