from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK, HTTP_201_CREATED
)

from app.models import Pass, Worker
from app.serializers import PassSerializer


class APIViewSet(viewsets.GenericViewSet):
    """API."""

    queryset = Pass.objects.all()
    serializer_class = PassSerializer

    @action(detail=False, methods=['GET'])
    def get_users(self, request):
        users = Worker.objects.all()
        data = list()
        for user in users:
            data.append({
                "id": user.pk,
                "full_name": user.name,
            })
        return Response(data)

    @action(detail=False, methods=['POST'])
    def create_pass(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            name = serializer.data.get("name")
            worker_id = serializer.data.get("worker")
            worker = Worker.objects.get(id=worker_id)
            _pass = Pass.objects.create(
                name=name,
                worker=worker
            )
            return Response(data={"id": _pass.pk}, status=HTTP_201_CREATED)
        except Worker.DoesNotExist:
            return Response(
                data={"detail": "Сотрудника с таким id нет в базе"},
                status=HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data={"detail": "Ошибка при создании заявки, попробуйте ещё раз"},
                status=HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=['GET'])
    def check_passes(self, request):
        passes = Pass.objects.filter(is_approved=True, is_validated=None)
        if passes:
            return Response([{"name": _pass.name, "id": _pass.pk} for _pass in passes])
        else:
            return Response({})

    @action(detail=False, methods=['GET'])
    def check_worker_approval(self, request):
        _pass = Pass.objects.filter(id=request.GET.get("id")).first()
        if _pass.is_approved is True:
            return Response(status=HTTP_201_CREATED)
        elif _pass.is_approved is False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def check_security_approval(self, request):
        _pass = Pass.objects.filter(id=request.GET.get("id")).first()
        if _pass.is_validated is True:
            return Response(status=HTTP_201_CREATED)
        elif _pass.is_validated is False:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def choice_yes(self, request):
        pass_id = request.data.get('id')
        if not pass_id:
            return Response(
                data={'detail: Не указан айди пропуска'},
                status=HTTP_400_BAD_REQUEST
            )
        _pass = get_object_or_404(Pass, id=pass_id)
        _pass.is_validated = True
        _pass.save(update_fields=['is_validated'])
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def choice_no(self, request):
        pass_id = request.data.get('id')
        if not pass_id:
            return Response(
                data={'detail: Не указан айди пропуска'},
                status=HTTP_400_BAD_REQUEST
            )
        _pass = get_object_or_404(Pass, id=pass_id)
        _pass.is_validated = False
        _pass.save(update_fields=['is_validated'])
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def approve(self, request):
        pass_id = request.data.get('id')
        if not pass_id:
            return Response(
                data={'detail: Не указан айди пропуска'},
                status=HTTP_400_BAD_REQUEST
            )
        _pass = get_object_or_404(Pass, id=pass_id)
        _pass.is_approved = True
        _pass.save(update_fields=['is_approved'])
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def decline(self, request):
        pass_id = request.data.get('id')
        if not pass_id:
            return Response(
                data={'detail: Не указан айди пропуска'},
                status=HTTP_400_BAD_REQUEST
            )
        _pass = get_object_or_404(Pass, id=pass_id)
        _pass.is_approved = False
        _pass.save(update_fields=['is_approved'])
        return Response(status=HTTP_200_OK)