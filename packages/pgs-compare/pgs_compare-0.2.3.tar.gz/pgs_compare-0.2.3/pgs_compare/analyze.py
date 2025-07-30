"""
Module for analyzing PGS across ancestry groups.
"""

import os
import logging
import json
import pandas as pd
import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


def load_ancestry_data(data_dir=None):
    """
    Load 1000 Genomes ancestry information.

    Args:
        data_dir (str, optional): Directory containing the 1000 Genomes data.
                                 Default is "data/1000_genomes" in the current directory.

    Returns:
        pandas.DataFrame: DataFrame with ancestry information
    """
    if data_dir is None:
        data_dir = os.path.join(os.getcwd(), "data", "1000_genomes")

    panel_file = os.path.join(data_dir, "integrated_call_samples_v3.20130502.ALL.panel")

    if not os.path.exists(panel_file):
        logger.error(f"Ancestry panel file not found: {panel_file}")
        return pd.DataFrame()

    panel_df = pd.read_csv(panel_file, sep="\t")
    logger.info(f"Loaded ancestry information for {len(panel_df)} samples")

    return panel_df


def load_scores(scores_file, ancestry_df=None):
    """
    Load PGS and merge with ancestry information.

    Args:
        scores_file (str): Path to the scores file (aggregated_scores.txt.gz)
        ancestry_df (pandas.DataFrame, optional): DataFrame with ancestry information.
                                               If None, it will be loaded.

    Returns:
        pandas.DataFrame: DataFrame with scores and ancestry information
    """
    if not os.path.exists(scores_file):
        logger.error(f"Scores file not found: {scores_file}")
        return pd.DataFrame()

    scores_df = pd.read_csv(scores_file, sep="\t")
    scores_df["SUM"] = scores_df["SUM"].round(8)
    logger.info(f"Loaded {len(scores_df)} score entries")

    # Ensure we have ancestry information
    if ancestry_df is None or ancestry_df.empty:
        ancestry_df = load_ancestry_data()

    if ancestry_df.empty:
        logger.warning("Could not load ancestry information")
        scores_df["GROUP"] = "UNKNOWN"
        return scores_df

    # Map sample IDs to ancestry groups
    scores_df["GROUP"] = scores_df["IID"].map(
        ancestry_df.set_index("sample")["super_pop"]
    )

    # Clean up PGS IDs to remove any suffixes
    scores_df["PGS"] = scores_df["PGS"].str.split("_").str[0]

    logger.info(f"Merged scores with ancestry information")
    return scores_df


def calculate_summary_statistics(scores_df):
    """
    Calculate summary statistics for PGS by ancestry group and PGS study.

    Args:
        scores_df (pandas.DataFrame): DataFrame with scores and ancestry information

    Returns:
        dict: Dictionary with summary statistics
    """
    sorted_groups = sorted(list(scores_df["GROUP"].unique()) + ["ALL"])
    pgs_ids = scores_df["PGS"].unique()

    summary_stats = {}

    for pgs_id in pgs_ids:
        if pgs_id not in summary_stats:
            summary_stats[pgs_id] = {}

        for group in sorted_groups:
            # Get scores for this PGS and ancestry group
            group_scores = (
                scores_df[scores_df["PGS"] == pgs_id]
                if group == "ALL"
                else scores_df[
                    (scores_df["PGS"] == pgs_id) & (scores_df["GROUP"] == group)
                ]
            )

            # Calculate summary statistics
            summary_stats[pgs_id][group] = {
                "mean": group_scores["SUM"].mean() if not group_scores.empty else None,
                "median": (
                    group_scores["SUM"].median() if not group_scores.empty else None
                ),
                "std": group_scores["SUM"].std() if not group_scores.empty else None,
                "min": group_scores["SUM"].min() if not group_scores.empty else None,
                "max": group_scores["SUM"].max() if not group_scores.empty else None,
                "count": len(group_scores) if not group_scores.empty else 0,
            }

    logger.info(f"Calculated summary statistics for {len(pgs_ids)} PGS studies")
    return summary_stats


def standardize_scores(scores_df):
    """
    Standardize scores within each ancestry group for each PGS study.

    Args:
        scores_df (pandas.DataFrame): DataFrame with scores and ancestry information

    Returns:
        pandas.DataFrame: DataFrame with added z-score column
    """
    # Make a copy to avoid modifying the original
    scores_df = scores_df.copy()

    # Initialize z-score column
    scores_df["z_score"] = np.nan

    # Build deterministic list of groups: ALL first, then sorted ancestry groups
    # Important: ALL is not included
    sorted_groups = sorted(list(scores_df["GROUP"].unique()))

    # Standardize within each ancestry group for each PGS
    for pgs_id in scores_df["PGS"].unique():
        for group in sorted_groups:
            # Create mask for this PGS and specific ancestry group
            mask = (scores_df["PGS"] == pgs_id) & (scores_df["GROUP"] == group)

            group_scores = scores_df.loc[mask, "SUM"]

            # Calculate z-scores within this ancestry group if there are scores
            if len(group_scores) > 0:
                scores_df.loc[mask, "z_score"] = (
                    group_scores - group_scores.mean()
                ) / group_scores.std()
            else:
                logger.warning(f"No scores for {pgs_id} in {group}")

    logger.info("Standardized scores within ancestry groups")
    return scores_df


def calculate_correlations(scores_df):
    """
    Calculate correlations between PGS studies within each ancestry group.

    Args:
        scores_df (pandas.DataFrame): DataFrame with scores and ancestry information

    Returns:
        dict: Dictionary with correlation matrices by ancestry group
    """
    # Get unique ancestry groups
    sorted_groups = sorted(list(scores_df["GROUP"].unique()) + ["ALL"])

    # Calculate correlations for each ancestry group
    correlations = {}
    average_correlations = {}

    for group in sorted_groups:
        # Get scores for this ancestry group
        group_data = (
            scores_df if group == "ALL" else scores_df[scores_df["GROUP"] == group]
        )

        if len(group_data) == 0:
            logger.warning(f"No data for ancestry group {group}")
            continue

        # Create a pivot table: rows=individuals, columns=PGS IDs, values=scores
        try:
            pivot_data = group_data.pivot(index="IID", columns="PGS", values="SUM")

            # Calculate correlation matrix
            corr_matrix = pivot_data.corr()

            # Save correlation matrix and average correlation
            correlations[group] = corr_matrix.to_dict()

            # Calculate mean of all correlations (excluding self-correlations on diagonal)
            mask = ~np.eye(corr_matrix.shape[0], dtype=bool)
            corr_values = corr_matrix.values[mask]

            # Calculate average correlation and standard deviation
            avg_correlation = float(corr_values.mean())
            std_correlation = float(corr_values.std())

            # Store average and standard deviation
            average_correlations[group] = {
                "mean": avg_correlation,
                "std": std_correlation,
                "min": float(corr_values.min()),
                "max": float(corr_values.max()),
                "count": len(corr_values),
            }

        except Exception as e:
            logger.warning(f"Error calculating correlations for group {group}: {e}")
            correlations[group] = {}
            average_correlations[group] = {
                "mean": None,
                "std": None,
                "min": None,
                "max": None,
                "count": 0,
            }

    logger.info(f"Calculated correlations for {len(correlations)} ancestry groups")
    return {"correlations": correlations, "average_correlations": average_correlations}


def calculate_levene_test(variance_by_group, test_name="overall"):
    """
    Perform Levene's test for equal variances across ancestry groups.

    Args:
        variance_by_group (dict): Dictionary mapping group names to arrays of individual variances
        test_name (str): Name/description of what is being tested (for logging)

    Returns:
        dict: Dictionary with Levene's test results including statistic, p-value, and interpretation
    """
    levene_test_results = {}

    if len(variance_by_group) >= 2:
        try:
            # Prepare data for Levene's test
            variance_groups = [
                variances
                for variances in variance_by_group.values()
                if len(variances) > 0
            ]
            group_names = [
                group
                for group, variances in variance_by_group.items()
                if len(variances) > 0
            ]

            if len(variance_groups) >= 2:
                # Perform Levene's test (using median as center)
                levene_statistic, levene_p_value = stats.levene(
                    *variance_groups, center="median"
                )

                levene_test_results = {
                    "statistic": float(levene_statistic),
                    "p_value": float(levene_p_value),
                    "groups_tested": group_names,
                }

                logger.info(
                    f"Levene's test ({test_name}) p-value: {levene_p_value:.4f}"
                )
            else:
                logger.warning(
                    f"Insufficient groups with data for Levene's test ({test_name})"
                )
                levene_test_results = {
                    "statistic": None,
                    "p_value": None,
                    "groups_tested": [],
                }
        except Exception as e:
            logger.error(f"Error performing Levene's test ({test_name}): {e}")
            levene_test_results = {
                "statistic": None,
                "p_value": None,
                "groups_tested": [],
            }
    else:
        logger.warning(f"Insufficient ancestry groups for Levene's test ({test_name})")
        levene_test_results = {
            "statistic": None,
            "p_value": None,
            "groups_tested": [],
        }

    return levene_test_results


def calculate_variance(scores_df):
    """
    Calculate variance of z-scores for each individual across PGS studies,
    then average these variances within each ancestry group.

    This measures how consistently individuals are ranked by different PGS studies.
    Lower variance indicates more stable predictions across PGS models.

    Also calculates PGS variance - the variance of each PGS's predictions from the
    "true" z-score (average of all PGS for each individual).

    Additionally performs Levene's test to test for statistically significant
    differences in variance between ancestry groups.

    Args:
        scores_df (pandas.DataFrame): DataFrame with scores and ancestry information

    Returns:
        dict: Dictionary with variance information by ancestry group and PGS,
              including Levene's test results
    """
    sorted_groups = sorted(list(scores_df["GROUP"].unique()) + ["ALL"])

    # Initialize result dictionaries
    individual_variance = {}
    pgs_variance = {}

    # Dictionaries to map variances back to scores_df
    individual_variance_map = {}  # Maps (IID, GROUP) to individual variance

    # Dictionary to collect individual variances for Levene's test
    variance_by_group = {}

    # Dictionary to collect PGS-specific variances for individual Levene's tests
    pgs_variance_by_group = {}  # Structure: {pgs_id: {group: [variances]}}

    for group in sorted_groups:
        # Get scores for this ancestry group
        group_data = (
            scores_df if group == "ALL" else scores_df[scores_df["GROUP"] == group]
        )

        if len(group_data) == 0:
            logger.warning(f"No data for ancestry group {group}")
            continue

        # Create pivot table with individuals as rows and PGS IDs as columns
        pivot_data = group_data.pivot_table(
            index="IID", columns="PGS", values="z_score", aggfunc="first"
        )

        # Calculate "true" z-score for each individual (average across all PGS)
        true_zscores = pivot_data.mean(axis=1)

        # Calculate variance for each individual across all PGS
        individual_variances = pivot_data.var(axis=1)

        # Store individual variances for Levene's test (excluding ALL group)
        if group != "ALL":
            variance_by_group[group] = individual_variances.dropna().values

        # Store mapping of each individual's variance
        for iid, variance in individual_variances.items():
            individual_variance_map[(iid, group)] = variance

        # Calculate summary statistics for this group
        individual_variance[group] = {
            "average_variance": float(individual_variances.mean()),
            "median_variance": float(individual_variances.median()),
            "std_variance": float(individual_variances.std()),
            "max_variance": float(individual_variances.max()),
            "min_variance": float(individual_variances.min()),
            "count": len(individual_variances),
        }

        pgs_variance[group] = {}

        for pgs in pivot_data.columns:
            # Calculate squared differences between this PGS's scores and true scores
            squared_diffs = (pivot_data[pgs] - true_zscores) ** 2

            # Calculate mean of squared differences (MSE)
            mse = squared_diffs.mean()

            # Store the result
            pgs_variance[group][pgs] = {
                "variance": float(mse),
                "rmse": float(np.sqrt(mse)),
                "mean_abs_diff": float((pivot_data[pgs] - true_zscores).abs().mean()),
                "count": len(squared_diffs),
            }

            # Collect individual PGS variances for Levene's test (excluding ALL group)
            if group != "ALL":
                if pgs not in pgs_variance_by_group:
                    pgs_variance_by_group[pgs] = {}

                # For each PGS, collect the squared differences (individual variances from consensus)
                pgs_variance_by_group[pgs][group] = squared_diffs.dropna().values

    # Perform overall Levene's test for equal variances across ancestry groups
    levene_test_results = calculate_levene_test(
        variance_by_group, "overall individual variance"
    )

    # Perform individual Levene's tests for each PGS
    pgs_levene_tests = {}
    for pgs_id in pgs_variance_by_group:
        pgs_levene_tests[pgs_id] = calculate_levene_test(
            pgs_variance_by_group[pgs_id], f"PGS {pgs_id} variance"
        )

    # Add individual variance column
    scores_df["individual_variance"] = scores_df.apply(
        lambda row: individual_variance_map.get((row["IID"], row["GROUP"]), np.nan),
        axis=1,
    )

    logger.info(
        f"Calculated z-score variances for {len(individual_variance)} ancestry groups"
    )
    logger.info(
        f"Performed Levene's tests for {len(pgs_levene_tests)} individual PGS studies"
    )

    return {
        "individual_variance": individual_variance,
        "pgs_variance": pgs_variance,
        "levene_test": levene_test_results,
        "pgs_levene_tests": pgs_levene_tests,
    }


def analyze_scores(trait_id=None, scores_file=None, data_dir=None, output_dir=None):
    """
    Analyze PGS across ancestry groups.

    Args:
        trait_id (str, optional): Trait ID. Used for organizing output if provided.
        scores_file (str, optional): Path to the scores file (aggregated_scores.txt.gz).
                                   If None, will look in the standard location based on trait_id.
        data_dir (str, optional): Directory containing the 1000 Genomes data.
                                Default is "data/1000_genomes" in the current directory.
        output_dir (str, optional): Directory to store analysis results.
                                  Default is "results/[trait_id]" in the current directory.

    Returns:
        dict: Dictionary with analysis results
    """
    # Set up directories
    if data_dir is None:
        data_dir = os.path.join(os.getcwd(), "data", "1000_genomes")

    if output_dir is None:
        if trait_id is not None:
            output_dir = os.path.join(os.getcwd(), "results", trait_id, "analysis")
        else:
            output_dir = os.path.join(os.getcwd(), "results", "analysis")

    os.makedirs(output_dir, exist_ok=True)

    # Determine scores file path if not provided
    if scores_file is None:
        if trait_id is not None:
            scores_file = os.path.join(
                os.getcwd(),
                "results",
                trait_id,
                "results",
                "ALL",
                "score",
                "aggregated_scores.txt.gz",
            )

        else:
            logger.error("Could not find scores file")
            return {"success": False, "error": "Scores file not found"}

        if not os.path.exists(scores_file):
            logger.error("Could not find scores file")
            return {"success": False, "error": "Scores file not found"}

    # Load ancestry data
    ancestry_df = load_ancestry_data(data_dir)

    if ancestry_df.empty:
        return {"success": False, "error": "Could not load ancestry data"}

    # Load scores
    scores_df = load_scores(scores_file, ancestry_df)

    if scores_df.empty:
        return {"success": False, "error": "Could not load scores data"}

    # Run analyses
    results = {
        "trait_id": trait_id,
        "summary_statistics": calculate_summary_statistics(scores_df),
        "success": True,
    }

    # Standardize scores
    scores_df = standardize_scores(scores_df)

    # Calculate correlations
    correlation_results = calculate_correlations(scores_df)
    results["correlations"] = correlation_results["correlations"]
    results["average_correlations"] = correlation_results["average_correlations"]

    # Calculate variance
    variance_results = calculate_variance(scores_df)
    results["individual_variance"] = variance_results["individual_variance"]
    results["pgs_variance"] = variance_results["pgs_variance"]
    results["levene_test"] = variance_results["levene_test"]
    results["pgs_levene_tests"] = variance_results["pgs_levene_tests"]

    # Save results to JSON files
    for key in results.keys():
        output_file = os.path.join(output_dir, f"{key}.json")
        with open(output_file, "w") as f:
            json.dump(results[key], f, indent=2)

    # Also save the standardized scores for potential further analysis
    scores_output = os.path.join(output_dir, "standardized_scores.csv")
    scores_df.to_csv(scores_output, index=False)

    logger.info(f"Analysis completed and results saved to {output_dir}")

    # Add output path to results
    results["output_path"] = output_dir

    return results
