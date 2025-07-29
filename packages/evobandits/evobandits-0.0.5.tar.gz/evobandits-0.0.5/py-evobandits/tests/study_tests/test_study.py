# Copyright 2025 EvoBandits
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from contextlib import nullcontext
from unittest.mock import create_autospec

import pytest
from evobandits import ALGORITHM_DEFAULT, EvoBandits, Study

from tests._functions import clustering as cl
from tests._functions import rosenbrock as rb


def test_algorithm_default():
    # the default algorithm should always be a new Evobandits instance without modifications
    assert ALGORITHM_DEFAULT == EvoBandits()


@pytest.mark.parametrize(
    "seed, kwargs, exp_algorithm",
    [
        [None, {"log": ("WARNING", "No seed provided")}, ALGORITHM_DEFAULT],
        [42, {}, ALGORITHM_DEFAULT],
        [42.0, {"exp": pytest.raises(TypeError)}, ALGORITHM_DEFAULT],
    ],
    ids=[
        "default",
        "default_with_seed",
        "fail_seed_type",
    ],
)
def test_study_init(seed, kwargs, exp_algorithm, caplog):
    # Extract expected exceptions and logs
    expectation = kwargs.pop("exp", nullcontext())
    log = kwargs.pop("log", None)

    # Initialize a Study and verify its properties
    with expectation:
        study = Study(seed, **kwargs)
        assert study.seed == seed
        assert study.algorithm == exp_algorithm
        assert study.objective is None
        assert study.params is None

        if log:
            level, msg = log
            matched = any(
                record.levelname == level and msg in record.message for record in caplog.records
            )
            assert matched, f"Expected {level} log containing '{msg}'"


@pytest.mark.parametrize(
    "objective, params, trials, kwargs",
    [
        [rb.function, rb.PARAMS, 1, {}],
        [
            cl.function,
            cl.PARAMS,
            2,
            {"n_best": 2, "optimize_ret": cl.ARMS_EXAMPLE, "exp_result": cl.TRIALS_EXAMPLE},
        ],
        [rb.function, rb.PARAMS, 1, {"maximize": True}],
        [rb.function, rb.PARAMS, 1, {"maximize": "False", "exp": pytest.raises(TypeError)}],
    ],
    ids=[
        "valid_default_testcase",
        "valid_clustering_testcase",
        "default_with_maximize",
        "invalid_maximize_type",
    ],
)
def test_optimize(objective, params, trials, kwargs):
    # Mock dependencies
    # Per default, and expected results from the rosenbrock testcase are used to mock EvoBandits.
    mock_algorithm = create_autospec(EvoBandits, instance=True)
    mock_algorithm.optimize.return_value = kwargs.pop("optimize_ret", rb.ARM_BEST)
    exp_result = kwargs.pop("exp_result", rb.TRIAL_BEST)
    study = Study(seed=42, algorithm=mock_algorithm)  # seeding to avoid warning log

    # Extract expected exceptions
    expectation = kwargs.pop("exp", nullcontext())

    # Optimize a study and verify results
    with expectation:
        result = study.optimize(objective, params, trials, **kwargs)
        assert result == exp_result
        assert mock_algorithm.optimize.call_count == 1  # Always run algorithm once for now
