# Type hinting for better code readability and function definitions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .DataPreProcessor import DataPreProcessor

class FeatureTargetSplitMixin:
    # Splits the DataFrame into features and target variable
    def _feature_target_split(self) -> "DataPreProcessor":
        """
        Splits the DataFrame into features and target variable.
        """

        # Extract features and target without modifying self.working_df
        self.features_df = self.working_df.drop(columns=self.target_variable)
        self.target_df = self.working_df[self.target_variable]

        # Convert to Series if only one target column
        if len(self.target_variable) == 1:
            self.target_df = self.target_df.iloc[:, 0]  # Convert DataFrame to Series