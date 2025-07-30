#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import Optional

from datarobot.models import Model as datarobot_model
from datarobot.utils import get_id_from_response


class Model(datarobot_model):
    """Experimental model class"""

    def continue_incremental_learning_from_incremental_model(
        self, chunk_definition_id: str, early_stopping_rounds: Optional[int] = None
    ):
        """Submit a job to the queue to perform the first incremental learning iteration training on an existing
        sample model. This functionality requires the SAMPLE_DATA_TO_START_PROJECT feature flag to be enabled.

        Parameters
        ----------
        chunk_definition_id: str
            The Mongo ID for the chunking service.
        early_stopping_rounds: Optional[int]
            The number of chunks in which no improvement is observed that triggers the early stopping mechanism.

        Returns
        -------
        job : ModelJob
            The created job that is retraining the model
        """
        from ...models.modeljob import (  # pylint: disable=import-outside-toplevel,cyclic-import
            ModelJob,
        )

        url = f"projects/{self.project_id}/incrementalLearningModels/fromIncrementalModel/"
        payload = {
            "modelId": self.id,
            "chunkDefinitionId": chunk_definition_id,
        }
        if early_stopping_rounds:
            payload["earlyStoppingRounds"] = early_stopping_rounds
        response = self._client.post(url, data=payload)
        return ModelJob.from_id(self.project_id, get_id_from_response(response))
