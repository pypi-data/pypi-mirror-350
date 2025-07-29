import json
import os
import logging
import math
import numbers

from typing import List, Dict
from teradataml.analytics.valib import *
from teradataml import DataFrame
from tmo.context.model_context import ModelContext
from tmo.stats.stats_util import (
    _capture_stats,
    _NpEncoder,
    _parse_scoring_stats,
    _compute_continuous_edges,
)

logger = logging.getLogger(__name__)


def record_training_stats(
    df: DataFrame,
    features: List[str],
    targets: List[str] = [],
    categorical: List[str] = [],
    context: ModelContext = {},
    feature_importance: Dict[str, float] = {},
    **kwargs,
) -> Dict:
    """
    Compute and record the dataset statistics used for training. This information provides ModelOps with a snapshot
    of the dataset at this point in time (i.e. at the point of training). ModelOps uses this information for data and
    prediction drift monitoring. It can also be used for data quality monitoring as all of the information which is
    captured here is available to configure an alert on (e.g. max > some_threshold).

    Depending on the type of variable (categorical or continuous), different statistics and distributions are computed.
    All of this is computed in Vantage via the Vantage Analytics Library (VAL).

    Continuous Variable:
        Distribution: Histogram
        Statistics: Min, Max, Average, Skew, etc, nulls

    Categorical Variable:
        Distribution: Frequency
        Statistics: nulls

    The following example shows how you would use this function for a binary classification problem where the there
    are 3 features and 1 target. As it is classification, the target must be categorical and in this case, the features
    are all continuous.
    example usage:
        training_df = DataFrame.from_query("SELECT * from my_table")

        record_training_stats(training_df,
                              features=["feat1", "feat2", "feat3"],
                              targets=["targ1"],
                              categorical=["targ1"],
                              context=context)

    :param df: teradataml dataframe used for training with the feature and target variables
    :type df: teradataml.DataFrame
    :param features: feature variable(s) used in this training
    :type features: List[str]
    :param targets: target variable(s) used in this training
    :type targets: List[str]
    :param categorical: variable(s) (feature or target) that is categorical
    :type categorical: List[str]
    :param context: ModelContext which is associated with that training invocation
    :type context: ModelContext
    :param feature_importance: (Optional) feature importance
    :type feature_importance: Dict[str, float]
    :return: the computed data statistics
    :rtype: Dict
    :raise ValueError: if features or targets are not provided
    :raise TypeError: if df is not of type teradataml.DataFrame
    """

    logger.info("Computing training dataset statistics")

    if not features:
        raise ValueError("One or more features must be provided")

    # backward compatibility for when we had targets incorrectly named predictors.. remove in future version
    if "predictors" in kwargs:
        logger.warning(
            "Usage of `predictors` as argument to `record_training_stats` is"
            " deprecated. "
        )
        targets = kwargs.pop("predictors")

    if not targets:
        logger.warning(
            "One or more targets are not provided to collect training statistics, make"
            " sure this is what you want."
        )

    feature_metadata_fqtn = None
    feature_metadata_group = None
    data_stats_filename = "artifacts/output/data_stats.json"

    if context:
        feature_metadata_fqtn = context.dataset_info.get_feature_metadata_fqtn()
        feature_metadata_group = context.dataset_info.feature_metadata_monitoring_group
        data_stats_filename = os.path.join(
            context.artifact_output_path, "data_stats.json"
        )

    data_stats = _capture_stats(
        df=df,
        features=features,
        targets=targets,
        categorical=categorical,
        feature_importance=feature_importance,
        feature_metadata_fqtn=feature_metadata_fqtn,
        feature_metadata_group=feature_metadata_group,
    )

    with open(data_stats_filename, "w+") as f:
        json.dump(data_stats, f, indent=2, cls=_NpEncoder)

    return data_stats


def record_evaluation_stats(
    features_df: DataFrame,
    predicted_df: DataFrame,
    feature_importance: Dict[str, float] = {},
    context: ModelContext = None,
    **kwargs,
) -> Dict:
    """
    Compute and record the dataset statistics used for evaluation. This information provides ModelOps with a snapshot
    of the dataset at this point in time (i.e. at the point of evaluation). ModelOps uses this information for data
    and prediction drift monitoring. It can also be used for data quality monitoring as all of the information which
    is captured here is available to configure an alert on (e.g. max > some_threshold).

    Depending on the type of variable (categorical or continuous), different statistics and distributions are computed.
    All of this is computed in Vantage via the Vantage Analytics Library (VAL).

    Continuous Variable:
        Distribution: Histogram
        Statistics: Min, Max, Average, Skew, etc, nulls

    Categorical Variable:
        Distribution: Frequency
        Statistics: nulls

    example usage:
        features_df = DataFrame.from_query("SELECT * from my_features_table")

        predicted_df = model.predict(features_df)

        record_evaluation_stats(features_df=features_df,
                                predicted_df=predicted_df,
                                context=context)

    :param features_df: dataframe containing feature variable(s) from evaluation
    :type features_df: teradataml.DataFrame
    :param predicted_df: dataframe containing predicted target variable(s) from evaluation
    :type predicted_df: teradataml.DataFrame
    :param context: ModelContext which is associated with that training invocation
    :type context: ModelContext
    :param feature_importance: (Optional) feature importance
    :type feature_importance: Dict[str, float]
    :return: the computed data statistics
    :rtype: Dict
    :raise ValueError: if the number of predictions (rows) do not match the number of features (rows)
    :raise TypeError: if features_df or predicted_df is not of type teradataml.DataFrame
    """

    logger.info("Computing evaluation dataset statistics")

    feature_metadata_fqtn = None
    feature_metadata_group = None
    output_data_stats_filename = "artifacts/output/data_stats.json"
    input_data_stats_filename = "artifacts/input/data_stats.json"

    if context:
        feature_metadata_fqtn = context.dataset_info.get_feature_metadata_fqtn()
        feature_metadata_group = context.dataset_info.feature_metadata_monitoring_group
        output_data_stats_filename = os.path.join(
            context.artifact_output_path, "data_stats.json"
        )
        input_data_stats_filename = os.path.join(
            context.artifact_input_path, "data_stats.json"
        )

    with open(input_data_stats_filename, "r") as f:
        training_data_stats = json.load(f)

    data_stats = _parse_scoring_stats(
        features_df=features_df,
        predicted_df=predicted_df,
        data_stats=training_data_stats,
        feature_importance=feature_importance,
        feature_metadata_fqtn=feature_metadata_fqtn,
        feature_metadata_group=feature_metadata_group,
    )

    # for evaluation, the core will do it (we may change this later to unify)..
    with open(output_data_stats_filename, "w+") as f:
        json.dump(data_stats, f, indent=2, cls=_NpEncoder)

    return data_stats


def record_scoring_stats(
    features_df: DataFrame, predicted_df: DataFrame, context: ModelContext = None
) -> Dict:
    """
    Compute and record the dataset statistics used for scoring. This information provides ModelOps with a snapshot
    of the dataset at this point in time (i.e. at the point of scoring). ModelOps uses this information for data
    and prediction drift monitoring. It can also be used for data quality monitoring as all of the information which
    is captured here is available to configure an alert on (e.g. max > some_threshold).

    Depending on the type of variable (categorical or continuous), different statistics and distributions are computed.
    All of this is computed in Vantage via the Vantage Analytics Library (VAL).

    Continuous Variable:
        Distribution: Histogram
        Statistics: Min, Max, Average, Skew, etc, nulls

    Categorical Variable:
        Distribution: Frequency
        Statistics: nulls

    example usage:
        features_df = DataFrame.from_query("SELECT * from my_features_table")

        predicted_df = model.predict(features_df)

        record_scoring_stats(features_df=features_df,
                            predicted_df=predicted_df,
                            context=context)

    :param features_df: dataframe containing feature variable(s) from evaluation
    :type features_df: teradataml.DataFrame
    :param predicted_df: dataframe containing predicted target variable(s) from evaluation
    :type predicted_df: teradataml.DataFrame
    :param context: ModelContext which is associated with that training invocation
    :type context: ModelContext
    :return: the computed data statistics
    :rtype: Dict
    :raise ValueError: if the number of predictions (rows) do not match the number of features (rows)
    :raise TypeError: if features_df or predicted_df is not of type teradataml.DataFrame
    """

    logger.info("Computing scoring dataset statistics")

    feature_metadata_fqtn = None
    feature_metadata_group = None
    input_data_stats_filename = "artifacts/input/data_stats.json"

    if context:
        feature_metadata_fqtn = context.dataset_info.get_feature_metadata_fqtn()
        feature_metadata_group = context.dataset_info.feature_metadata_monitoring_group
        input_data_stats_filename = os.path.join(
            context.artifact_input_path, "data_stats.json"
        )
        output_data_stats_filename = os.path.join(
            context.artifact_output_path, "data_stats.json"
        )

    with open(input_data_stats_filename, "r") as f:
        training_data_stats = json.load(f)

    data_stats = _parse_scoring_stats(
        features_df=features_df,
        predicted_df=predicted_df,
        data_stats=training_data_stats,
        feature_metadata_fqtn=feature_metadata_fqtn,
        feature_metadata_group=feature_metadata_group,
    )

    # for evaluation, the core will do it (we may change this later to unify)..
    with open(output_data_stats_filename, "w+") as f:
        json.dump(data_stats, f, indent=2, cls=_NpEncoder)

    return data_stats


def compute_continuous_stats(features_df: DataFrame, continuous_features: List[str]):
    """This function computes bin edges for continuous features. Only numeric columns are used,
    others are ignored with warning. For each column it computes maximum and minimum values, and
    attempts to split the difference into 10 bins. If only smaller number is possile - it generates
    the maximum number (e.g. integer column with minimum 5 and maximum 10 generates only 5 bins).
    The column has to have at least two distinct values, otherwise the column is ignored.

    Args:
        features_df (DataFrame): Teradata DataFrame used to compute statistics metadata
        continuous_features (List): list of columns representing continuous features

    Returns:
        dict: Dictionary with keys corresponding to requested features, and values containing edges
    """
    dtypes = {r[0].lower(): r[1] for r in features_df.dtypes._column_names_and_types}

    # Numeric types in teradata are represented as either int, or float or decimal.Decimal,
    # so other columns shall be ignored
    # COLUMN NAME	TYPE
    # int_column	int
    # byte_column	int
    # smallint_column	int
    # decimal_column	decimal.Decimal
    # numeric_column	decimal.Decimal
    # float_column	float
    # real_column	float
    # double_precision_column	float
    # number_column	decimal.Decimal
    lowered_features = list(map(str.lower, continuous_features))
    features = []
    for f in lowered_features:
        if (
            dtypes[f].startswith("decimal")
            or dtypes[f].startswith("float")
            or dtypes[f].startswith("int")
        ):
            features.append(f)
        else:
            logger.warning(
                f"Column {f} has a type {dtypes[f]} which is not compatible with"
                " continuous feature types. This column will be ignored."
            )

    logger.debug(
        "Executing this VAL"
        f" {valib.Statistics(data=features_df, columns=features, stats_options='all', charset='UTF8').show_query()}"
    )
    stats = valib.Statistics(
        data=features_df, columns=features, stats_options="all", charset="UTF8"
    )
    stats = stats.result.to_pandas(all_rows=True).reset_index()
    stats["xcol"] = stats["xcol"].str.lower()
    stats = stats.set_index("xcol", drop=False)

    non_trivial_features = []
    for f in features:
        if stats.loc[f].loc["xcnt"] == 0:
            logger.warning(f"Feature {f} has only NULL values, ignored")
        elif stats.loc[f].loc["xmin"] == stats.loc[f].loc["xmax"]:
            logger.warning(
                f"Feature {f} doesn't have enough unique values to be considered"
                " continuous feature (needs at least two distinct not null values),"
                " ignored"
            )
        else:
            non_trivial_features.append(f)

    bins = 10  # Default number of bins; if data doesn't allow 10 bins - we generate the maximum number allowed
    reference_edges = _compute_continuous_edges(
        non_trivial_features, stats, dtypes, bins=bins
    )
    edges_dict = dict(zip(non_trivial_features, reference_edges))

    for variable_name, edges in edges_dict.items():
        if len(edges) < bins:
            logger.warning(
                f"Variable {variable_name} has only {len(edges)} bins computed when"
                f" {bins} should have been computed {edges}.\nPlease ensure the"
                " variable is not categorical (use -t categorical)."
            )

    column_stats = {}
    for f in edges_dict.keys():
        column_stats[f.lower()] = {"edges": edges_dict[f]}

    if len(column_stats) == 0:
        raise Exception(
            f"No columns with computable statistics metadata were found, please see"
            f" warning messages above"
        )

    return column_stats


def compute_categorical_stats(features_df: DataFrame, categorical_features: List[str]):
    """This function computes frequencies for categorical features. Each column must have at least one non-NULL value,
    all NULL columns are ignored. NULL value is ignored in frequencies (number of NULLs is reported for every
    training/evaluation/scoring jobs).

    Args:
        features_df (DataFrame): Teradata DataFrame used to compute statistics metadata
        categorical_features (List): list of columns representing categorical features

    Returns:
        dict: Dictionary with keys corresponding to requested features, and values containing frequencies
    """
    logger.debug(
        "Executing this VAL"
        f" {valib.Frequency(data=features_df, columns=categorical_features, charset='UTF8').show_query()}"
    )
    statistics = valib.Frequency(
        data=features_df, columns=categorical_features, charset="UTF8"
    )
    statistics = statistics.result.to_pandas(all_rows=True).reset_index()
    statistics = statistics.drop(
        statistics.columns.difference(["xcol", "xval", "xpct"]), axis=1
    )
    statistics["xcol"] = statistics["xcol"].str.lower()
    statistics = (
        statistics.groupby("xcol")
        .apply(lambda x: dict(zip(x["xval"], x["xpct"])))
        .to_dict()
    )

    lowered_features = list(map(str.lower, categorical_features))
    features = list(lowered_features)
    for f in features:
        values_list = list(statistics[f].keys())
        for k in values_list:
            if isinstance(k, numbers.Number):
                if math.isnan(k):
                    logger.warning(
                        f"Categorical feature {f} has NULL values in reference table,"
                        " NULLs will be ignored"
                    )
                    del statistics[f][k]
        if not statistics[f]:
            logger.warning(
                f"Categorical feature {f} has only NULL values in reference table, no"
                " statistics metadata generated"
            )
            lowered_features.remove(f)

    column_stats = {
        f: {"categories": list(statistics[f].keys())} for f in lowered_features
    }

    return column_stats
