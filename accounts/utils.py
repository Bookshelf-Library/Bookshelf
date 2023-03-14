import pytz
from rest_framework.views import Response, status


def permission_to_loan(account_id, Loan=None, current_date=None):
    if Loan is None:
        from copies.models import Loan

        Loan = Loan

    if current_date is None:
        from datetime import datetime

        current_date = datetime.now()

    loans = Loan.objects.filter(account_id=account_id, is_active=True)

    utc = pytz.UTC
    expires_on = current_date.replace(tzinfo=utc)

    for loan in loans:
        if loan.delivery_at is None and expires_on > loan.deliver_in:
            return False

    return True


def openingtime(day, hour):
    time = int(hour)
    if day == "Saturday" or day == "Sunday":
        return False
    if time > 18 or time < 9:
        return False
    return True
