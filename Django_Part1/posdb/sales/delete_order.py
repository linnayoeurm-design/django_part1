#python manage.py shell
from sales.models import Order
Order.objects.all().delete()