from typing import Iterable, Optional
from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4
# mb pattern?

UNIT_TYPES = (
  ('OFFER', 'OFFER'),
  ('CATEGORY', 'CATEGORY')
)


class MyMinValueValidator(MinValueValidator):
  def compare(self, a, b) -> bool:
    if a is None or b is None:
      return True
    return super().compare(a, b)

  
class ShopUnitBase(models.Model):
  id = models.UUIDField(
    primary_key=True,
    default=uuid4
  )

  name = models.CharField(
    max_length=256
  )

  date = models.DateTimeField(
    
  )

  price = models.BigIntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(0)]
  )

  parent_id = models.ForeignKey(
    'back_api.ShopUnitBase',
    on_delete=models.CASCADE,
    null=True,
    blank=True
  )

  _type = models.CharField(
    max_length=16,
    choices=UNIT_TYPES
  )

  def __repr__(self) -> str:
    return f"{self.name} ({self.id})"

  def __str__(self) -> str:
    return self.__repr__()


  def children(self):
    # useless method
    if self._type == UNIT_TYPES[0][0]:
      return None
    r = list()
    for c in ShopUnitBase.objects.filter(parent_id=self):
      _r = c.children()
      r.append(_r)
    return r

  def first_children(self):
    if self._type == UNIT_TYPES[0][0]:
      return None
    r = [c for c in ShopUnitBase.objects.filter(parent_id=self)]
    return r

  def get_categ_price(self):
    # simple, but slow function for calculation avg categ price
    if self._type == UNIT_TYPES[0][0]:
      return self.price
    sum = 0
    count = 0
    l = [i for i in ShopUnitBase.objects.filter(parent_id=self)]
    while l:
      c = l.pop(0)
      if c._type == UNIT_TYPES[0][0]:
        sum += c.price
        count += 1
      else:
        l += [i for i in ShopUnitBase.objects.filter(parent_id=c)]
    if not count:
      return None
    return sum//count
    
  def __add_to_history(self):
    # saving history of updates
    data = {field.name:getattr(self,field.name) for field in self._meta.fields}
    if data['parent_id'] is not None:
      data['parent_id'] = data['parent_id'].id
    ShopUnitHistory.objects.create(**data)

  def deep_delete(self):
    self.__add_to_history()
    self.delete()

  def save(self, *args, **kwargs):
    self.__add_to_history()
    if self.parent_id is not None:
      c = ShopUnitBase.objects.get(id=self.parent_id.id)
      c.date = self.date
      c.save()
    return super(ShopUnitBase, self).save(*args, **kwargs)


class ShopUnitHistory(models.Model):
  row_pk = models.BigAutoField(
    primary_key=True
  )

  id = models.UUIDField(
    default=uuid4
  )

  name = models.CharField(
    max_length=256
  )

  date = models.DateTimeField(
    
  )

  price = models.BigIntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(0)]
  )

  parent_id = models.UUIDField(
    null=True,
    blank=True
  )

  _type = models.CharField(
    max_length=16,
    choices=UNIT_TYPES
  )

  def is_deleted(self):
    return ShopUnitBase.objects.filter(id=self.id).first() is None

  
  def __repr__(self) -> str:
    return f"{self.name} ({self.id})"

  def __str__(self) -> str:
    return self.__repr__()