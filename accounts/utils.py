import pytz


def permission_to_loan(account_id, Loan, current_date):
    loans = Loan.objects.filter(account_id=account_id, is_active=True)

    utc = pytz.UTC
    expires_on = current_date.replace(tzinfo=utc)

    for loan in loans:
        if loan.delivery_at is None and expires_on > loan.deliver_in:
            return False

    return True
