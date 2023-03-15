import pytz


def permission_to_loan(account_id, Loan=None, current_date=None, punishment=None):
    if punishment:
        return False

    if Loan is None:
        from copies.models import Loan

        Loan = Loan

    if current_date is None:
        from datetime import datetime

        current_date = datetime.now()

    loans = Loan.objects.filter(account_id=account_id, is_active=True)

    utc = pytz.UTC
    expires_date = current_date.replace(tzinfo=utc)

    for loan in loans:
        if loan.delivery_at is None and expires_date > loan.deliver_in:
            return False

    return True


def openingtime(day, hour):
    time = int(hour)
    if day == "Saturday" or day == "Sunday":
        return False
    if time > 18 or time < 9:
        return False
    return True


def remove_punishment(*args):
    account_punished = args[0]
    account_punished.punishment = None
    account_punished.save()
