from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from back_api.serializers import *
from back_api import views
import json
import datetime


class SerializerTest1(TestCase):
  def setUp(self) -> None:
    self.exs = json.loads('{ "id": "3fa85f64-5717-4562-b3fc-2c963f66a444", "name": "Оффер", "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a333", "price": 234, "type": "OFFER" }')
    self.exsl = [self.exs] * 2
    self.req = {'items': self.exsl, 'updateDate': datetime.datetime.now().isoformat()}
    self.req = {'items': [self.exs], 'updateDate': datetime.datetime.now().isoformat()}

  def test_exs(self):
    a = ShopUnitImport(self.exs)
    b = ShopUnitImport(self.exsl)
    c = ShopUnitImportRequest(data=self.req)
    # print(c.is_valid())
    # print(c._errors)
    # print(c)
    # print(a)
    # print(b)


class ViewsTest1(APITestCase):

  def test_imports(self):
    exs = json.loads('{ "id": "3fa85f64-5717-4562-b3fc-2c963f66a444", "name": "Оффер", "parentId": null, "price": 234, "type": "OFFER" }')

    mdata = {
      'items': [exs],
      'updateDate': datetime.datetime.now().isoformat()
    }
    url = reverse('includes')
    res = self.client.post(url, data=mdata, format='json')
    print(res)
