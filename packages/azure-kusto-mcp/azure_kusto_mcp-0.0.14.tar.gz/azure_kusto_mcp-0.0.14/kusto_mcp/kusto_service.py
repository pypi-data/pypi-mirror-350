import inspect
import os
import uuid
from itertools import islice
from typing import Any, Dict, List, Optional, cast

from azure.kusto.data import ClientRequestProperties
from azure.kusto.data.data_format import DataFormat
from azure.kusto.ingest import IngestionProperties, IngestionResult
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from kusto_mcp.kusto_config import KustoConfig
from kusto_mcp.kusto_connection import KustoConnection
from kusto_mcp.kusto_response_formatter import format_results

from . import __version__  # type: ignore

# MCP server
mcp = FastMCP("kusto-mcp-server")


class KustoService:
    _conn: Optional[KustoConnection] = None
    DESTRUCTIVE_TOOLS = {
        "execute_command",
        "ingest_inline_into_table",
        "ingest_csv_file_to_table",
    }

    def __init__(self, config: KustoConfig):
        self.config = config

    @property
    def conn(self) -> KustoConnection:
        if self._conn is None:
            self._conn = KustoConnection(self.config)
        return self._conn

    def execute_query(
        self, query: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes a KQL query on the specified database. If no database is provided,
        it will use the database name from the config or the default database.

        :param query: The KQL query to execute.
        :param database: The name of the database to execute the query on. If not provided,
                        it will use the database name from the config or the default database.
        :return: The result of the query execution as a list of dictionaries (json).
        """
        return self._execute(query, database=database)

    def execute_command(
        self, command: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes a kusto management command on the specified database. If no database is provided,
        it will use the database name from the config or the default database.

        :param command: The kusto management command to execute.
        :param database: The name of the database to execute the command on. If not provided,
                        it will use the database name from the config or the default database.
        :return: The result of the command execution as a list of dictionaries (json).
        """
        return self._execute(command, database=database)

    def print_file(self, file_abs_path: str, lines_number: int = -1) -> str:
        """
        Reads content from a file at the specified absolute path. Can read either the entire file
        or a specified number of lines from the beginning.

        :param file_abs_path: The absolute path to the file to read.
        :param lines_number: Number of lines to read from the start of the file. Use -1 to read entire file.
        :return: The content of the file as a string.
        """
        try:
            if lines_number == -1:
                with open(file_abs_path, "r") as f:
                    return f.read()

            with open(file_abs_path) as input_file:
                return "".join(islice(input_file, lines_number))
        except FileNotFoundError:
            return f"Error: File not found: {file_abs_path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def ingest_csv_file_to_table(
        self,
        destination_table_name: str,
        file_abs_path: str,
        ignore_first_record: bool,
        database: Optional[str] = None,
    ) -> IngestionResult:
        """
        Ingests a CSV file into a specified table. If the table doesn't exist, creates it based on
        the CSV headers. If no database is provided, uses the config database.

        :param destination_table_name: Name of the table to ingest data into.
        :param file_abs_path: Absolute path to the CSV file to ingest.
        :param ignore_first_record: Whether to ignore the first record (header row) during ingestion.
        :param database: The target database name. If not provided, uses the config database.
        :return: The IngestionResult containing details about the ingestion operation.
        """
        database = database or self.config.database_name
        if not database:
            raise ValueError(
                "Database name must be provided either in the config or as an argument."
            )
        ingest_client = self.conn.ingestion_client
        ingestion_properties = IngestionProperties(
            database=database,
            table=destination_table_name,
            data_format=DataFormat.CSV,
            ignore_first_record=ignore_first_record,
        )

        # ingest from file
        file_abs_path = os.path.normpath(file_abs_path)
        self._run_clear_streamingingestion_schema()
        return ingest_client.ingest_from_file(
            file_abs_path, ingestion_properties=ingestion_properties
        )

    def list_databases(self) -> List[Dict[str, Any]]:
        """
        Retrieves a list of all databases in the Kusto cluster.

        :return: List of dictionaries containing database information.
        """
        return self._execute(".show databases")

    def list_tables(self, database: str) -> List[Dict[str, Any]]:
        """
        Retrieves a list of all tables in the specified database.

        :param database: The name of the database to list tables from.
        :return: List of dictionaries containing table information.
        """
        return self._execute(".show tables", database=database)

    def get_entities_schema(
        self, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves schema information for all entities (tables, materialized views, functions)
        in the specified database. If no database is provided, uses the config database.

        :param database: Optional database name. If not provided, uses the config database.
        :return: List of dictionaries containing entity schema information.
        """
        return self._execute(
            f"""
            .show databases entities with (showObfuscatedStrings=true)
            | where DatabaseName == '{database or self.config.database_name}'
            | project EntityName, EntityType, Folder, DocString
        """
        )

    def get_table_schema(
        self, table_name: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves the schema information for a specific table in the specified database.
        If no database is provided, uses the config database.

        :param table_name: Name of the table to get schema for.
        :param database: Optional database name. If not provided, uses the config database.
        :return: List of dictionaries containing table schema information.
        """
        return self._execute(f".show table {table_name} cslschema", database=database)

    def get_function_schema(
        self, function_name: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves schema information for a specific function, including parameters and output schema.
        If no database is provided, uses the config database.

        :param function_name: Name of the function to get schema for.
        :param database: Optional database name. If not provided, uses the config database.
        :return: List of dictionaries containing function schema information.
        """
        return self._execute(f".show function {function_name}", database=database)

    def sample_table_data(
        self, table_name: str, sample_size: int = 10, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves a random sample of records from the specified table.
        If no database is provided, uses the config database.

        :param table_name: Name of the table to sample data from.
        :param sample_size: Number of records to sample. Defaults to 10.
        :param database: Optional database name. If not provided, uses the config database.
        :return: List of dictionaries containing sampled records.
        """
        return self._execute(f"{table_name} | sample {sample_size}", database=database)

    def sample_function_data(
        self,
        function_call_with_params: str,
        sample_size: int = 10,
        database: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves a random sample of records from the result of a function call.
        If no database is provided, uses the config database.

        :param function_call_with_params: Function call string with parameters.
        :param sample_size: Number of records to sample. Defaults to 10.
        :param database: Optional database name. If not provided, uses the config database.
        :return: List of dictionaries containing sampled records.
        """
        return self._execute(
            f"{function_call_with_params} | sample {sample_size}", database=database
        )

    def ingest_inline_into_table(
        self, table_name: str, data_comma_separator: str, database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Ingests inline CSV data into a specified table. The data should be provided as a comma-separated string.
        If no database is provided, uses the config database.

        :param table_name: Name of the table to ingest data into.
        :param data_comma_separator: Comma-separated data string to ingest.
        :param database: Optional database name. If not provided, uses the config database.
        :return: List of dictionaries containing the ingestion result.
        """
        return self._execute(
            f".ingest inline into table {table_name} <| {data_comma_separator}",
            database=database,
        )

    def _run_clear_streamingingestion_schema(
        self, database: Optional[str] = None
    ) -> None:
        self._execute(
            ".clear database cache streamingingestion schema",
            readonly_override=True,
            database=database,
        )

    def _execute(
        self,
        query: str,
        readonly_override: bool = False,
        database: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        caller_frame = inspect.currentframe().f_back  # type: ignore
        # Get the name of the caller function
        action = caller_frame.f_code.co_name  # type: ignore

        database = (
            database
            or self.config.database_name
            or cast(str, self.conn.client.default_database)  # type: ignore
        )
        # agents can send messy inputs
        database = database.strip()
        query = query.strip()

        client = self.conn.client
        crp: ClientRequestProperties = ClientRequestProperties()
        crp.application = f"kusto-mcp-server{{{__version__}}}"  # type: ignore
        crp.client_request_id = f"KMCP.{action}:{str(uuid.uuid4())}"  # type: ignore
        if action not in self.DESTRUCTIVE_TOOLS and not readonly_override:
            crp.set_option("request_readonly", True)
        result_set = client.execute(database, query, crp)
        return format_results(result_set)


assert os.environ.get(
    "KUSTO_SERVICE_URI"
), "Environment variable KUSTO_SERVICE_URI must be set."

# Create the service instance
service = KustoService(
    config=KustoConfig(
        query_service_uri=cast(str, os.environ.get("KUSTO_SERVICE_URI")),
        database_name=os.environ.get("KUSTO_DATABASE"),
    )
)

# TODO: clean this up. probably would be better if it was placed elsewhere
mcp.add_tool(
    service.execute_query,
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
mcp.add_tool(
    service.execute_command,
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
)
mcp.add_tool(
    service.list_databases,
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
mcp.add_tool(
    service.list_tables,
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
mcp.add_tool(
    service.get_entities_schema,
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
mcp.add_tool(
    service.get_table_schema,
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
mcp.add_tool(
    service.get_function_schema,
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
mcp.add_tool(
    service.sample_table_data,
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
mcp.add_tool(
    service.sample_function_data,
    annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
)
mcp.add_tool(
    service.ingest_inline_into_table,
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
)
# Hide tools that use local fs for now until we feel safe to expose them
# mcp.add_tool(
#     service.print_file,
#     annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
# )
# mcp.add_tool(
#     service.ingest_csv_file_to_table,
#     annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False),
# )
