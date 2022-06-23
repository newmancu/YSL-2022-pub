from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import timedelta
from back_api import models
from back_api import serializers
from back_api.converters import DateTimeConverter


class LeveldDict:
  # additional structure for '/imports'
  # there are right ordered items of ShopUnitBase in self.flatten
  def __init__(self, imports) -> None:
    self.tree = dict()
    self.ptree = dict()
    self.flatten = [] 
    for item in imports:
      iid = item['id'] 
      pid = item['parent_id']
      
      if iid in self.tree:
        raise serializers.ValidationError('uuid dublication')
      self.tree[iid] = item
      if pid not in self.ptree:
        self.ptree[pid] = set()
      self.ptree[pid].add(iid)

    for key in self.tree:
      tpc = self.tree[key]['parent_id']
      if tpc not in self.tree:
        self.__calc_lvl(key)
      elif self.tree[tpc]['_type'] != models.UNIT_TYPES[1][0]:
        raise serializers.ValidationError('%s as parent' % models.UNIT_TYPES[1][0])

  def __calc_lvl(self, root_id):
    queue = [(root_id, 0)]

    while queue:
      cur = queue.pop(0)
      
      dd = cur[1] + 1- len(self.flatten)
      if dd > 0:
        self.flatten += [list() for i in range(dd)] 
      self.flatten[cur[1]].append(self.tree[cur[0]])
      if cur[0] in self.ptree:
        queue += list(map(lambda x: (x, cur[1]+1), self.ptree[cur[0]]))


class ShopUnitView(APIView):
  # Class based view for '/imports'
  def post(self, request):
    ser = serializers.ShopUnitImportRequest(data=request.data)
    to_save = []
    try:
      ser.is_valid(True)
      valid, validated_data = self._validate_imports(ser.validated_data['items'])
      if not valid:
        raise serializers.ValidationError()
      for validation_level in validated_data:
        for item in validation_level:
          instance = models.ShopUnitBase.objects.filter(pk=item['id']).first()
          model_ser = serializers.ShopUnitSerializer(
            instance=instance,
            data={'date':ser.validated_data['updateDate'], **item}
          )
          if model_ser.is_valid(True):
            if (instance is not None and instance._type != model_ser.validated_data['_type']):
              raise serializers.ValidationError()
            to_save.append(model_ser)
      for it in to_save:
        it.save()
      return Response(status=status.HTTP_200_OK)
    except serializers.ValidationError:
      return Response(data=serializers.ERROR_400, status=status.HTTP_400_BAD_REQUEST)

  def _validate_imports(self, imports):
    # Check imports and sort imports
    pc_set = self.__sort_imports(imports)
    if len(pc_set[0]) <= 0:
      return False, {}
    for items in pc_set[0]:
      pc = models.ShopUnitBase.objects.filter(pk=items['parent_id']).first()
      if items['parent_id'] is not None and \
        (pc is None or pc._type != models.UNIT_TYPES[1][0]):
        return False, {}
    return True, pc_set

  def __sort_imports(self, imports):
    pc_set = LeveldDict(imports)
    return pc_set.flatten

@api_view(['DELETE'])
def shop_unit_delete(request, id):
  # function based view for '/delete/'
  try:
    obj = models.ShopUnitBase.objects.get(id=id)
    obj.deep_delete()
    return Response(status=status.HTTP_200_OK)
  except models.ShopUnitBase.DoesNotExist:
    return Response(data=serializers.ERROR_404, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def shop_unit_nodes(request, id):
  # function based view for '/nodes/'
  try:
    obj = models.ShopUnitBase.objects.get(id=id)
    ser = serializers.ShopUnit(instance=obj)
    return Response(data=ser.data, status=status.HTTP_200_OK)
  except models.ShopUnitBase.DoesNotExist:
    return Response(data=serializers.ERROR_404, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def shop_unit_sales(request):
  # function based view for '/sales/'
  try:
    date = DateTimeConverter().to_python(request.GET.get('date'))
    objs = models.ShopUnitBase.objects.filter(
      date__gte=date - timedelta(days=1), 
      date__lte=date,
      _type=models.UNIT_TYPES[0][0]
    )
    ser = serializers.ShopUnitStatisticResponse(instance={'items': objs})
    return Response(data=ser.data, status=status.HTTP_200_OK)
  except ValueError:
    return Response(data=serializers.ERROR_400, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def shop_unit_node_statistic(request, id):
  # function based view for '/node/<uuid:id>/statistic'
  try:
    dtconverter = DateTimeConverter()
    dateStart = dtconverter.to_python(request.GET.get('dateStart'))
    dateEnd = dtconverter.to_python(request.GET.get('dateEnd'))
    
    if dateEnd <= dateStart:
      return Response(data=serializers.ERROR_400, status=status.HTTP_400_BAD_REQUEST)

    query = models.ShopUnitHistory.objects.filter(id=id)
    f_query = query.first()
    if f_query is None or f_query.is_deleted():
      return Response(data=serializers.ERROR_404, status=status.HTTP_404_NOT_FOUND)
    objs = query.filter(
      date__gte=dateStart,
      date__lt=dateEnd
    )
    ser = serializers.ShopUnitHistoryStatisticResponse(instance={'items': objs})

    return Response(data=ser.data, status=status.HTTP_200_OK)
  except Exception as exp:
    return Response(data=serializers.ERROR_400, status=status.HTTP_400_BAD_REQUEST)
