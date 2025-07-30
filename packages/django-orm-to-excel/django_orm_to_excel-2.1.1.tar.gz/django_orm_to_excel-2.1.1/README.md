# django-orm-to-excel

A small library for turning Django ORM objects (such as records or QuerySet) into an Excel spreadsheet.

### Example:

```python
from django_orm_to_excel import save_to_excel

# querysets
profiles = Profile.objects.all()

with open("queryset_dump.xlsx", "w") as file:
    save_to_excel(file, profiles, fields=["name", "age"])

# records
profile = profiles.first()

with open("record_dump.xlsx", "w") as file:
    save_to_excel(file, profile, fields=["name", "age"])
```
