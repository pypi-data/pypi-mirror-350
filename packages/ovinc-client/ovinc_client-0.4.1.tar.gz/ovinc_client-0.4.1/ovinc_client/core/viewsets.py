import abc

from rest_framework.viewsets import GenericViewSet

from ovinc_client.core.cache import CacheMixin


class MainViewSet(CacheMixin, GenericViewSet):
    """
    Base ViewSet
    """

    ...


class CreateMixin(abc.ABC):
    @abc.abstractmethod
    def create(self, request, *args, **kwargs):
        raise NotImplementedError()


class ListMixin(abc.ABC):
    @abc.abstractmethod
    def list(self, request, *args, **kwargs):
        raise NotImplementedError()


class RetrieveMixin(abc.ABC):
    @abc.abstractmethod
    def retrieve(self, request, *args, **kwargs):
        raise NotImplementedError()


class UpdateMixin(abc.ABC):
    @abc.abstractmethod
    def update(self, request, *args, **kwargs):
        raise NotImplementedError()


class DestroyMixin(abc.ABC):
    @abc.abstractmethod
    def destroy(self, request, *args, **kwargs):
        raise NotImplementedError()
