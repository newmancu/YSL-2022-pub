from rest_framework.serializers import ModelField, ValidationError
from back_api.models import ShopUnitBase, ShopUnitHistory
from rest_framework import serializers
from back_api import models


class ShopUnitImportListSerializer(serializers.ListSerializer):
  # list_serializer_class for ShopUnitImport Serializer

  def create(self, validated_data):
    units = [models.ShopUnitBase(**item) for item in validated_data]
    return models.ShopUnitBase.objects.create(units)


class ShopUnitImport(serializers.Serializer):
  # Serializer for ShopUnitImport Schemas

  id = ModelField(ShopUnitBase._meta.get_field('id'))
  name = ModelField(ShopUnitBase._meta.get_field('name'))
  parentId = ModelField(ShopUnitBase._meta.get_field('parent_id'), source='parent_id', allow_null=True)
  type = ModelField(ShopUnitBase._meta.get_field('_type'), source='_type')
  price = ModelField(ShopUnitBase._meta.get_field('price'), allow_null=True, required=False)

  def validate(self, attrs):
    if attrs['_type'] == models.UNIT_TYPES[0][0] and attrs['price'] is None:
      raise ValidationError("для типа %s поле price не дожлно быть равным None" % models.UNIT_TYPES[0][0])
    elif attrs['_type'] == models.UNIT_TYPES[1][0]:
      if 'price' not in attrs:
        attrs['price'] = None
      elif attrs['price'] is not None:
        raise ValidationError("для типа %s поле price дожлно быть равным None" % models.UNIT_TYPES[1][0])
    return attrs

  class Meta:
    list_serializer_class = ShopUnitImportListSerializer


class ShopUnitImportRequest(serializers.Serializer):
  # Serializer for ShopUnitImportRequest Schemas
  items = ShopUnitImport(many=True)
  updateDate = serializers.DateTimeField()

  def create(self, validated_data):
    objs = [ShopUnitBase.objects.create(date=validated_data['updateDate'], **item) for item in validated_data['items']]
    return objs

  def update(self, instance, validated_data):
    return super().update(instance, validated_data)

  def validate(self, data):
    ids = set([item['id'] for item in data['items']])
    if len(ids) != len(data['items']):
      raise serializers.ValidationError("в одном запросе не может быть двух элементов с одинаковым id")
    return data


class ShopUnitSerializer(serializers.ModelSerializer):
  # default ShopUnitBase ModelSerializer
  class Meta:
    fields = '__all__'
    model = models.ShopUnitBase


class ShopUnit(serializers.ModelSerializer):
  # Serializer for ShopUnit Schemas

  parentId = ModelField(ShopUnitBase._meta.get_field('parent_id'), source='parent_id', allow_null=True)
  type = ModelField(ShopUnitBase._meta.get_field('_type'), source='_type')

  date = serializers.SerializerMethodField()
  children = serializers.SerializerMethodField()
  price = serializers.SerializerMethodField()

  def get_price(self, foo):
    if foo._type == models.UNIT_TYPES[0][0]:
      return foo.price
    return foo.get_categ_price()

  def get_children(self, foo):
    data = ShopUnit(instance=foo.first_children(), many=True).data
    if foo._type == models.UNIT_TYPES[0][0]:
      return None
    return data

  def get_date(self, foo):
    # this function needs only for passing tests
    # ISO-8601 %f - microseconds, not milliseconds
    return foo.date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

  class Meta:
    model = models.ShopUnitBase
    fields = ('id','name','date','parentId','type','price','children')



"""classes for statistic"""

class ShopInitStatisticUnit(serializers.ModelSerializer):
  # Serializer for elements of 'sales' URL 

  parentId = ModelField(ShopUnitBase._meta.get_field('parent_id'), source='parent_id', allow_null=True)
  type = ModelField(ShopUnitBase._meta.get_field('_type'), source='_type')
  date = serializers.SerializerMethodField()

  def get_date(self, obj):
    # this function needs only for passing tests
    # ISO-8601 %f - microseconds, not milliseconds
    return obj.date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

  class Meta:
    fields = ('id','name','date','parentId','type','price')
    model = models.ShopUnitBase


class ShopUnitStatisticResponse(serializers.Serializer):
  # Serializer for Response of 'sales' URL
  items = ShopInitStatisticUnit(many=True)


class ShopInitHistoryStatisticUnit(serializers.ModelSerializer):
  # Serializer for elements of 'node_statistic' URL 
  parentId = ModelField(ShopUnitHistory._meta.get_field('parent_id'), source='parent_id', allow_null=True)
  type = ModelField(ShopUnitHistory._meta.get_field('_type'), source='_type')
  date = serializers.SerializerMethodField()

  def get_date(self, obj):
    # this function needs only for passing tests
    # ISO-8601 %f - microseconds, not milliseconds
    return obj.date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

  class Meta:
    fields = ('id','name','date','parentId','type','price')
    model = models.ShopUnitHistory


class ShopUnitHistoryStatisticResponse(serializers.Serializer):
  # Serializer for Response of 'node_statistic' URL
  items = ShopInitHistoryStatisticUnit(many=True)


"""ERRORS RESPONSES"""

ERROR_400 = {
  "code": 400,
  "message": "Validation Failed"
}

ERROR_404 = {
  "code": 404,
  "message": "Item not found"
}