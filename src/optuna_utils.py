from pathlib import Path

import joblib
import optuna
import torch
from optuna.trial import TrialState

from src.constants import get_default_params
from src.optimize_utils import process_every_gift

NUM_TRIALS = 100
TIMEOUT_IN_SECONDS = 3600

COLUMN_SEPARATOR = "|"
LINE_BREAK = "\n"


def make_dummy_row(dummy_string, num_columns):
    return (
        f"{COLUMN_SEPARATOR}{dummy_string}" * num_columns
        + f"{COLUMN_SEPARATOR}{LINE_BREAK}"
    )


def count_columns(string):
    return string.count(COLUMN_SEPARATOR) - 1


def my_objective(
    trial,
    egs_solutions: dict,
    pre_computed_palettes: torch.tensor,
    pre_computed_app_ids: list[str],
    params: dict,
) -> float:
    if params is None:
        params = get_default_params()
    params["factor_ramp"] = trial.suggest_float(
        "factor_ramp",
        -1.0,
        1.0,
        step=0.01,
    )
    params["factor_source"] = trial.suggest_float(
        "factor_source",
        -1.0,
        1.0,
        step=0.01,
    )
    params["factor_target"] = trial.suggest_float(
        "factor_target",
        -1.0,
        1.0,
        step=0.01,
    )

    # Check whether we already evaluated the sampled parameters.
    # https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-ignore-duplicated-samples
    states_to_consider = (TrialState.COMPLETE,)
    try:
        trials_to_consider = trial.study.get_trials(
            deepcopy=False,
            states=states_to_consider,
        )
    except AttributeError:
        trials_to_consider = []
    for t in reversed(trials_to_consider):
        if trial.params == t.params:
            # Use the existing value as trial duplicated the parameters.
            return t.value

    print(f"Parameters: {params}")
    print(f"Number of gift wrappings: {len(egs_solutions['gift'])}")

    gift_ranks = process_every_gift(
        egs_solutions,
        pre_computed_palettes,
        pre_computed_app_ids,
        [],
        params,
        verbose=False,
    )

    ranks = torch.Tensor([r for r in gift_ranks if r is not None])
    score = ranks.min() + ranks.median() + ranks.mean() + ranks.max()

    param_str = "| Factor R      | Factor S      | Factor T  "
    rank_str = "| Min Rank     | Median Rank   | Mean Rank     | Max Rank  "
    score_str = "| Score (sum)  |\n"
    header_row = f"{param_str}{rank_str}{score_str}"

    param_values_str = f"| {params['factor_ramp']:.2f} | {params['factor_source']:.2f} | {params['factor_target']:.2f} "
    rank_values_str = f"| {ranks.min():.0f}    | {ranks.median():.0f}  | {ranks.mean():.2f}    | {ranks.max():.0f} "
    score_values_str = f"| {score:.2f}  |\n"
    values_row = f"{param_values_str}{rank_values_str}{score_values_str}"

    num_columns = count_columns(header_row)

    print(
        header_row,
        make_dummy_row("-", num_columns),
        values_row,
        make_dummy_row(" ", num_columns),
        sep="",
    )

    print("\n---\n")

    return score


def run_study(
    objective,
    num_trials: int = NUM_TRIALS,
    timeout_in_seconds: int = TIMEOUT_IN_SECONDS,
    study_fname: str = "",
    previous_study=None,
):
    if previous_study is not None:
        study = previous_study
    elif study_fname and Path(study_fname).exists():
        study = joblib.load(study_fname)
        # https://optuna.readthedocs.io/en/stable/faq.html#how-can-i-save-and-resume-studies
        print("Best trial until now:")
        print(" Value: ", study.best_trial.value)
        print(" Params: ")
        for key, value in study.best_trial.params.items():
            print(f"    {key}: {value}")
    else:
        study = optuna.create_study()

    study.optimize(objective, n_trials=num_trials, timeout=timeout_in_seconds)
    print(f"Best params is {study.best_params} with value {study.best_value}")

    if study_fname:
        joblib.dump(study, study_fname)

    return study
