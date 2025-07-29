from typing import Dict, List

import pandas as pd
from scipy.stats import pearsonr, spearmanr
from .md import (
    get_flac_markdown,
    get_badd_markdown,
    get_adaface_markdown,
    get_badd_json,
    get_adaface_json,
    get_flac_json,
)
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


def analysis_json(
    csv_path: str,
    task: str,
    target: str,
    sensitive: List[str],
    sp_th: float = 0.1,
    rep_th: float = 0.1,
):
    df = pd.read_csv(csv_path)
    representation_bias_result = analyze_representation_bias(df, sensitive)
    representation_bias_plot = plot_representation_bias_html(df, sensitive)
    suggestions = []
    results_dict = {"task": task, "biases": [], "mitigation": []}
    bias_threshold = rep_th
    representation_biases_found = False
    for key, value in representation_bias_result.items():
        if isinstance(value, dict):
            max_proportion = max(value.values())
            min_proportion = min(value.values())
            if max_proportion - min_proportion > bias_threshold * sum(value.values()):
                suggestions.append(
                    f"There is representation bias for {key} ({(max_proportion-min_proportion)*100:.2f}% gap between most and less represented group)."
                )
                results_dict["biases"].append(suggestions[-1])
                representation_biases_found = True

    spurious_correlations = find_spurious_correlations(df, target, sensitive, sp_th)
    spurious_correlations_found = len(spurious_correlations) > 0

    if task.lower() == "face verification":
        suggestions.append(
            "Consider using AdaFace for training a fairer face verification model."
        )
        results_dict["mitigation"].append(suggestions[-1])

    elif task.lower() == "image classification":
        if len(spurious_correlations) == 1:
            suggestions.append(
                f"There is spurious correlation of {(spurious_correlations[0][2])*100:.2f}% between {spurious_correlations[0][0]} and {spurious_correlations[0][1]}."
            )
            results_dict["biases"].append(suggestions[-1])
            results_dict["mitigation"].append(
                "Consider using the FLAC method to mitigate it."
            )
        elif len(spurious_correlations) > 1:
            for tar, sen, per in spurious_correlations:
                suggestions.append(
                    f"There is spurious correlation of {per*100:.2f}% between {tar} and {sen}."
                )
                results_dict["biases"].append(suggestions[-1])
            results_dict["mitigation"].append(
                "Given that there are multiple spurious correlations, consider using the BAdd method to mitigate it."
            )

    if len(results_dict["mitigation"]) == 0:
        results_dict["mitigation"].append(
            "Consider using the FLAC method for learning fair representations."
        )

    if representation_biases_found and not spurious_correlations_found:
        title = "Visual representation bias"
    elif spurious_correlations_found and not representation_biases_found:
        title = "Spurious correlations bias"
    elif spurious_correlations_found and representation_biases_found:
        title = "Spurious correlations and representation biases"
    else:
        title = "No issue detected"

    json_output = [
        {"type": "heading", "level": 1, "content": title},
        {
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "content": "This report analyzes the dataset for representation biases and spurious correlations, providing insights and mitigation recommendations.",
                }
            ],
        },
        {"type": "heading", "level": 3, "content": "Representation Bias"},
        {"type": "html", "content": representation_bias_plot},
    ]

    if representation_biases_found:
        paragraph = "The analysis reveals significant representation biases across several sensitive attributes. "
        bias_descriptions = []
        for key, value in representation_bias_result.items():
            if isinstance(value, dict):
                max_proportion = max(value.values())
                min_proportion = min(value.values())
                if max_proportion - min_proportion > bias_threshold * sum(
                    value.values()
                ):
                    bias_descriptions.append(
                        f"{key} exhibits a {(max_proportion-min_proportion)*100:.2f}% gap between the most and least represented groups"
                    )
        if len(bias_descriptions) > 1:
            paragraph += (
                ", ".join(bias_descriptions[:-1])
                + " and "
                + bias_descriptions[-1]
                + ". "
            )
        else:
            paragraph += bias_descriptions[0] + ". "

        paragraph += "These imbalances suggest potential biases in model training, as underrepresented groups may receive inadequate attention."
        json_output.append(
            {"type": "paragraph", "content": [{"type": "text", "content": paragraph}]}
        )
    else:
        paragraph = "The analysis indicates no significant representation biases across the sensitive attributes. The distribution of data across different groups appears to be relatively balanced, suggesting a well-represented dataset."
        json_output.append(
            {"type": "paragraph", "content": [{"type": "text", "content": paragraph}]}
        )

    json_output.append(
        {"type": "heading", "level": 3, "content": "Spurious Correlations"}
    )

    if spurious_correlations_found:
        paragraph = "Spurious correlations were identified between the target variable and several sensitive attributes. "
        correlation_descriptions = []
        for tar, sen, per in spurious_correlations:
            correlation_descriptions.append(
                f"a correlation of {per*100:.2f}% was found between {tar} and the target"
            )
        if len(correlation_descriptions) > 1:
            correlation_descriptions[0] = correlation_descriptions[0].capitalize()
            paragraph += (
                ", ".join(correlation_descriptions[:-1])
                + " and "
                + correlation_descriptions[-1]
                + ", indicating strong, potentially misleading relationships. "
            )
        else:
            correlation_descriptions[0] = correlation_descriptions[0].capitalize()
            paragraph += (
                correlation_descriptions[0]
                + ", indicating a strong, potentially misleading relationship. "
            )
        paragraph += "These correlations suggest that the model may learn to rely on these attributes, leading to biased predictions."
        json_output.append(
            {"type": "paragraph", "content": [{"type": "text", "content": paragraph}]}
        )
    else:
        paragraph = "No significant spurious correlations were found between the target variable and the sensitive attributes. This suggests that the model is unlikely to learn misleading relationships based on these attributes."
        json_output.append(
            {"type": "paragraph", "content": [{"type": "text", "content": paragraph}]}
        )

    json_output.append(
        {"type": "heading", "level": 2, "content": "Mitigation Recommendations"}
    )
    # json_output.append({"type": "paragraph", "content": f"**Task: {results_dict['task']}**"})

    if representation_biases_found or spurious_correlations_found:
        paragraph = "Given the identified representation biases and spurious correlations, several mitigation strategies are recommended. "
        if representation_biases_found:
            paragraph += "For representation bias, consider techniques such as oversampling or undersampling to balance the dataset. "
        if spurious_correlations_found:
            if len(spurious_correlations) == 1:
                paragraph += "Additionally, due to the spurious correlations, FLAC is suggested to reduce the model's reliance on these attributes. "
            else:
                paragraph += "Additionally, due to the spurious correlations, BAdd is suggested to reduce the model's reliance on these attributes. "
        if task.lower() == "face verification":
            paragraph += "For face verification tasks, AdaFace is recommended to train fairer models."
        json_output.append(
            {"type": "paragraph", "content": [{"type": "text", "content": paragraph}]}
        )

    else:
        paragraph = "Although no significant biases were detected, it is still recommended to consider FLAC for learning fair representations. This proactive approach can enhance the model's robustness and fairness."
        json_output.append(
            {"type": "paragraph", "content": [{"type": "text", "content": paragraph}]}
        )

    flac_present = any("flac" in text.lower() for text in results_dict["mitigation"])
    badd_present = any("badd" in text.lower() for text in results_dict["mitigation"])
    adaface_present = any(
        "adaface" in text.lower() for text in results_dict["mitigation"]
    )

    if flac_present:
        json_output += get_flac_json()
    elif badd_present:
        json_output += get_badd_json()
    elif adaface_present:
        json_output += get_adaface_json()

    return json_output  # json.dumps(json_output, indent=4)


def analysis_md(
    csv_path: str,
    task: str,
    target: str,
    sensitive: List[str],
    sp_th: float = 0.1,
    rep_th: float = 0.1,
):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_path)
    representation_bias_result = analyze_representation_bias(df, sensitive)

    # Provide suggestions based on the task and analysis results
    suggestions = []
    results_dict = {"task": task, "biases": [], "mitigation": []}
    bias_threshold = rep_th
    c = 0
    for key, value in representation_bias_result.items():
        if isinstance(value, dict):
            # print(value)
            max_proportion = max(value.values())
            min_proportion = min(value.values())
            if max_proportion - min_proportion > bias_threshold * sum(value.values()):
                suggestions.append(
                    f"There is representation bias for {key} ({(max_proportion-min_proportion)*100:.2f}% gap between most and less represented group)."
                )

                results_dict["biases"].append(suggestions[-1])

    sc = find_spurious_correlations(df, target, sensitive, sp_th)
    if task.lower() == "face verification":
        suggestions.append(
            "Consider using AdaFace for training a fairer face verification model."
        )
        results_dict["mitigation"].append(suggestions[-1])

    elif task.lower() == "image classification":
        if len(sc) == 1:
            suggestions.append(
                f"There is spurious correlation of {(sc[0][2])*100:.2f}% between {sc[0][0]} and {sc[0][1]}."
            )
            results_dict["biases"].append(suggestions[-1])
            results_dict["mitigation"].append(
                "Consider using the FLAC method to mitigate it."
            )
        elif len(sc) > 1:
            for tar, sen, per in sc:
                suggestions.append(
                    f"There is spurious correlation of {per*100:.2f}% between {tar} and {sen}."
                )
                results_dict["biases"].append(suggestions[-1])
            results_dict["mitigation"].append(
                "Given that there are multiple spurious correlations, consider using the BAdd method to mitigate it."
            )

    if len(results_dict["mitigation"]) == 0:
        results_dict["mitigation"].append(
            "Consider using the FLAC method for learning fair represnetations."
        )
    nl = "\n"
    markdown = f"""
# Task: {results_dict['task']}

## Biases:
{''.join([f"- {bias}{nl}" for bias in results_dict['biases']])}

## Mitigation:
{''.join([f"- {mitigation}{nl}" for mitigation in results_dict['mitigation']])}
"""
    flac_present = any("flac" in text.lower() for text in results_dict["mitigation"])
    badd_present = any("badd" in text.lower() for text in results_dict["mitigation"])
    adaface_present = any(
        "adaface" in text.lower() for text in results_dict["mitigation"]
    )

    if flac_present:
        markdown += get_flac_markdown()
    elif badd_present:
        markdown += get_badd_markdown()
    elif adaface_present:
        markdown += get_adaface_markdown()

    return markdown


def analysis(
    csv_path: str,
    task: str,
    target: str,
    sensitive: List[str],
    sp_th: float = 0.1,
    rep_th: float = 0.1,
    output: str = "md",
):
    if output == "md":
        return analysis_md(csv_path, task, target, sensitive, sp_th, rep_th)
    elif output == "json":
        return analysis_json(csv_path, task, target, sensitive, sp_th, rep_th)
    else:
        raise ValueError("ouput format should be either md or json")


def find_spurious_correlations(
    df, target_column, attribute_columns, threshold=0.01, method="pearson"
):
    """
    Finds spurious correlations between attributes and the target column in a DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing attributes and the target column.
        attribute_columns (list): List of attribute column names.
        target_column (str): The name of the target column.
        threshold (float): The threshold for correlation coefficient above which correlations are considered significant.
        method (str): The method to compute correlation. Options: 'pearson' (default) or 'spearman'.

    Returns:
        spurious_correlations (list of tuples): List of tuples containing attribute-target pairs with spurious correlations.
    """
    spurious_correlations = []

    if method == "pearson":
        corr_func = pearsonr
    elif method == "spearman":
        corr_func = spearmanr
    else:
        raise ValueError(
            "Invalid correlation method. Please choose 'pearson' or 'spearman'."
        )
    df[target_column], _ = pd.factorize(df[target_column])
    # print(df)
    for column in attribute_columns:
        codes, _ = pd.factorize(df[column])
        correlation, _ = corr_func(codes, df[target_column])
        # print(correlation)
        if abs(correlation) > threshold:
            spurious_correlations.append((column, target_column, abs(correlation)))

    return spurious_correlations


def plot_representation_bias_html(
    df: pd.DataFrame, sensitive: List[str]
) -> str:
    """
    Creates a horizontal barplot showing the distribution of intersectional groups
    defined by the given sensitive attributes, and returns it as an HTML <img> tag.
    """

    # Step 1: Create intersection key
    df['intersection'] = df[sensitive].astype(str).agg(' / '.join, axis=1)
    counts = df['intersection'].value_counts(normalize=True).sort_values(ascending=True)  # ascending for horizontal plot

    # Step 2: Adjust figure height based on number of categories
    n_groups = len(counts)
    height_per_group = 0.2
    min_height = 4
    fig_height = max(min_height, n_groups * height_per_group)

    # Step 3: Create the plot (horizontal)
    plt.figure(figsize=(8, fig_height))
    ax = sns.barplot(x=counts.values, y=counts.index, palette="muted")

    # Add proportion labels to each bar
    for i, (val, label) in enumerate(zip(counts.values, counts.index)):
        ax.text(val + 0.001, i, f"{val:.4f}", va='center')

    max_val = counts.values.max()
    plt.xlim(0, max_val + max_val*0.1)
    plt.xlabel('Proportion (%)')
    attr_label = " / ".join(sensitive)
    plt.ylabel(f"Intersection of Sensitive Attributes ({attr_label})")
    plt.title('Representation Bias by Sensitive Attribute Intersections')
    plt.tight_layout()

    # Step 4: Convert plot to HTML
    buffer = io.BytesIO()
    plt.savefig("tmp.png", bbox_inches='tight')
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()

    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    html_img = f'<img src="data:image/png;base64,{img_base64}" />'

    return html_img


def analyze_representation_bias(
    df: pd.DataFrame, sensitive: List[str]
) -> Dict[str, Dict[str, float]]:
    """
    Analyzes representation bias with respect to sensitive attributes.

    Parameters:
    csv_path (str): The path to the CSV file.
    sensitive (List[str]): A list of column names of the sensitive attributes.

    Returns:
    Dict[str, Dict[str, float]]: A dictionary with representation bias scores.
    """

    # Initialize the result dictionary
    result = {}

    # Analyze representation bias for each sensitive attribute
    for attribute in sensitive:
        attribute_counts = df[attribute].value_counts(normalize=True)
        result[attribute] = attribute_counts.to_dict()

    return result


def json_to_str_recursively(data, indent=0):
    """Converts a JSON object to a string iteratively and recursively."""
    result_str = ""

    if isinstance(data, list):
        for item in data:
            result_str += json_to_str_recursively(item, indent)
    elif isinstance(data, dict):
        if data.get("type") == "heading":
            result_str += " " * indent + f"{'#' * data['level']} {data['content']}\n"
        elif data.get("type") == "paragraph":
            content = data.get("content", [])
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "text":
                        result_str += " " * indent + item.get("content", "")
                    elif item.get("type") == "inline_code":
                        result_str += f"`{item.get('content', '')}`"
                    elif item.get("type") == "link":
                        result_str += (
                            f"[{item.get('content', '')}]({item.get('url', '')})"
                        )
                    elif item.get("type") == "code":
                        result_str += (
                            "\n"
                            + " " * (indent + 4)
                            + "```"
                            + item.get("language", "")
                            + "\n"
                        )
                        result_str += (
                            " " * (indent + 4) + item.get("content", "") + "\n"
                        )
                        result_str += " " * (indent + 4) + "```"
            else:
                result_str += " " * indent + str(content)
            result_str += "\n"  # newline after paragraph
        elif data.get("type") == "code":
            result_str += " " * indent + "```" + data.get("language", "") + "\n"
            result_str += " " * indent + data.get("content", "") + "\n"
            result_str += " " * indent + "```\n"
        elif data.get("type") == "list":
            result_str += json_to_str_recursively(data.get("content", []), indent)
        else:
            result_str += " " * indent + str(data) + "\n"
    else:
        result_str += " " * indent + str(data) + "\n"

    return result_str


# data = analysis(
#     csv_path="./data/rfw.csv",
#     task="face verification",  # "image classification",
#     target="Gender",
#     sensitive=["Gender", "Race", "Age Category"],
#     sp_th=0.01,
#     rep_th=0.01,
#     output="json",
# )
# print(data)
# print(json_to_str_recursively(data))
