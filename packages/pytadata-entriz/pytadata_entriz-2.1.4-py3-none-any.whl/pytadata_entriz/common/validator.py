import os
import math
import logging
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict
import pandas as pd


class SchemaDataValidator:
    """
    Validates data against a schema defined in a file.
    This class checks for missing columns, data types, and null values
    """

    # ---------------     constructor and helper methods UNCHANGED     --------------- #
    def __init__(
        self,
        schema_csv_path,
        input_data_df,
        logger: logging.Logger,
    ):
        self.schema_csv_path = schema_csv_path
        self.input_data_df = input_data_df
        self.schema_df = None
        self.data_df = None
        self.errors: List[Dict[str, Any]] = []
        self.logger = logger

        self._type_checkers = {
            "STRING": self._is_string,
            "INTEGER": self._es_int,
            "FLOAT": self._es_float,
            "DATETIME": self._es_date,
            "DATE": self._es_date,
            "BOOL": self._es_bool,
        }

    # ---------- helper type-checkers ---------- #
    @staticmethod
    def _is_string(x):
        if isinstance(x, bytes):
            return False
        elif not pd.notna(x) and isinstance(x, float):
            return False
        return isinstance(str(x), str) and pd.notna(x)

    @staticmethod
    def _es_int(x):
        if isinstance(x, bool):
            return False
        if isinstance(x, int):
            return True
        if isinstance(x, str):
            try:
                int(x)
                return True
            except ValueError:
                return False
        if isinstance(x, float):
            return not math.isnan(x) and x == int(x)
        return False

    @staticmethod
    def _es_float(x):
        if isinstance(x, bool):
            return False
        if isinstance(x, str):
            try:
                float(x)
                return True
            except ValueError:
                return False
        return isinstance(x, (int, float)) and not pd.isna(x)

    @staticmethod
    def _es_date(x):
        if isinstance(x, (datetime, pd.Timestamp)):
            return True
        if isinstance(x, str):
            try:
                datetime.fromisoformat(x)
                return True
            except (ValueError, TypeError):
                pass
            try:
                datetime.strptime(x, "%d/%m/%Y")
                return True
            except (ValueError, TypeError):
                return False
        return False

    @staticmethod
    def _es_bool(x):
        if isinstance(x, bool):
            return True
        return isinstance(x, int) and x in [0, 1]

    # --- Loading Methods ---
    def load_schema(self):
        if not os.path.exists(self.schema_csv_path):
            self.logger.error(f"Schema file not found: {self.schema_csv_path}")
            raise FileNotFoundError(f"Schema file not found: {self.schema_csv_path}")

        try:
            self.schema_df = pd.read_csv(self.schema_csv_path)
        except Exception as e:
            self.logger.error(f"Error loading schema from {self.schema_csv_path}: {e}")
            raise IOError(f"Error loading schema from {self.schema_csv_path}: {e}")

        self.schema_df.rename(columns=lambda c: c.strip(), inplace=True)

        if "¿Obligatorio?" in self.schema_df.columns:
            self.schema_df["obligatorio"] = (
                self.schema_df["¿Obligatorio?"].astype(str).str.strip().str.lower()
                == "obligatorio"
            )
        else:
            self.schema_df["obligatorio"] = False
            self.logger.warning(
                f"'¿Obligatorio?' column not found in schema file {self.schema_csv_path}. "
                "Assuming all columns are optional."
            )

        required_schema_cols = ["Datos", "Tipo"]
        if not all(col in self.schema_df.columns for col in required_schema_cols):
            missing = [
                col for col in required_schema_cols if col not in self.schema_df.columns
            ]
            self.logger.error(
                f"Schema file {self.schema_csv_path} missing columns: {missing}"
            )
            raise ValueError(
                f"Schema file {self.schema_csv_path} must contain columns: {required_schema_cols}. Missing: {missing}"
            )
        self.logger.info("Schema loaded successfully.")

    def load_data(self):
        if isinstance(self.input_data_df, pd.DataFrame):
            self.data_df = self.input_data_df
            self.logger.info("Data loaded successfully from DataFrame.")
        else:
            self.logger.error(
                "Data loading from file paths is not implemented in this version. "
                "Please provide a pandas DataFrame directly."
            )
            raise NotImplementedError(
                "Loading data from file paths is not implemented in this version. "
                "Please provide a pandas DataFrame directly."
            )

    def _collect_errors(self, mask, serie, col, tpo, problema, validacion):
        return [
            {
                "fila": idx,  # 0-based (report adds +1 later)
                "columna": col,
                "valor": val,
                "problema": problema,
                "tipo_esperado": tpo,
                "tipo_encontrado": type(val).__name__ if pd.notna(val) else "NaN/None",
                "validacion": validacion,
            }
            for idx, val in serie[mask].items()
        ]

    # -----------------------------------------------------------------------

    def validate(self):
        """
        Vectorised
        """
        if self.schema_df is None:
            raise ValueError("Schema not loaded. Call load_schema() first.")
        if self.data_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        self.errors: list[dict] = []  # reset

        for _, regla in self.schema_df.iterrows():
            col = str(regla["Datos"]).strip()
            tpo = str(regla["Tipo"]).strip().upper()
            required = bool(regla["obligatorio"])

            # 1 . columna inexistente --------------------------------------------------
            if col not in self.data_df.columns:
                self.errors.append(
                    {
                        "fila": None,
                        "columna": col,
                        "valor": None,
                        "problema": "La columna no existe en el dataset",
                        "tipo_esperado": tpo,
                        "tipo_encontrado": "N/A",
                        "validacion": "Columna Faltante",
                    }
                )
                continue

            checker = self._type_checkers.get(tpo)
            if checker is None:
                self.errors.append(
                    {
                        "fila": None,
                        "columna": col,
                        "valor": None,
                        "problema": f"Tipo '{tpo}' no reconocido en el validador",
                        "tipo_esperado": tpo,
                        "tipo_encontrado": "N/A",
                        "validacion": "Configuración Inválida",
                    }
                )
                continue

            serie = self.data_df[col]

            # 2 . valores nulos en campo obligatorio ----------------------------------
            if required:
                null_mask = serie.isna()
                if null_mask.any():
                    self.errors.extend(
                        self._collect_errors(
                            null_mask,
                            serie,
                            col,
                            tpo,
                            "Valor nulo pero la columna es obligatoria",
                            "Campo Obligatorio",
                        )
                    )

            # 3 . tipo de dato incorrecto (solo para no-nulos) ------------------------
            valid_mask = serie.apply(
                checker
            )  # calls the *original* per-value function → logic identical
            invalid_mask = (~serie.isna()) & (~valid_mask)
            # invalid_mask = (serie.isna()) & (~valid_mask)

            if invalid_mask.any():
                self.errors.extend(
                    self._collect_errors(
                        invalid_mask,
                        serie,
                        col,
                        tpo,
                        f"Tipo inválido, esperaba {tpo}",
                        "Tipo de Dato",
                    )
                )
        self.logger.info(
            f"Validation completed. Found {len(self.errors)} potential issues."
        )

    # --- Reporting Methods ---
    def get_report_dataframe(self, enable_err_details: bool = False):
        """
        Converts the collected errors into a pandas DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing validation issues.
                              Returns an empty DataFrame with correct columns
                              if no issues were found or if validation failed
                              during setup/loading.
        """
        if not self.errors:
            return pd.DataFrame(
                columns=[
                    "fila",
                    "columna",
                    "valor",
                    "problema",
                    "tipo_esperado",
                    "tipo_encontrado",
                    "validacion",
                ]
            )

        collapsed_complete = self._collapse_errors(self.errors)

        self.logger.info(
            f"Collapsing errors into {len(collapsed_complete)} unique issues."
        )

        df_complete = (
            pd.DataFrame(collapsed_complete)
            .sort_values(["fila", "columna"], na_position="first")
            .reset_index(drop=True)
        )

        return df_complete

    # --- Main Execution Method ---
    def run_validation_and_report(
        self,
        enable_err_details=False,
    ):
        try:
            start_time = datetime.now()
            self.load_schema()
            self.load_data()
            start_time = datetime.now()
            self.logger.info(f"Validation process detect started at {start_time}.")
            self.validate()  # This is the optimized part
            end_time = datetime.now()
            self.logger.info(
                f"Validation process detect started at {end_time - start_time}."
            )
            start_time = datetime.now()
            self.logger.info(f"Validation process group end at {start_time}.")
            report_df = self.get_report_dataframe(enable_err_details)
            end_time = datetime.now()
            self.logger.info(
                f"Validation process group end at {end_time - start_time}."
            )

            duration = end_time - start_time

            self.logger.info(
                f"Validation process finished. Report has {report_df.shape[0]} rows. Time taken: {duration}"
            )

            return report_df
        except (FileNotFoundError, ValueError, IOError) as e:
            self.logger.error(
                f"A known error occurred during validation setup or loading: {e}"
            )
            return pd.DataFrame(
                columns=[
                    "fila",
                    "columna",
                    "valor",
                    "problema",
                    "tipo_esperado",
                    "tipo_encontrado",
                    "validacion",
                ]
            )
        except Exception:
            self.logger.exception(
                "An unexpected error occurred during validation:"
            )  # .exception logs stack trace
            return pd.DataFrame(
                columns=[
                    "fila",
                    "columna",
                    "valor",
                    "problema",
                    "tipo_esperado",
                    "tipo_encontrado",
                    "validacion",
                ]
            )

    def _collapse_errors(self, error_dicts):
        """
        Collapse duplicated (fila, columna) entries while preserving the original
        semantics ( first valor / tipos  +  concatenated problema & validacion ).

        Returns
        -------
        list[dict]  one dict per unique (fila, columna)
        """
        merged = defaultdict(
            lambda: {
                "valor": None,
                "problema": set(),
                "tipo_esperado": None,
                "tipo_encontrado": None,
                "validacion": set(),
            }
        )

        for err in error_dicts:
            key = (err["fila"], err["columna"])
            bucket = merged[key]

            # keep first seen scalar fields (matches old behaviour)
            if bucket["valor"] is None:
                bucket["valor"] = err["valor"]
                bucket["tipo_esperado"] = err["tipo_esperado"]
                bucket["tipo_encontrado"] = err["tipo_encontrado"]

            # accumulate many-to-one fields
            bucket["problema"].add(err["problema"])
            bucket["validacion"].add(err["validacion"])

        # flatten sets into the original pipe-joined strings
        result = []
        for (fila, columna), data in merged.items():
            result.append(
                {
                    "fila": None if fila is None else fila + 1,  # +1 for human rows
                    "columna": columna,
                    "valor": data["valor"],
                    "problema": " | ".join(sorted(data["problema"])),
                    "tipo_esperado": data["tipo_esperado"],
                    "tipo_encontrado": data["tipo_encontrado"],
                    "validacion": " | ".join(sorted(data["validacion"])),
                }
            )
        return result
