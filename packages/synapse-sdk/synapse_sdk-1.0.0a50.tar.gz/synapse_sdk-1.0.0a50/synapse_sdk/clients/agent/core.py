from synapse_sdk.clients.base import BaseClient


class CoreClientMixin(BaseClient):
    def health_check(self):
        path = 'health/'
        return self._get(path)

    def get_metrics(self, panel):
        path = f'metrics/{panel}/'
        return self._get(path)
