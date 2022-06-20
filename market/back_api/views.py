from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import mixins
from rest_framework import status
from back_api import models
from back_api import serializers

class ShopUnitGenerics(
  GenericAPIView,
  mixins.CreateModelMixin,
  mixins.DestroyModelMixin
  ):

  queryset = models.ShopUnitBase.objects.all()
  serializer_class = serializers.ShopUnitImportRequest

  def create(self, request, *args, **kwargs):
    mdata = request.data
    serializer = self.get_serializer(mdata)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ShopUnitView(APIView):

  def post(self, request):
    ser = serializers.ShopUnitImportRequest(data=request.data)
    try:
      ser.is_valid(True)
      # TODO: check and sort ser.data ShopUnits
      for item in ser.validated_data['items']:
        instance = models.ShopUnitBase.objects.filter(pk=item['id']).first()
        model_ser = serializers.ShopUnitSerializer(
          instance=instance,
          data={'date':ser.validated_data['updateDate'], **item}
        )
        if model_ser.is_valid(True):
          model_ser.save()
      return Response(status=status.HTTP_200_OK)
    except serializers.ValidationError:
      print(ser._errors)
      return Response(data=serializers.ERROR_400, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def shop_unit_delete(request, id):
  try:
    obj = models.ShopUnitBase.objects.get(id=id)
    obj.deep_delete()
    return Response(status=status.HTTP_200_OK)
  except models.ShopUnitBase.DoesNotExist:
    return Response(data=serializers.ERROR_404, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def shop_unit_nodes(request, id):
  try:
    obj = models.ShopUnitBase.objects.get(id=id)
    ser = serializers.ShopUnit(instance=obj)
    return Response(data=ser.data, status=status.HTTP_200_OK)
    # print(ser._errors)
    # return Response(data=serializers.ERROR_400, status=status.HTTP_400_BAD_REQUEST)
  except models.ShopUnitBase.DoesNotExist:
    return Response(data=serializers.ERROR_404, status=status.HTTP_404_NOT_FOUND)

# Create your views here.
