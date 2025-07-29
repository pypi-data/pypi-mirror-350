import asyncio
from pathlib import Path
import os
from crypticorn.hive import (
    ApiClient,
    Configuration,
    ModelsApi,
    DataApi,
    StatusApi,
    Configuration,
    AdminApi,
    DataVersion,
    FeatureSize,
)
from crypticorn.hive.utils import download_file
from typing import Optional
from pydantic import StrictInt


class DataApiWrapper(DataApi):
    """
    A wrapper for the DataApi class.
    """

    async def download_data(
        self,
        model_id: StrictInt,
        folder: Path = Path("data"),
        version: Optional[DataVersion] = None,
        feature_size: Optional[FeatureSize] = None,
        *args,
        **kwargs,
    ) -> list[Path]:
        """
        Download data for model training. All three files (y_train, x_test, x_train) are downloaded and saved under e.g. FOLDER/v1/coin_1/*.feather.
        The folder will be created if it doesn't exist.

        :param model_id: Model ID (required) (type: int)
        :param version: Data version. Default is the latest public version. (optional) (type: DataVersion)
        :param feature_size: The number of features in the data. Default is LARGE. (optional) (type: FeatureSize)
        :return: A list of paths to the downloaded files.
        """
        response = await super().download_data(
            model_id=model_id,
            version=version,
            feature_size=feature_size,
            *args,
            **kwargs,
        )
        base_path = f"{folder}/v{response.version.value}/coin_{response.coin.value}/"
        os.makedirs(base_path, exist_ok=True)

        return await asyncio.gather(
            *[
                download_file(
                    url=response.links.y_train,
                    dest_path=base_path + "y_train_" + response.target + ".feather",
                ),
                download_file(
                    url=response.links.x_test,
                    dest_path=base_path
                    + "x_test_"
                    + response.feature_size
                    + ".feather",
                ),
                download_file(
                    url=response.links.x_train,
                    dest_path=base_path
                    + "x_train_"
                    + response.feature_size
                    + ".feather",
                ),
            ]
        )


class HiveClient:
    """
    A client for interacting with the Crypticorn Hive API.
    """

    config_class = Configuration

    def __init__(
        self,
        config: Configuration,
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.models = ModelsApi(self.base_client)
        self.data = DataApiWrapper(self.base_client)
        self.status = StatusApi(self.base_client)
        self.admin = AdminApi(self.base_client)
