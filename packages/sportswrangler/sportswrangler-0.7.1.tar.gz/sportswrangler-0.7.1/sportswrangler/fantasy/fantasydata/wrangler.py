from sportswrangler.generic.wrangler import Wrangler
import os
import zipfile
import requests
import pandas as pd
import polars as pl
from typing import List, Optional
import logging
from sportswrangler.utils.enums import Sport

logger = logging.getLogger(__name__)


class FantasyDataWrangler(Wrangler):
    _endpoint = "https://sportsdata.io/members/download-file"
    # Doesn't matter, not used for anything
    sport: Sport = Sport.NFL

    def get_data(
        self,
        path: str,
        file_types: List[str],
        years: List[int],
        product_key: Optional[str] = None,
        force: bool = False,
    ) -> dict:
        """
        Download and extract fantasy data files

        Args:
            path: Directory to extract files to
            file_types: List of file types to extract
            years: List of years to get data for
            product_key: Optional product key for authentication
            force: If True, force download even if files exist

        Returns:
            Dictionary mapping filenames to their dataframes (pandas or polars based on preferred_dataframe setting)
        """
        # Create directories if they don't exist
        os.makedirs(path, exist_ok=True)

        zip_path = os.path.join(path, "data.zip")
        extract_path = os.path.join(path, "extracted")

        # Check if we need to download
        need_download = not os.path.exists(zip_path) or force
        need_extract = (
            need_download
            or not os.path.exists(extract_path)
            or not os.listdir(extract_path)
        )

        if need_download:
            if not product_key:
                raise ValueError("Product key required for downloading files")

            # Download zip file
            logger.info("Downloading zip file...")
            response = self.session.get(self._endpoint, params={"product": product_key})
            response.raise_for_status()

            with open(zip_path, "wb") as f:
                f.write(response.content)
            logger.info("Download complete")

        if need_extract:
            logger.info("Extracting zip file...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
            logger.info("Extraction complete")

        # Process requested files
        dataframes = {}
        # Generate file patterns for each file type and year
        file_patterns = [
            f"{file_type}.{year}.csv" for file_type in file_types for year in years
        ]

        for pattern in file_patterns:
            file_path = os.path.join(extract_path, pattern)
            if os.path.exists(file_path):
                logger.info(f"Processing file: {pattern}")
                try:
                    # Load file contents into appropriate dataframe type
                    if self.preferred_dataframe == "pandas":
                        dataframes[pattern] = pd.read_csv(file_path)
                    elif self.preferred_dataframe == "polars":
                        dataframes[pattern] = pl.read_csv(file_path, infer_schema_length=1000000)
                    else:
                        raise ValueError(
                            "preferred_dataframe must be either 'pandas' or 'polars'"
                        )
                    logger.info(f"Loaded {pattern} successfully")
                except Exception as e:
                    logger.warning(f"Failed to load {pattern}: {e}")
            else:
                logger.warning(f"File not found: {file_path}")

        if not dataframes:
            raise FileNotFoundError("No files were loaded successfully")

        return dataframes
