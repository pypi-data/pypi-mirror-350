#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import glob
import os
import time
from contextlib import suppress
from datetime import datetime, timezone
from typing import Dict, Optional

from rich.console import Console

from data_diff import TableSegment, connect, connect_to_table, diff_tables
from data_diff.databases import Database
from dcs_sdk.sdk.config.config_loader import Comparison, SourceTargetConnection
from dcs_sdk.sdk.utils.serializer import serialize_table_schema
from dcs_sdk.sdk.utils.table import create_table_schema_row_count, differ_rows
from dcs_sdk.sdk.utils.themes import theme_1
from dcs_sdk.sdk.utils.utils import (
    calculate_column_differences,
    duck_db_load_csv_to_table,
    find_identical_columns,
    generate_table_name,
    obfuscate_sensitive_data,
)


class DBTableDiffer:
    def __init__(self, config: Comparison):
        self.config = config
        self.console = Console(record=True)
        self.created_at = datetime.now(tz=timezone.utc)
        self.start_time = time.monotonic()
        self.algorithm = "hashdiff"
        self.table1 = None
        self.table2 = None
        self.diff_iter = None
        self.response = {}
        self.source_file_path = self.config.source.filepath
        self.target_file_path = self.config.target.filepath
        self.limit = config.limit
        self.default_limit = 1000
        self.table_limit = 100
        self.source_db: Database = None
        self.target_db: Database = None
        self.similarity = self.config.similarity
        self.similarity_providers = None
        if self.similarity:
            from dcs_sdk.sdk.utils.similarity_score.base_provider import (
                ensure_nltk_data,
            )
            from dcs_sdk.sdk.utils.similarity_score.cosine_similarity_provider import (
                CosineSimilarityProvider,
            )
            from dcs_sdk.sdk.utils.similarity_score.jaccard_provider import (
                JaccardSimilarityProvider,
            )
            from dcs_sdk.sdk.utils.similarity_score.levenshtein_distance_provider import (
                LevenshteinDistanceProvider,
            )

            ensure_nltk_data()

            self.similarity_providers = {
                "jaccard": JaccardSimilarityProvider,
                "levenshtein": LevenshteinDistanceProvider,
                "cosine": CosineSimilarityProvider,
            }

    def create_dataset_dict(
        self,
        config: SourceTargetConnection,
        table: TableSegment,
        db_name: str,
        file_path: str,
        database_type: str,
    ) -> Dict:
        schema_list = [serialize_table_schema(v) for v in table.get_schema().values()]
        schema_list.sort(key=lambda x: x["column_name"].upper())

        return {
            "id": config.id,
            "name": config.name,
            "workspace": config.workspace,
            "database_type": database_type,
            "table_name": table.table_path[0],
            "schema": table.database.default_schema,
            "database": db_name,
            "primary_keys": list(table.key_columns),
            "file_path": file_path,
            "files": [] if file_path is None else [generate_table_name(csv, False) for csv in glob.glob(file_path)],
            "row_count": table.count(),
            "columns": schema_list,
            "exclusive_pk_cnt": 0,
            "duplicate_pk_cnt": 0,
            "null_pk_cnt": 0,
        }

    def connect_to_db_table(
        self,
        config: SourceTargetConnection,
        is_source: bool,
    ) -> TableSegment:
        if is_source:
            primary_keys = self.config.primary_keys_source
            columns = self.config.source_columns
            where = self.config.source_filter
        else:
            primary_keys = self.config.primary_keys_target
            columns = self.config.target_columns
            where = self.config.target_filter

        return connect_to_table(
            {
                "driver": config.driver,
                "host": config.host,
                "port": config.port,
                "http_path": config.http_path,
                "access_token": config.access_token,
                "user": config.username,
                "password": config.password,
                "database": config.database,
                "schema": config.schema_name,
                "filepath": config.filepath,
                "warehouse": config.warehouse,
                "role": config.role,
                "catalog": config.catalog,
                "account": config.account,
                "odbc_driver": config.odbc_driver,
                "server": config.server,
                "project": config.project,
                "dataset": config.dataset,
                "keyfile": config.keyfile,
                "impersonate_service_account": config.impersonate_service_account,
                "bigquery_credentials": config.bigquery_credentials,
            },
            config.table,
            tuple(primary_keys),
            extra_columns=tuple(columns),
            where=where,
        )

    def connect_to_db(self, config: SourceTargetConnection, is_source: bool):
        if is_source:
            self.source_db: Database = connect(
                {
                    "driver": config.driver,
                    "host": config.host,
                    "port": config.port,
                    "http_path": config.http_path,
                    "access_token": config.access_token,
                    "user": config.username,
                    "password": config.password,
                    "database": config.database,
                    "warehouse": config.warehouse,
                    "schema": config.schema_name,
                    "role": config.role,
                    "catalog": config.catalog,
                    "account": config.account,
                    "odbc_driver": config.odbc_driver,
                    "server": config.server,
                    "project": config.project,
                    "keyfile": config.keyfile,
                    "impersonate_service_account": config.impersonate_service_account,
                    "bigquery_credentials": config.bigquery_credentials,
                    "dataset": config.dataset,
                }
            )
        else:
            self.target_db: Database = connect(
                {
                    "driver": config.driver,
                    "host": config.host,
                    "port": config.port,
                    "http_path": config.http_path,
                    "access_token": config.access_token,
                    "user": config.username,
                    "password": config.password,
                    "database": config.database,
                    "warehouse": config.warehouse,
                    "schema": config.schema_name,
                    "role": config.role,
                    "catalog": config.catalog,
                    "account": config.account,
                    "odbc_driver": config.odbc_driver,
                    "server": config.server,
                    "project": config.project,
                    "keyfile": config.keyfile,
                    "impersonate_service_account": config.impersonate_service_account,
                    "bigquery_credentials": config.bigquery_credentials,
                    "dataset": config.dataset,
                }
            )

    def process_duckdb(self, is_source: bool):
        if is_source:
            filepath = self.config.source.filepath
        else:
            filepath = self.config.target.filepath
        if filepath is None:
            raise ValueError("File path is required for file")
        if filepath.endswith(".csv"):
            if not duck_db_load_csv_to_table(self.config, filepath, is_source):
                raise ValueError(f"Error in loading CSV, for the {'source' if is_source else 'target'}")

    def _prepare_source_table(self) -> Optional[str]:
        view_name = None
        if self.config.source.driver == "duckdb":
            return view_name
        if self.config.source_query is not None:
            self._process_database_as_schema(
                driver=self.config.source.driver,
                is_source=True,
            )
            self.connect_to_db(
                self.config.source,
                is_source=True,
            )
            view_name = self.source_db.create_view_from_query(
                query=self.config.source_query,
                schema=self.config.temporary_schema_source,
                view_name=self.config.view_name_source,
            )
            self.config.source.schema_name = self.config.temporary_schema_source
            self.config.source.table = view_name
        return view_name

    def _prepare_target_table(self) -> Optional[str]:
        view_name = None
        if self.config.target.driver == "duckdb":
            return view_name
        if self.config.target_query is not None:
            self._process_database_as_schema(
                driver=self.config.target.driver,
                is_source=False,
            )
            self.connect_to_db(
                self.config.target,
                is_source=False,
            )
            view_name = self.target_db.create_view_from_query(
                query=self.config.target_query,
                schema=self.config.temporary_schema_target,
                view_name=self.config.view_name_target,
            )
            self.config.target.schema_name = self.config.temporary_schema_target
            self.config.target.table = view_name

        return view_name

    def _process_database_as_schema(self, driver: str, is_source: bool):
        if driver in ["mysql"]:
            if is_source:
                self.config.source.database = self.config.temporary_schema_source
            else:
                self.config.target.database = self.config.temporary_schema_target

    def _process_duckdb_connections(self):
        if self.config.source.driver == "duckdb":
            self.process_duckdb(is_source=True)
        if self.config.target.driver == "duckdb":
            self.process_duckdb(is_source=False)

    def diff_tables(
        self,
        is_cli: bool = False,
        show_stats: bool = False,
        save_html: bool = False,
        html_path: str = "dcs_report.html",
        display_table: bool = False,
    ) -> Dict:

        self._process_duckdb_connections()
        view_name_source = self._prepare_source_table()
        view_name_target = self._prepare_target_table()

        self.table1 = self.connect_to_db_table(self.config.source, is_source=True)
        self.table2 = self.connect_to_db_table(self.config.target, is_source=False)

        db1_name = self.config.source.database or self.config.source.catalog or self.config.source.project or "source"
        db2_name = self.config.target.database or self.config.target.catalog or self.config.target.project or "target"

        columns_order_wise_src = self.config.primary_keys_source + self.config.source_columns
        columns_order_wise_target = self.config.primary_keys_target + self.config.target_columns

        src_masking_cols = self.config.source_masking_columns
        tgt_masking_cols = self.config.target_masking_columns
        masking_character = self.config.masking_character

        source_dataset = self.create_dataset_dict(
            self.config.source,
            self.table1,
            db1_name,
            self.source_file_path,
            "file" if self.config.source.driver == "duckdb" else self.config.source.driver,
        )
        target_dataset = self.create_dataset_dict(
            self.config.target,
            self.table2,
            db2_name,
            self.target_file_path,
            "file" if self.config.target.driver == "duckdb" else self.config.target.driver,
        )
        table_1_row_count = source_dataset.get("row_count", 0)
        table_2_row_count = target_dataset.get("row_count", 0)

        error_message = None
        is_table_empty = False
        if table_1_row_count == 0:
            error_message = f"Source table '{source_dataset.get('table_name')}' is empty"
            is_table_empty = True
        if table_2_row_count == 0:
            if error_message:
                error_message += f" and target table '{target_dataset.get('table_name')}' is empty"
            else:
                error_message = f"Target table '{self.response.get('target_dataset').get('table_name')}' is empty"
            is_table_empty = True
        if not is_table_empty and not self.config.schema_diff:
            self.diff_iter = diff_tables(
                self.table1,
                self.table2,
                algorithm=self.algorithm,
                bisection_factor=self.config.advanced_configuration.bisection_factor,
                bisection_threshold=self.config.advanced_configuration.bisection_threshold,
                max_threadpool_size=self.config.advanced_configuration.max_threadpool_size,
                strict=self.config.strict,
            )

        columns_mappings = [
            {"source_column": src, "target_column": trg}
            for src, trg in zip(columns_order_wise_src, columns_order_wise_target)
        ]

        self.response = {
            "source_dataset": source_dataset,
            "target_dataset": target_dataset,
            "columns_mappings": columns_mappings,
        }

        max_row_count = max(table_1_row_count, table_2_row_count)
        self.process_limit(max_row_count)
        if not is_table_empty and not self.config.schema_diff:
            diff_res = differ_rows(
                diff_iter=self.diff_iter,
                response=self.response,
                limit=self.limit,
                table_limit=self.table_limit,
                display_table=display_table,
                similarity=self.similarity,
                similarity_providers=self.similarity_providers,
                fields=self.config.source_columns,
                quick_comparison=self.config.quick_comparison,
                src_masking_cols=src_masking_cols if src_masking_cols else [],
                tgt_masking_cols=tgt_masking_cols if tgt_masking_cols else [],
                masking_character=masking_character,
            )
        else:
            diff_res = {
                "stats": {
                    "rows_A": 0,
                    "rows_B": 0,
                    "exclusive_A": 0,
                    "exclusive_B": 0,
                    "diff_pk_percent": 0,
                    "unchanged": 0,
                    "total_diff_count": 0,
                    "diff_rows_count": 0,
                    "total_duplicate_count_source": 0,
                    "total_duplicate_count_target": 0,
                    "diff_rows_percent": 0,
                    "has_differences": False,
                    "error": {},
                },
                "exclusive_pk_values_target": [],
                "exclusive_pk_values_source": [],
                "duplicate_pk_values_source": [],
                "duplicate_pk_values_target": [],
                "records_with_differences": [],
                "table": None,
            }
            if is_table_empty:
                diff_res["stats"]["has_differences"] = table_1_row_count != table_2_row_count
                try:
                    diff_res["stats"]["diff_pk_percent"] = abs(
                        (table_1_row_count - table_2_row_count) / max(table_1_row_count, table_2_row_count)
                    )
                except ZeroDivisionError:
                    diff_res["stats"]["diff_pk_percent"] = 0
                diff_res["stats"]["error"] = {
                    "code": "empty_table",
                    "message": error_message,
                    "level": "WARNING",
                }

        diff_res.setdefault("stats", {})["rows_A"] = table_1_row_count
        diff_res.setdefault("stats", {})["rows_B"] = table_2_row_count

        columns_with_unmatched_data_type, columns_not_compared = calculate_column_differences(
            source_dataset["columns"], target_dataset["columns"], columns_mappings
        )

        diff_res.get("stats", {}).update(
            {
                "identical_columns": find_identical_columns(
                    source_dataset["columns"],
                    target_dataset["columns"],
                ),
                "columns_with_unmatched_data_type": columns_with_unmatched_data_type,
                "columns_not_compared": columns_not_compared,
            }
        )
        if self.config.schema_diff:
            identical_col_length = len(diff_res.get("stats", {}).get("identical_columns", []))
            diff_res["stats"]["has_differences"] = not (
                identical_col_length == len(source_dataset.get("columns", []))
                and identical_col_length == len(target_dataset.get("columns", []))
            )
            if error_message:
                diff_res["stats"]["error"]["level"] = "WARNING"

        source_dataset["exclusive_pk_cnt"] = diff_res.get("stats", {}).get("exclusive_A", 0)
        target_dataset["exclusive_pk_cnt"] = diff_res.get("stats", {}).get("exclusive_B", 0)
        table = diff_res.pop("table", None)
        if is_cli and display_table:
            create_table_schema_row_count(self.response, table, self.console)
            if save_html:
                self.console.save_html(html_path, theme=theme_1, clear=True)

        duckb_file_location_source = self.config.source.filepath
        duckb_file_location_target = self.config.target.filepath
        self.config.source.filepath = self.source_file_path
        self.config.target.filepath = self.target_file_path
        if self.config.source.driver == "duckdb":
            self.config.source.driver = "file"
        if self.config.target.driver == "duckdb":
            self.config.target.driver = "file"

        self.response["source_dataset"]["duplicate_pk_cnt"] = diff_res.get("stats", {}).get(
            "total_duplicate_count_source", 0
        )
        self.response["target_dataset"]["duplicate_pk_cnt"] = diff_res.get("stats", {}).get(
            "total_duplicate_count_target", 0
        )
        self.response["source_dataset"]["null_pk_cnt"] = diff_res.get("stats", {}).get("null_pk_count_source", 0)
        self.response["target_dataset"]["null_pk_cnt"] = diff_res.get("stats", {}).get("null_pk_count_target", 0)

        self.response["source_dataset"]["pk_cnt"] = (
            self.response["source_dataset"]["row_count"]
            - self.response["source_dataset"]["duplicate_pk_cnt"]
            - self.response["source_dataset"]["null_pk_cnt"]
        )
        self.response["target_dataset"]["pk_cnt"] = (
            self.response["target_dataset"]["row_count"]
            - self.response["target_dataset"]["duplicate_pk_cnt"]
            - self.response["target_dataset"]["null_pk_cnt"]
        )
        self.response.update(diff_res)
        if show_stats:
            self.print_stats()

        self.drop_view_and_close_connection(view_name_source, view_name_target)
        self.cleanup_duckdb(
            src=duckb_file_location_source,
            target=duckb_file_location_target,
        )
        finished_at = datetime.now(tz=timezone.utc)
        end_time = time.monotonic()
        duration = end_time - self.start_time
        meta = {
            "meta": {
                "created_at": self.created_at.isoformat(),
                "seconds": round(duration, 2),
                "finished_at": finished_at.isoformat(),
                "status": "done",
            }
        }
        self.response.update(meta)
        return self.response

    def process_limit(self, max_row_count):
        if isinstance(self.limit, int):
            if self.limit > max_row_count:
                self.limit = max_row_count
                print(f"Limit exceeds max row count, adjusted to {max_row_count}")
            return

        if isinstance(self.limit, str):
            if "%" in self.limit:
                cleaned_limit = self.limit.replace("%", "").strip()
                if cleaned_limit.isdigit():
                    percentage = float(cleaned_limit)
                    if percentage > 100:
                        self.limit = max_row_count
                        print("Percentage exceeds 100%, set to maximum row count")
                    else:
                        calc_limit = int((percentage / 100) * max_row_count)
                        self.limit = max(1, int(calc_limit))
                        print(f"Limit set to {self.limit} ({percentage}% of {max_row_count})")
                else:
                    self.limit = self.default_limit
                    print(f"Invalid percentage format, set to default: {self.limit}")
            else:
                self.limit = self.default_limit
                print(f"Invalid string format, set to default: {self.limit}")

    def drop_view_and_close_connection(self, view_name_source, view_name_target):

        def safe_close(db_connection):
            if db_connection:
                with suppress(Exception):
                    db_connection.close()

        safe_close(self.table1.database)
        safe_close(self.table2.database)

        if self.source_db:
            self.source_db.drop_view_from_db(
                view_name=view_name_source,
                schema=self.config.temporary_schema_source,
            )
        if self.target_db:
            self.target_db.drop_view_from_db(
                view_name=view_name_target,
                schema=self.config.temporary_schema_target,
            )

        safe_close(self.source_db)
        safe_close(self.target_db)

    def cleanup_duckdb(self, src: str, target: str):
        if src and src.endswith("duckdb"):
            with suppress(Exception):
                os.remove(src)
        if target and target.endswith("duckdb"):
            with suppress(Exception):
                os.remove(target)

    def print_stats(self):
        try:
            stats = self.response.get("stats", {})
            output = ""
            if stats:
                if self.config.quick_comparison:
                    output += f"Quick comparison: {self.config.quick_comparison}\n"
                    output += f"Has differences {stats.get('has_differences', False)}\n"
                else:
                    output += f"{stats.get('exclusive_A', 0)} rows are exclusive to source\n"
                    output += f"{stats.get('exclusive_B', 0)} rows are exclusive to target\n"
                    output += f"{stats.get('total_duplicate_count_source', 0)} duplicate rows in source\n"
                    output += f"{stats.get('total_duplicate_count_target', 0)} duplicate rows in target\n"
                    # output += f"{stats.get('total_diff_count', 0)} rows are different\n"
                    # output += f"{stats.get('diff_rows_count', 0)} rows are different\n"
                    for k, v in stats.get("values", {}).items():
                        output += f"{v} rows with different values in column: {k}\n"
                    # output += f"{round((stats.get('diff_pk_percent', 0) * 100),3)}% of primary keys are different\n"
                    # output += f"{round((stats.get('diff_rows_percent', 0) * 100),3)}% of rows are different\n"
                print(output)
        except Exception as e:
            print(f"Error in printing stats: {e}")

    def slice_rows(self, rows, start, end):
        return rows[start:end]


def diff_db_tables(
    config: Comparison,
    is_cli: bool = False,
    show_stats: bool = False,
    save_html: bool = False,
    html_path: str = "dcs_report.html",
    display_table: bool = False,
) -> Dict:
    differ = DBTableDiffer(config)
    response = differ.diff_tables(
        is_cli=is_cli,
        show_stats=show_stats,
        save_html=save_html,
        html_path=html_path,
        display_table=display_table,
    )
    response["comparison_name"] = config.comparison_name
    configuration = config.model_dump()
    del configuration["source"]["id"]
    del configuration["target"]["id"]
    configuration["source"]["schema_name"] = response["source_dataset"]["schema"]
    configuration["target"]["schema_name"] = response["target_dataset"]["schema"]
    response["configuration"] = configuration
    if is_cli:
        response["configuration"]["source"] = obfuscate_sensitive_data(response["configuration"]["source"])
        response["configuration"]["target"] = obfuscate_sensitive_data(response["configuration"]["target"])
    return response
