from synapse_sdk.clients.backend.annotation import AnnotationClientMixin
from synapse_sdk.clients.backend.core import CoreClientMixin
from synapse_sdk.clients.backend.dataset import DatasetClientMixin
from synapse_sdk.clients.backend.hitl import HITLClientMixin
from synapse_sdk.clients.backend.integration import IntegrationClientMixin
from synapse_sdk.clients.backend.ml import MLClientMixin


class BackendClient(
    AnnotationClientMixin,
    CoreClientMixin,
    DatasetClientMixin,
    IntegrationClientMixin,
    MLClientMixin,
    HITLClientMixin,
):
    name = 'Backend'
    token = None
    tenant = None
    agent_token = None

    def __init__(self, base_url, token=None, tenant=None, agent_token=None):
        super().__init__(base_url)
        self.token = token
        self.tenant = tenant
        self.agent_token = agent_token

    def _get_headers(self):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        if self.tenant:
            headers['SYNAPSE-Tenant'] = f'Token {self.tenant}'
        if self.agent_token:
            headers['SYNAPSE-Agent'] = f'Token {self.agent_token}'
        return headers
