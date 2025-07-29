from azure.identity import ChainedTokenCredential, DefaultAzureCredential
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.ingest import KustoStreamingIngestClient

from kusto_mcp.kusto_config import KustoConfig


class KustoConnection:
    config: KustoConfig
    _client: KustoClient
    _ingestion_client: KustoStreamingIngestClient

    def __init__(self, config: KustoConfig):
        self.config = config
        self._client = self._create_client()
        self._ingestion_client = self._create_ingestion_client()

    def _get_credential(self) -> ChainedTokenCredential:
        return DefaultAzureCredential(
            exclude_shared_token_cache_credential=True,
            exclude_interactive_browser_credential=False,
        )

    def _create_client(self) -> KustoClient:
        credential = self._get_credential()

        kcsb = KustoConnectionStringBuilder.with_azure_token_credential(
            connection_string=self.config.query_service_uri, credential=credential
        )

        return KustoClient(kcsb)

    def _create_ingestion_client(self) -> KustoStreamingIngestClient:
        credential = self._get_credential()
        kcsb = KustoConnectionStringBuilder.with_azure_token_credential(
            connection_string=self.config.query_service_uri, credential=credential
        )
        return KustoStreamingIngestClient(kcsb)

    @property
    def client(self) -> KustoClient:
        return self._client

    @property
    def ingestion_client(self) -> KustoStreamingIngestClient:
        return self._ingestion_client
