from typing import Dict, List

import Levenshtein
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from util_intelligence.char_util import chinese_punctuation_to_english, normalize_char_text
from util_intelligence.regex import replace_multiple_spaces


def _compare_value(pred_value, tag_value):
    def normalize_number_value(value):
        try:
            float_value = float(value.replace(',', ''))
            int_value = int(float_value)
            if float_value == int_value:
                return str(int_value)
            else:
                return str(float_value)
        except Exception:
            return value

    def normalize_value(value: str):
        value = str(value).strip().lower()
        value = replace_multiple_spaces(value)
        value = normalize_char_text(value)
        value = chinese_punctuation_to_english(value)
        value = normalize_number_value(value)
        return value

    pred_value = normalize_value(pred_value.rstrip('*'))
    tag_value = normalize_value(tag_value)
    similarity = Levenshtein.ratio(pred_value, tag_value)
    return similarity


def _compare_record(
    pred_record,
    tag_record,
    exclusion_keys=[],
    i=0,
    pred_name="pred",
    tag_name="tag",
):
    for key in exclusion_keys:
        pred_record.pop(key, None)
        tag_record.pop(key, None)

    record_compare: List[Dict] = []
    for field in tag_record.keys():
        field_compare: Dict = {'no': i}
        field_compare['field'] = field
        pred_value = pred_record[field] if pred_record.get(field) else ''
        tag_value = tag_record[field] if tag_record.get(field) else ''
        field_compare[pred_name] = pred_value
        field_compare[tag_name] = tag_value
        field_compare['similarity'] = _compare_value(pred_value, tag_value)
        record_compare.append(field_compare)
    return record_compare


def _compare_table_result(
    pred: List[Dict[str, str]],
    tag: List[Dict[str, str]],
    exclusion_keys: List[str],
    pred_name="pred",
    tag_name="tag",
) -> List[List]:
    compare: List[List] = []
    for i, (pred_record, tag_record) in enumerate(zip(pred, tag)):
        record_compare = _compare_record(
            pred_record,
            tag_record,
            exclusion_keys=exclusion_keys,
            i=i,
            pred_name=pred_name,
            tag_name=tag_name,
        )
        compare.append(record_compare)
    return compare


def compare_table_result(
    pred,
    tag,
    exclusion_keys=[],
    pred_name="pred",
    tag_name="tag",
):
    if not tag:
        tag = []

    if not pred:
        pred = []

    if isinstance(pred, dict):
        pred = [pred]

    if isinstance(tag, dict):
        tag = [tag]

    if len(pred) < len(tag):
        for i in range(len(pred), len(tag)):
            pred.append({})
    elif len(pred) > len(tag):
        for i in range(len(tag), len(pred)):
            tag.append({})

    compare = _compare_table_result(
        pred,
        tag,
        exclusion_keys=exclusion_keys,
        pred_name=pred_name,
        tag_name=tag_name,
    )
    return compare


compare_records = compare_table_result


def compare_kv_result(pred, tag, exclusion_keys=[]):
    return _compare_record(pred, tag, exclusion_keys=exclusion_keys)


def aggregate_by_fields_and_calculate_accuracy(
    df, fields=['field']
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """按照文件类型和字段聚类，计算 Accuracy"""
    filtered_df = df

    # 各个字段的数量
    df_grouped = (
        filtered_df.groupby(fields)
        .count()
        .reindex(columns=['similarity'])
        .rename(columns={'similarity': 'total_count'})
    )

    # 相似度为 1 的各个文件类型各个字段的数量
    matched_df_grouped = (
        filtered_df[filtered_df['similarity'] == 1]
        .groupby(fields)
        .count()
        .reindex(columns=['similarity'])
        .rename(columns={'similarity': 'exact_match_count'})
    )

    # exact_match_count / total_count
    aggregated_df = pd.merge(df_grouped, matched_df_grouped, on=fields, how='left')
    aggregated_df['total_count'] = aggregated_df['total_count'].fillna(0)
    aggregated_df['total_count'] = aggregated_df['total_count'].astype(int)
    aggregated_df['exact_match_count'] = aggregated_df['exact_match_count'].fillna(0)
    aggregated_df['exact_match_count'] = aggregated_df['exact_match_count'].astype(int)
    aggregated_df['accuracy'] = aggregated_df['exact_match_count'] / aggregated_df['total_count']
    return df_grouped, matched_df_grouped, aggregated_df


def save_Xs_Ys(Xs, Ys, file_path: str):
    with open(file_path, 'a') as f:
        for x, y in zip(Xs, Ys):
            f.write(f'{x} {y}\n')


def read_Xs_Ys(file_path: str):
    Xs = []
    Ys = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            x, y = line.split()
            Xs.append(int(x))
            Ys.append(float(y))
    return Xs, Ys


def plot_scatter_and_fitted_polynomial(
    Xs,
    Ys,
    title='Actual Data vs Fitted Polynomial',
    x_label='Xs',
    y_label='Ys',
    fit=True,
    legend=True,
    figsize=(10, 6),
):
    plt.figure(figsize=figsize)
    plt.scatter(Xs, Ys, marker='o', color='b', label='Actual Data', alpha=0.3)

    if fit:
        # 拟合二次多项式
        coefficients = np.polyfit(Xs, Ys, 2)
        polynomial = np.poly1d(coefficients)

        # 遍历 Xs, 去掉重复的 x
        fitted_Ys = polynomial(Xs)
        _Xs, _Ys = [], []
        for x, y in zip(Xs, fitted_Ys):
            if x not in _Xs:
                _Xs.append(x)
                _Ys.append(y)
        plt.plot(_Xs, _Ys, color='r', label='Fitted Polynomial')

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if legend:
        plt.legend()
    plt.grid(True)
    plt.show()
