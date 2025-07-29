import json

import pandas as pd
from pandas import DataFrame

from .endpoints import Endpoints
from .session import Session
from .utils.errors import ErrorMessages
from .utils.logger import get_logger
from .utils.time import get_unix_day_bounds

logger = get_logger(__name__)


class Activities:
    """Handles activity fetching and slot management."""

    def __init__(self, session: Session) -> None:
        """Initialize the Activities class."""
        self.session = session.session
        self.headers = session.headers

    def fetch(self) -> DataFrame:
        """
        Fetch all available activities.

        Returns:
            DataFrame: A DataFrame containing activity details.

        Raises:
            RuntimeError: If the request fails.
        """
        logger.info("Fetching activities...")
        response = self.session.post(Endpoints.ACTIVITIES, headers=self.headers)

        if response.status_code != 200:
            error_msg = ErrorMessages.failed_fetch("activities")
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        try:
            activities = response.json().get("activities", {})
        except json.JSONDecodeError as err:
            error_msg = "Invalid JSON response while fetching activities."
            logger.error(error_msg)
            raise RuntimeError(error_msg) from err

        if not activities:
            logger.warning("No activities found in the response.")

        df_activities = pd.DataFrame.from_dict(activities, orient="index")
        df_activities.index = df_activities.index.astype(int)  # Ensure index is integer for consistency

        logger.info("Activities fetched successfully.")
        return df_activities

    def daily_slots(self, df_activities: DataFrame, activity_name: str, day: str) -> DataFrame:
        """
        Fetch available slots for a specific activity on a given day.

        Args:
            df_activities (DataFrame): The DataFrame of activities.
            activity_name (str): The name of the activity.
            day (str): The day in 'YYYY-MM-DD' format.

        Returns:
            DataFrame: A DataFrame containing available slots.

        Raises:
            ValueError: If the specified activity is not found.
            RuntimeError: If slots cannot be fetched.
        """
        logger.info(f"Fetching available slots for '{activity_name}' on {day}...")

        # Check if the activity exists
        activity_match = df_activities[df_activities["name_activity"] == activity_name]
        if activity_match.empty:
            error_msg = ErrorMessages.activity_not_found(
                activity_name, df_activities["name_activity"].unique().tolist()
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Extract activity ID and category ID
        # Ensures activity_id is an integer
        activity_id = activity_match.index[0]
        id_category_activity = activity_match.at[activity_id, "activityCategoryId"]

        # Get Unix timestamp bounds for the day
        unix_day_bounds = get_unix_day_bounds(day)

        # Fetch slots
        params = {
            "id_category_activity": id_category_activity,
            "start": unix_day_bounds[0],
            "end": unix_day_bounds[1],
        }
        response = self.session.get(Endpoints.SLOTS, headers=self.headers, params=params)

        if response.status_code != 200:
            error_msg = ErrorMessages.failed_fetch("slots")
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        try:
            slots = response.json()
        except json.JSONDecodeError as err:
            error_msg = "Invalid JSON response while fetching slots."
            logger.error(error_msg)
            raise RuntimeError(error_msg) from err

        if not slots:
            warning_msg = ErrorMessages.no_slots(activity_name, day)
            logger.warning(warning_msg)
            return DataFrame()

        logger.debug(f"Daily slots fetched for '{activity_name}' on {day}.")

        # Filter desired columns
        columns = [
            "name_activity",
            "id_activity_calendar",
            "id_activity",
            "id_category_activity",
            "start_timestamp",
            "end_timestamp",
            "n_inscribed",
            "capacity",
            "n_waiting_list",
            "cancelled",
            "can_join",
            "trainer",
        ]
        df_slots = pd.DataFrame(slots)

        # Ensure only desired columns are selected without KeyError
        df_slots = df_slots.loc[:, df_slots.columns.intersection(columns)]

        # Only select rows of the specified activity
        df_slots = df_slots[df_slots["id_activity"] == activity_id]
        if df_slots.empty:
            warning_msg = ErrorMessages.no_matching_slots(activity_name, day)
            logger.warning(warning_msg)
            return DataFrame()

        return df_slots
