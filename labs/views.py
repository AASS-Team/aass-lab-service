from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from labs.models import Lab


class LabsList(APIView):
    """
    List all labs, or create a new lab.
    """

    serializer_class = serializers.LabSerializer

    def get(self, request, format=None):
        labs = Lab.objects.all()
        serializer = self.serializer_class(labs, many=True)

        return Response(data=serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(available=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


class LabDetail(APIView):
    """
    Retrieve, update or delete a lab instance.
    """

    def get_object(self, id):
        try:
            return Lab.objects.get(pk=id)
        except Lab.DoesNotExist:
            raise NotFound()

    def get(self, request, id, format=None):
        lab = self.get_object(id)
        serializer = serializers.LabSerializer(lab)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        lab = self.get_object(id)
        serializer = serializers.LabSerializer(lab, data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        lab = self.get_object(id)
        deleted_rows = lab.delete()

        if len(deleted_rows) <= 0:
            return Response(
                data={
                    "errors": {"global": "Nepodarilo sa vymazať laboratórium"},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
