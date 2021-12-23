from main.models import Operation
from datetime import datetime
from datetime import date
from datetime import timedelta


def test(days:int):
    d = datetime.now().date() - timedelta(days=days)
    a = Operation.objects.filter(created_at__date__gte=d).all()
    return a