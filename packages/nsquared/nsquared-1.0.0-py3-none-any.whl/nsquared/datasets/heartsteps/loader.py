"""Dataset loader for the HeartSteps V1 dataset.

Source: https://github.com/klasnja/HeartStepsV1
License: CC-BY-4.0
Paper Reference:
    Klasnja, P., Smith, S., Seewald, N. J., Lee, A., Hall, K., Luers, B., Hekler, E. B., & Murphy, S. A. (2019).
    Efficacy of Contextually Tailored Suggestions for Physical Activity: A Micro-randomized Optimization Trial of HeartSteps.
    Annals of Behavioral Medicine, 53(6), 573–582.
    https://doi.org/10.1093/abm/kay067
"""

from nsquared.datasets.dataloader_base import NNDataLoader
from nsquared.datasets.dataloader_factory import register_dataset
from datetime import timedelta
import numpy as np
import pandas as pd
from typing import Any
import warnings
import logging
from joblib import Memory
from nsquared.data_types import DataType


memory = Memory(".joblib_cache", verbose=2)

logger = logging.getLogger(__name__)

params = {
    "freq": (str, "5min", "Frequency of step count samples"),
    "participants": (int, 37, "Number of participants in the study"),
    "max_study_day": (int, 52, "Maximum number of study days to include"),
    "num_measurements": (int, 12, "Number of measurements per decision point"),
}


@register_dataset("heartsteps", params)
class HeartStepsDataLoader(NNDataLoader):
    """Data from the Heartsteps V1 study formatted into a matrix or tensor.
    To initialize with default settings, use: NNData.create("heartsteps").

    """

    urls = {
        "jbsteps.csv": "https://raw.githubusercontent.com/klasnja/HeartStepsV1/refs/heads/main/data_files/jbsteps.csv",
        "suggestions.csv": "https://raw.githubusercontent.com/klasnja/HeartStepsV1/refs/heads/main/data_files/suggestions.csv",
    }

    def __init__(
        self,
        agg: str = "mean",
        freq: str = "5min",
        participants: int = 37,
        max_study_day: int = 52,
        num_measurements: int = 12,
        log_transform: bool = True,
        **kwargs: Any,
    ):
        """Initializes the HeartSteps data loader.

        Args:
        ----
            agg: Aggregation method to use to create scalar dataset. Default: "mean".
            freq: Frequency of step count samples. Default: "5min".
            participants: Number of participants to include. Default: 37 (maximum).
            max_study_day: Maximum study day. Default: 52.
            num_measurements: Number of measurements taken after each decision point. Default: 12.
                Note: it is recommended that you use no more than 1-2 hours of data after each decision point to avoid overlap with the next decision point.
                This means that freq (in minutes) * num_measurements should be approximately 60.
            log_transform: Whether to apply log transformation to the data. Default: True.
            kwargs: Additional keyword arguments.

        """
        super().__init__(
            agg=agg,
            **kwargs,
        )
        self.freq = freq
        self.participants = participants
        self.max_study_day = max_study_day
        self.num_measurements = num_measurements
        self.data = None
        self.mask = None
        self.log_transform = log_transform

    def process_data_scalar(self, agg: str = "mean") -> tuple[np.ndarray, np.ndarray]:
        """Process the data into scalar setting. Note that this implementation is specific to HeartSteps as it calls upon functions that do specific HeartSteps data processing.

        Args:
        ----
            agg: Aggregation method to use. Default: "mean". Options: "mean", "sum", "median", "std", "variance"

        Returns:
        -------
            data: 2d processed data matrix of floats
            mask: Mask for processed data

        """
        df_steps, df_suggestions = self._load_data()
        data, _, mask = self._proc_dist_data(df_steps, df_suggestions)
        if agg == "mean":
            data = np.nanmean(data, axis=2)
        elif agg == "sum":
            data = np.nansum(data, axis=2)
        elif agg == "median":
            data = np.nanmedian(data, axis=2)
        elif agg == "std":
            data = np.nanstd(data, axis=2)
        elif agg == "variance":
            data = np.nanvar(data, axis=2)
        else:
            raise ValueError(
                "agg must be one of 'mean', 'sum', 'median', 'std', or 'variance'"
            )

        data = np.squeeze(data)
        self.data = data
        self.mask = mask
        return data, mask

    def process_data_distribution(
        self, data_type: DataType | None = None
    ) -> tuple[np.ndarray, np.ndarray]:
        """Process the data into distribution setting. Note that this implementation is specific to HeartSteps as it calls upon functions that do specific HeartSteps data processing.

        Args:
            data_type: Data type to process. Default: None.

        Returns:
            data: 4d processed data tensor of floats
            mask: Mask for processed data

        """
        df_steps, df_suggestions = self._load_data()

        _, data2d, mask = self._proc_dist_data(df_steps, df_suggestions)
        self.data = data2d
        self.mask = mask
        return data2d, mask

    def get_full_state_as_dict(self, include_metadata: bool = False) -> dict:
        """Returns the full state as a dictionary. For HeartSteps, this includes the data, masking matrix, and the custom parameters (if include_metadata == True

        If the data and mask are None, then the data has not been processed yet. Call process_data_scalar() or process_data_distribution() to process the data first.

        Args:
            include_metadata (bool): Whether to include metadata in the dictionary. Default: False. The metadata for HeartSteps is currently empty.

        """
        full_state = {
            "data": self.data,
            "mask": self.mask,
            "custom_params": {
                "freq": self.freq,
                "participants": self.participants,
                "max_study_day": self.max_study_day,
                "num_measurements": self.num_measurements,
            },
        }
        return full_state

    ## HELPER FUNCTIONS
    @classmethod
    @memory.cache
    def _load_data(cls) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load the data from the remote source through urls

        Returns:
            df_steps: pd.DataFrame
            df_suggestions: pd.DataFrame

        """
        logger.info("Retrieving data from url...")
        jp_path = cls.urls["jbsteps.csv"]
        sug_path = cls.urls["suggestions.csv"]

        df_steps = pd.read_csv(jp_path, low_memory=False)
        df_suggestions = pd.read_csv(sug_path, low_memory=False)
        return df_steps, df_suggestions

    @staticmethod
    @memory.cache
    def _transform_dnn(
        df: Any,
        users: int = 37,
        max_study_day: int = 52,
        day_dec: int = 5,
        num_measurements: int = 12,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Iteratively transform the processed HeartSteps data into a 4d tensor"""
        warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
        final_M = np.zeros((users, max_study_day, day_dec, num_measurements))
        final_A = np.zeros((users, max_study_day, day_dec))

        for user in range(1, users + 1):
            for day in range(1, max_study_day + 1):
                for slot in range(1, day_dec + 1):
                    try:
                        df_uds = df.loc[pd.IndexSlice[(user, day, slot)]]
                        ind = df.index.get_indexer_for(df_uds.index)[0]
                        df_rng = df.iloc[
                            np.arange(ind, min(ind + num_measurements, len(df)))
                        ]
                        if df.iloc[ind]["avail"]:
                            # only take send.sedentary as the treatment indicator, could use send.active later
                            val = df.iloc[ind]["send.sedentary"]
                            conv_val = val if ~np.isnan(val) else df.iloc[ind]["send"]
                            final_A[user - 1, day - 1, slot - 1] = int(conv_val)
                        else:
                            final_A[user - 1, day - 1, slot - 1] = 2

                        measurements = df_rng["steps"].to_numpy()
                        if len(measurements) == num_measurements:
                            final_M[user - 1, day - 1, slot - 1] = measurements
                        else:
                            m_pad = np.pad(
                                measurements,
                                (0, num_measurements - len(measurements)),
                                constant_values=np.nan,
                            )
                            final_M[user - 1, day - 1, slot - 1] = m_pad
                    except KeyError:
                        final_A[user - 1, day - 1, slot - 1] = 0
                        final_M[user - 1, day - 1, slot - 1] = np.full(
                            num_measurements, np.nan
                        )
        final_M = final_M.reshape((users, max_study_day * day_dec, num_measurements))
        final_A = final_A.reshape((users, max_study_day * day_dec))
        return final_M, final_A

    @staticmethod
    def _get_mode(x: pd.Series) -> Any:
        if len(pd.Series.mode(x) > 1):
            return pd.Series.mode(x, dropna=False)[0]
        else:
            return pd.Series.mode(x, dropna=False)

    def _reind_id(self, df_u: Any) -> pd.DataFrame:
        """Function to reindex the data to include all time points for each user."""
        d_rnge = pd.date_range(
            min(df_u.index.astype("datetime64[ns]")),
            max(df_u.index.astype("datetime64[ns]")) + timedelta(days=1),
            normalize=True,
            inclusive="both",
            freq=self.freq,
        )
        d_rnge = d_rnge[d_rnge.indexer_between_time("00:00", "23:55")]
        # print(rng)
        df_reind = df_u.reindex(d_rnge)
        df_reind["user.index"] = df_reind["user.index"].ffill().bfill()
        df_reind["study.day.nogap"] = df_reind["study.day.nogap"].bfill().ffill()
        df_reind["steps"] = df_reind["steps"].fillna(0)
        return df_reind

    @staticmethod
    def _take_range(df: Any, range: int) -> pd.DataFrame:
        idx = df.index.get_indexer_for(df[pd.notna(df["sugg.select.slot"])].index)
        ranges = [np.arange(i, min(i + range + 1, len(df))) for i in idx]
        return df.iloc[np.concatenate(ranges)]

    @staticmethod
    def _create_slots(df: Any) -> pd.DataFrame:
        most_rec_slot = 0.0
        for ind, row in df.iterrows():
            curr_slot = row["sugg.select.slot"]
            if not np.isnan(curr_slot):
                if (
                    most_rec_slot != 5.0
                    and curr_slot != most_rec_slot + 1
                    and most_rec_slot != 0.0
                ):
                    df.at[ind, "new_slot"] = most_rec_slot + 1
                    most_rec_slot += 1
                elif most_rec_slot == 5.0 and curr_slot != 1:
                    df.at[ind, "new_slot"] = 1
                    most_rec_slot = 1
                else:
                    df.at[ind, "new_slot"] = curr_slot
                    most_rec_slot = curr_slot
        return df

    @staticmethod
    def _study_day(df: Any) -> pd.DataFrame:
        most_rec_slot = 1.0
        curr_study_day = 1
        for ind, row in df.iterrows():
            curr_slot = row["new_slot"]
            if not np.isnan(curr_slot):
                if most_rec_slot == 5.0 and curr_slot == 1:
                    curr_study_day += 1
                most_rec_slot = curr_slot
                df.at[ind, "study_day"] = curr_study_day
        return df

    @staticmethod
    @memory.cache
    def _group_steps(df: pd.DataFrame, freq: str) -> pd.DataFrame:
        return df.groupby(
            [
                # TODO: (Caleb) resolve this Grouper pyright error - says no parameter named 'label' but pd.Grouper param list has 'label'.
                # Main issue is that TimeGrouper (which has the param label) was deprecated but is still used under the hood
                # so the param label is not explicitly exposed in the Grouper init definition but is still accepted/used.
                pd.Grouper(freq=freq, level="steps.utime", label="right"),  # pyright: ignore
                pd.Grouper(level="user.index"),
            ],
            sort=False,
        ).agg(
            {
                "steps": "sum",
                "study.day.nogap": lambda x: HeartStepsDataLoader._get_mode(x),
            }
        )

    def _proc_dist_data(
        self, df_steps: pd.DataFrame, df_suggestions: pd.DataFrame
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Process the data into distribution setting."""
        logger.debug("Processing HeartSteps V1...")
        # get relevant cols and reformatting
        df_steps = pd.DataFrame(
            df_steps[["user.index", "steps.utime", "steps", "study.day.nogap"]]
        )
        df_steps = df_steps.copy()
        df_steps["steps.utime"] = pd.to_datetime(df_steps["steps.utime"])
        # create multi-index
        df_steps = df_steps.set_index(["user.index", "steps.utime"])

        # get relevant cols and reformatting
        df_sugg_sel = df_suggestions[
            [
                "user.index",
                "decision.index.nogap",
                "sugg.select.utime",
                "sugg.decision.utime",
                "sugg.select.slot",
                "avail",
                "send",
                "send.active",
                "send.sedentary",
            ]
        ]
        df_sugg_sel = df_sugg_sel.copy()
        df_sugg_sel["sugg.decision.utime"] = pd.to_datetime(
            df_sugg_sel["sugg.decision.utime"]
        )
        # TODO: (Caleb) Resolve pyright error with dropna function
        df_sugg_sel = df_sugg_sel.dropna(  # pyright: ignore
            subset=["sugg.decision.utime", "sugg.select.utime", "user.index"]
        )

        # group the step data by five minute intervals
        df_freq = HeartStepsDataLoader._group_steps(df_steps, self.freq).reset_index()

        df_freq_ind = df_freq.set_index("steps.utime")

        # expand the step data to include all time points
        # df_expand5min = df_5min_ind.groupby("user.index", group_keys=False).apply(
        #     lambda df_u: _reind_id(df_u)
        # )

        result_dfs = []
        user_indices = df_freq_ind["user.index"].unique()
        # process each user
        for user_idx in user_indices:
            # filter for just this user
            df_u = df_freq_ind[df_freq_ind["user.index"] == user_idx].copy()
            reindexed_df = self._reind_id(df_u)
            result_dfs.append(reindexed_df)
        df_expandfreq = pd.concat(result_dfs)

        df_expandfreq = df_expandfreq.reset_index(names="steps.utime")
        df_expandfreq["user.index"] = df_expandfreq["user.index"].astype("int64")

        # merge the step data with the notification data
        df_merged = (
            pd.merge_asof(
                df_expandfreq.sort_values(by="steps.utime"),
                df_sugg_sel.sort_values(by="sugg.decision.utime"),
                left_on="steps.utime",
                right_on="sugg.decision.utime",
                by="user.index",
                # TODO: (Caleb) Resolve pyright error with pd.Timedelta. This is due to another incompatibility in the pandas type specification.
                # tolerance does not accept NaT, but Timedelta could return NaT. Pandas documentation uses pd.Timedelta in this way exactly, so unsure of solution.
                tolerance=pd.Timedelta(self.freq),  # pyright: ignore
                allow_exact_matches=False,
                direction="backward",
            )
            .sort_values(by=["user.index", "steps.utime"])
            .reset_index(drop=True)
        )
        df_merged["sugg.select.slot"] = np.where(
            df_merged["decision.index.nogap"].isna(),
            np.nan,
            df_merged["sugg.select.slot"],
        )

        # get num_measurement rows after each notification period (1 hour of observations by default args)
        unique_users = df_merged["user.index"].unique()
        result_dfs = []

        for user_idx in unique_users:
            df_user = df_merged[df_merged["user.index"] == user_idx]
            df_user_range = HeartStepsDataLoader._take_range(
                df_user, self.num_measurements
            )
            result_dfs.append(df_user_range)

        df_merged_cut = pd.concat(result_dfs).reset_index(drop=True)
        df_merged_cut_nd = df_merged_cut.drop_duplicates()

        # set up column for study day
        df_merged_cut_nd = df_merged_cut_nd.copy()
        df_merged_cut_nd["study_day"] = np.nan
        df_merged_cut_nd["new_slot"] = np.nan

        # align decision points
        unique_users = df_merged_cut_nd["user.index"].unique()
        slot_results = []

        for user_idx in unique_users:
            df_user = df_merged_cut_nd[df_merged_cut_nd["user.index"] == user_idx]
            user_slots = HeartStepsDataLoader._create_slots(df_user)
            slot_results.append(user_slots)

        df_slot = pd.concat(slot_results)

        # Second groupby operation: study_day
        unique_users_slot = df_slot["user.index"].unique()
        study_day_results = []

        for user_idx in unique_users_slot:
            df_user = df_slot[df_slot["user.index"] == user_idx]
            user_study_day = HeartStepsDataLoader._study_day(df_user)
            study_day_results.append(user_study_day)

        df_study_day = pd.concat(study_day_results)

        # create unique index
        df_final = df_study_day.set_index(["user.index", "study_day", "new_slot"])

        # transform into 4d tensor + mask
        data, mask = HeartStepsDataLoader._transform_dnn(
            df_final,
            users=self.participants,
            max_study_day=self.max_study_day,
            num_measurements=self.num_measurements,
        )
        N, T = mask.shape
        data2d = np.empty([N, T], dtype=object)
        if self.log_transform:
            data = np.log(data + 1)

        # to align with 4d structure
        data = data[:, :, :, np.newaxis]

        for i in range(N):
            for j in range(T):
                data2d[i, j] = data[i, j].flatten()
        return data, data2d, mask
