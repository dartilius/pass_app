from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)

from app.models import Pass


class APIViewSet(viewsets.GenericViewSet):
    """."""

    queryset = Pass.objects.all()

    @action(detail=False, methods=['GET'])
    def get_users(self, request):
        users = User.objects.all()
        data = dict()
        for user in users:
            data.update({
                "id": user.pk,
                "full_name": user.get_full_name(),
            })
        return data

    @action(detail=False, methods=['POST'])
    def create_pass(self, request):
        try:
            name = request.data.get("name")
            worker = get_object_or_404(User, id=request.data.get("id"))
            self.queryset.create(
                name=name,
                worker=worker
            )
            return Response(status=HTTP_200_OK)
        except Http404:
            Response(
                data={"detail": "Сотрудника с таким id нет в базе"},
                status=HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                data={"detail": "Ошибка при создании заявки, попробуйте ещё раз"},
                status=HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=['GET'])
    def check_passes(self, request):
        passes = self.queryset.filter(is_approved=True, is_confirmed=None)
        if passes:
            return [{"name": _pass.client_name, "id": _pass.pk} for _pass in passes]
        else:
            return None

    @action(detail=False, methods=['GET'])
    def check_pass_status(self, request):
        _pass = self.queryset.filter(id=request.GET.get("id")).first()
        if _pass.is_approved is True:
            return Response(data={"status": "OK"}, status=HTTP_200_OK)
        elif _pass.is_approved is False:
            return Response(data={"status": "FAIL"}, status=HTTP_200_OK)
        else:
            return Response(data={"status": "WAIT"}, status=HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def choice_yes(self, request):
        pass_id = request.data.get('id')
        if not pass_id:
            return Response(
                data={'detail: Не указан айди пропуска'},
                status=HTTP_400_BAD_REQUEST
            )
        _pass = get_object_or_404(self.queryset, id=pass_id)
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
        _pass = get_object_or_404(self.queryset, id=pass_id)
        _pass.is_validated = False
        _pass.save(update_fields=['is_validated'])
        return Response(status=HTTP_200_OK)
