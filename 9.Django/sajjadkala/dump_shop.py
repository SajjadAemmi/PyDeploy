from django.core.serializers import serialize
from shop.models import Product

with open("db.json", "w", encoding="utf-8") as f:
    f.write(serialize("json", Product.objects.all(), indent=2))
