"""Dataset loader for the Tax Burden on Tobacco dataset.

Source: Centers for Disease Control and Prevention (CDC)
License: Public Domain
Paper Reference for Prop99:
    Abadie, A., Diamond, A., & Hainmueller, J. (2010).
    Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California's Tobacco Control Program.
    Journal of the American Statistical Association, 105(490), 493-505.
    https://doi.org/10.1198/jasa.2009.ap08746
"""

from nsquared.datasets.dataloader_base import NNDataLoader
from nsquared.datasets.dataloader_factory import register_dataset
from nsquared.data_types import DataType
import numpy as np
import pandas as pd
from typing import Any
import logging
from joblib import Memory
import os
import requests

memory = Memory(".joblib_cache", verbose=2)

logger = logging.getLogger(__name__)

params = {
    "start_year": (
        int,
        1970,
        "Start year for the data range.",
    ),
    "end_year": (
        int,
        2019,
        "End year for the data range.",
    ),
    "sample_states": (
        int,
        None,
        "Number of states to sample from the dataset. By default, returns all.",
    ),
    "seed": (int, None, "Random seed for reproducibility"),
}


@register_dataset("prop99", params)
class Prop99DataLoader(NNDataLoader):
    """Data from the Tax Burden on Tobacco dataset, focusing on cigarette consumption in packs.
    To initialize with default settings, use: NNData.create("prop99").
    """

    urls = {
        "tobacco_data": "https://data.cdc.gov/api/views/7nwe-3aj9/rows.csv?accessType=DOWNLOAD",
    }

    # 12 states that implemented Prop99 or similar legislation after 1988
    TREATED_STATES = {
        "CA",  # California
        "MA",  # Massachusetts
        "AZ",  # Arizona
        "OR",  # Oregon
        "FL",  # Florida
        "AK",  # Alaska
        "HI",  # Hawaii
        "MD",  # Maryland
        "MI",  # Michigan
        "NJ",  # New Jersey
        "NY",  # New York
        "WA",  # Washington
    }
    # 38 states that never implemented Prop99 or similar legislation
    CONTROL_STATES = {
        "TX",
        "WI",
        "MT",
        "RI",
        "KS",
        "ME",
        "UT",
        "VA",
        "IN",
        "GA",
        "AL",
        "SD",
        "NH",
        "DE",
        "NC",
        "CO",
        "AR",
        "CT",
        "MN",
        "NV",
        "LA",
        "IA",
        "NE",
        "SC",
        "OH",
        "TN",
        "WV",
        "KY",
        "ID",
        "MS",
        "IL",
        "WY",
        "VT",
        "ND",
        "PA",
        "OK",
        "MO",
        "NM",
    }
    # Rows to exclude from the dataset entirely
    EXCLUDED_STATES = {"DC"}

    def __init__(
        self,
        start_year: int = 1970,
        end_year: int = 2000,
        state: str = "CA",
        seed: int | None = None,
        **kwargs: Any,
    ):
        """Initializes the Prop99 data loader.

        Args:
        ----
            start_year: Start year for the data range. Default: 1970.
            end_year: End year for the data range. Default: 2019.
            state: State to impute. Default: "CA".
            seed: Random seed for reproducibility. Default: None
            kwargs: Additional keyword arguments.

        """
        super().__init__(
            **kwargs,
        )
        self.start_year = start_year
        self.end_year = end_year
        self.state = state
        self.data = None
        self.mask = None
        if seed is not None:
            np.random.seed(
                seed
            )  # instantiate random seed if provided but do it only once here

    def process_data_scalar(self) -> tuple[np.ndarray, np.ndarray]:
        """Process the data into scalar setting focusing on cigarette consumption in packs.

        Returns
        -------
            data: 2d processed data matrix of floats (states × years)
            mask: Mask for processed data

        """
        df = self._load_data()

        # Filter for cigarette consumption in packs
        logger.info(f"Original data shape: {df.shape}")
        df_consumption = df[
            df["SubMeasureDesc"] == "Cigarette Consumption (Pack Sales Per Capita)"
        ]
        logger.info(f"After SubMeasureDesc filter: {df_consumption.shape}")

        # Filter by year range
        df_consumption = df_consumption[
            (df_consumption["Year"] >= self.start_year)
            & (df_consumption["Year"] <= self.end_year)
        ]
        logger.info(f"After year range filter: {df_consumption.shape}")

        # Make sure we're working with a pandas DataFrame
        df_consumption = (
            pd.DataFrame(df_consumption)
            if not isinstance(df_consumption, pd.DataFrame)
            else df_consumption
        )

        # Pivot the data to get states as rows and years as columns
        data_df = df_consumption.pivot(
            index="LocationAbbr", columns="Year", values="Data_Value"
        )
        logger.info(f"Pivoted data shape: {data_df.shape}")

        # Retain only the control states and the treated state
        rows_to_drop = list(
            self.TREATED_STATES.union(self.EXCLUDED_STATES) - {self.state}
        )
        data_df = data_df.drop(rows_to_drop)
        logger.info(f"After excluding states: {data_df.shape}")

        # Create the mask: 0 for CA after 1988, 1 for everything else
        mask_df = pd.DataFrame(1, index=data_df.index, columns=data_df.columns)

        # If the treated state is in the data, set mask values to 0 for years after 1988
        assert self.state in mask_df.index, (
            f"{self.state} is not a valid state in the data"
        )
        # reorder the rows so that the treated state is the first row
        data_df = data_df.reindex(
            [self.state] + [state for state in data_df.index if state != self.state]
        )
        mask_df = mask_df.reindex(
            [self.state] + [state for state in mask_df.index if state != self.state]
        )

        ca_years = [year for year in mask_df.columns if int(year) > 1988]
        mask_df.loc[self.state, ca_years] = 0

        # Convert to numpy arrays
        data = data_df.to_numpy()
        mask = mask_df.to_numpy()

        # Store the processed data
        self.data = data
        self.mask = mask
        self.state_names = data_df.index.tolist()
        self.years = data_df.columns.tolist()

        return data, mask

    def process_data_distribution(
        self, data_type: DataType | None = None
    ) -> tuple[np.ndarray, np.ndarray]:
        """Does not apply to Prop99 as it is not a distributional dataset.

        Args:
            data_type: Data type to process. Default: None.

        """
        raise ValueError("There is no distributional data for Prop99.")

    def get_full_state_as_dict(self, include_metadata: bool = False) -> dict:
        """Returns the full state as a dictionary. For Prop99, this includes the data, masking matrix, and the custom parameters.

        If the data and mask are None, then the data has not been processed yet. Call process_data_scalar() to process the data first.

        Args:
            include_metadata (bool): Whether to include metadata in the dictionary. Default: False.

        """
        full_state = {
            "data": self.data,
            "mask": self.mask,
            "custom_params": {
                "start_year": self.start_year,
                "end_year": self.end_year,
            },
        }

        if include_metadata and hasattr(self, "state_names") and hasattr(self, "years"):
            full_state["metadata"] = {
                "state_names": self.state_names,
                "years": self.years,
                "data_description": "Cigarette Consumption (Per Capita in packs)",
            }

        return full_state

    @classmethod
    @memory.cache
    def _load_data(cls) -> pd.DataFrame:
        """Download and load the Tax Burden on Tobacco dataset."""
        csv_path = "tobacco_data.csv"

        # Check for locally provided file
        local_file = "The_Tax_Burden_on_Tobacco.csv"
        if os.path.exists(local_file):
            logger.info(f"Using locally provided file: {local_file}")
            return pd.read_csv(local_file)

        # Download if missing
        needs_download = not os.path.exists(csv_path)

        if needs_download:
            logger.info("Downloading Tax Burden on Tobacco dataset...")
            response = requests.get(cls.urls["tobacco_data"])
            if response.status_code != 200:
                raise RuntimeError(
                    f"Failed to download dataset: {response.status_code}"
                )
            # Write the content directly instead of using raw stream
            with open(csv_path, "wb") as f:
                f.write(response.content)

        logger.info(f"Loading data from {csv_path}")
        df = pd.read_csv(csv_path)
        return df
