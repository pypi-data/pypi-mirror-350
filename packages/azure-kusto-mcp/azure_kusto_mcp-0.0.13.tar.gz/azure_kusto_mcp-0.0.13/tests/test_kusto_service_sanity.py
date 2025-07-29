import os
from pathlib import Path
from typing import Generator, List, TypedDict
from unittest.mock import MagicMock, mock_open, patch

import pytest

# Set environment variables before importing KustoService
os.environ["KUSTO_SERVICE_URI"] = "https://test.kusto.windows.net"
os.environ["KUSTO_DATABASE"] = "test_db"

from azure.kusto.data import ClientRequestProperties
from azure.kusto.data.data_format import DataFormat
from azure.kusto.ingest import IngestionProperties

from kusto_mcp.kusto_config import KustoConfig
from kusto_mcp.kusto_service import KustoService


class KustoColumn(TypedDict):
    ColumnName: str
    DataType: str


class KustoResponse(TypedDict):
    TableName: str
    Columns: List[KustoColumn]
    Rows: List[List[str]]


@pytest.fixture
def mock_kusto_response() -> MagicMock:
    """Fixture for a standard Kusto response"""
    mock_columns = [MagicMock(column_name="col1")]
    mock_primary_result = MagicMock(columns=mock_columns, rows=[["value1"]])
    mock_response = MagicMock(primary_results=[mock_primary_result])
    return mock_response


@pytest.fixture
def mock_connection() -> MagicMock:
    """Fixture for mocked KustoConnection"""
    mock_conn = MagicMock()
    mock_conn.client = MagicMock()
    mock_conn.ingestion_client = MagicMock()
    return mock_conn


@pytest.fixture
def service(mock_connection: MagicMock) -> Generator[KustoService, None, None]:
    """Fixture for KustoService with mocked connection"""
    service = KustoService(
        config=KustoConfig(
            query_service_uri="https://test.kusto.windows.net", database_name="test_db"
        )
    )
    with patch.object(service, "_conn", mock_connection):
        yield service


def test_execute_query(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test execute_query functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    result = service.execute_query("test query")

    # Verify execution
    mock_connection.client.execute.assert_called_once()
    crp_arg = mock_connection.client.execute.call_args[0][2]
    assert isinstance(crp_arg, ClientRequestProperties)
    mock_connection.client.execute.assert_called_with("test_db", "test query", crp_arg)
    assert isinstance(crp_arg.application, str)
    assert "kusto-mcp-server" in str(crp_arg.application)

    # Verify result
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == {"col1": "value1"}


def test_execute_command(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test execute_command functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    _ = service.execute_command(".show tables")

    # Verify execution
    mock_connection.client.execute.assert_called_once()
    crp_arg = mock_connection.client.execute.call_args[0][2]
    assert isinstance(crp_arg, ClientRequestProperties)
    assert not crp_arg.has_option("request_readonly") or not crp_arg.get_option(
        "request_readonly"
    )  # type: ignore


def test_print_file(service: KustoService) -> None:
    """Test print_file functionality"""
    test_content = "test content\nline2"
    with patch("builtins.open", mock_open(read_data=test_content)):
        result = service.print_file("test.txt")
        assert result == test_content

        # Test with line limit
        result = service.print_file("test.txt", lines_number=1)
        assert result == "test content\n"


def test_print_file_not_found(service: KustoService) -> None:
    """Test print_file with non-existent file"""
    with patch("builtins.open", side_effect=FileNotFoundError()):
        result = service.print_file("nonexistent.txt")
        assert "Error: File not found" in result


def test_ingest_csv_file_to_table(
    service: KustoService, mock_connection: MagicMock
) -> None:
    """Test ingest_csv_file_to_table functionality"""
    mock_result = MagicMock()
    mock_connection.ingestion_client.ingest_from_file.return_value = mock_result

    _ = service.ingest_csv_file_to_table(
        destination_table_name="test_table",
        file_abs_path="test.csv",
        ignore_first_record=True,
    )

    # Verify ingestion call
    mock_connection.ingestion_client.ingest_from_file.assert_called_once()
    file_arg = mock_connection.ingestion_client.ingest_from_file.call_args[0][0]
    props_arg = mock_connection.ingestion_client.ingest_from_file.call_args[1][
        "ingestion_properties"
    ]

    assert Path(file_arg).name == "test.csv"
    assert isinstance(props_arg, IngestionProperties)
    assert props_arg.database == "test_db"
    assert props_arg.table == "test_table"
    assert props_arg.format == DataFormat.CSV
    assert props_arg.ignore_first_record is True


def test_list_databases(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test list_databases functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    result = service.list_databases()

    mock_connection.client.execute.assert_called_once_with(
        "test_db", ".show databases", mock_connection.client.execute.call_args[0][2]
    )
    assert isinstance(result, list)


def test_list_tables(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test list_tables functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    result = service.list_tables("test_db")

    mock_connection.client.execute.assert_called_once_with(
        "test_db", ".show tables", mock_connection.client.execute.call_args[0][2]
    )
    assert isinstance(result, list)


def test_get_entities_schema(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test get_entities_schema functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    result = service.get_entities_schema()

    mock_connection.client.execute.assert_called_once()
    assert isinstance(result, list)


def test_get_table_schema(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test get_table_schema functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    result = service.get_table_schema("test_table")

    mock_connection.client.execute.assert_called_once_with(
        "test_db",
        ".show table test_table cslschema",
        mock_connection.client.execute.call_args[0][2],
    )
    assert isinstance(result, list)


def test_get_function_schema(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test get_function_schema functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    result = service.get_function_schema("test_func")

    mock_connection.client.execute.assert_called_once_with(
        "test_db",
        ".show function test_func",
        mock_connection.client.execute.call_args[0][2],
    )
    assert isinstance(result, list)


def test_sample_table_data(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test sample_table_data functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    result = service.sample_table_data("test_table", sample_size=5)

    mock_connection.client.execute.assert_called_once_with(
        "test_db",
        "test_table | sample 5",
        mock_connection.client.execute.call_args[0][2],
    )
    assert isinstance(result, list)


def test_sample_function_data(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test sample_function_data functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    result = service.sample_function_data("test_func()", sample_size=5)

    mock_connection.client.execute.assert_called_once_with(
        "test_db",
        "test_func() | sample 5",
        mock_connection.client.execute.call_args[0][2],
    )
    assert isinstance(result, list)


def test_ingest_inline_into_table(
    service: KustoService, mock_connection: MagicMock, mock_kusto_response: MagicMock
) -> None:
    """Test ingest_inline_into_table functionality"""
    mock_connection.client.execute.return_value = mock_kusto_response

    result = service.ingest_inline_into_table("test_table", "value1,value2")

    mock_connection.client.execute.assert_called_once_with(
        "test_db",
        ".ingest inline into table test_table <| value1,value2",
        mock_connection.client.execute.call_args[0][2],
    )
    assert isinstance(result, list)
