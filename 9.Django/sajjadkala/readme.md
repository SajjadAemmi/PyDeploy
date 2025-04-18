# Django online shop



### Django Fixture

Create a Fixture

```bash
python manage.py dumpdata shop product --indent 2 > db.json  
```

Create a Fixture for persian character problem

```bash
python manage.py shell -c "from django.core.serializers import serialize; from shop.models import Product; open('my_data.json', 'w', encoding='utf-8').write(serialize('json', Product.objects.all(), indent=2))"
```

Load a Fixture into the Database

```bash
python manage.py loaddata my_data.json
```
