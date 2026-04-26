from __future__ import annotations

from pathlib import Path
import re

import pandas as pd


YEARBOOK_CORE_SPECS = {
    2019: {
        "gdp": "中国城市统计年鉴2020（excel）/中国城市统计年鉴2020（excel）/二、地级以上城市统计资料/2-9_地区生产总值.xlsx",
        "industry": "中国城市统计年鉴2020（excel）/中国城市统计年鉴2020（excel）/二、地级以上城市统计资料/2-10_地区生产总值构成.xlsx",
        "population": "中国城市统计年鉴2020（excel）/中国城市统计年鉴2020（excel）/二、地级以上城市统计资料/2-1_人口及户数.xlsx",
        "fiscal": "中国城市统计年鉴2020（excel）/中国城市统计年鉴2020（excel）/二、地级以上城市统计资料/2-11_地方一般公共预算收支状况(全市).xlsx",
    },
    2020: {
        "gdp": "中国城市统计年鉴2021（excel）/中国城市统计年鉴2021（excel）/二、地级以上城市统计资料/2-7_地区生产总值.xlsx",
        "industry": "中国城市统计年鉴2021（excel）/中国城市统计年鉴2021（excel）/二、地级以上城市统计资料/2-8_地区生产总值构成.xlsx",
        "population": "中国城市统计年鉴2021（excel）/中国城市统计年鉴2021（excel）/二、地级以上城市统计资料/2-1_人口数.xlsx",
        "fiscal": "中国城市统计年鉴2021（excel）/中国城市统计年鉴2021（excel）/二、地级以上城市统计资料/2-9_地方一般公共预算收支状况(全市).xlsx",
    },
    2021: {
        "gdp": "中国城市统计年鉴2022（excel）/中国城市统计年鉴2022（excel）/二、地级以上城市统计资料/2-7_地区生产总值.xlsx",
        "industry": "中国城市统计年鉴2022（excel）/中国城市统计年鉴2022（excel）/二、地级以上城市统计资料/2-8_地区生产总值构成.xlsx",
        "population": "中国城市统计年鉴2022（excel）/中国城市统计年鉴2022（excel）/二、地级以上城市统计资料/2-1_人口数.xlsx",
        "fiscal": "中国城市统计年鉴2022（excel）/中国城市统计年鉴2022（excel）/二、地级以上城市统计资料/2-9_地方一般公共预算收支状况(全市).xlsx",
    },
    2022: {
        "gdp": "中国城市统计年鉴2023（excel）/中国城市统计年鉴2023（excel）/2、地级以上城市统计资料/2-7_地区生产总值.xlsx",
        "industry": "中国城市统计年鉴2023（excel）/中国城市统计年鉴2023（excel）/2、地级以上城市统计资料/2-8_地区生产总值构成.xlsx",
        "population": "中国城市统计年鉴2023（excel）/中国城市统计年鉴2023（excel）/2、地级以上城市统计资料/2-1_人口数.xlsx",
        "fiscal": "中国城市统计年鉴2023（excel）/中国城市统计年鉴2023（excel）/2、地级以上城市统计资料/2-9_地方一般公共预算收支状况(全市).xlsx",
    },
    2023: {
        "gdp": "中国城市统计年鉴2024（excel）/中国城市统计年鉴2024（excel）/2、地级以上城市统计资料/2-6_地区生产总值.xlsx",
        "industry": "中国城市统计年鉴2024（excel）/中国城市统计年鉴2024（excel）/2、地级以上城市统计资料/2-7_地区生产总值构成.xlsx",
        "population": "中国城市统计年鉴2024（excel）/中国城市统计年鉴2024（excel）/2、地级以上城市统计资料/2-1_人口数.xlsx",
        "fiscal": "中国城市统计年鉴2024（excel）/中国城市统计年鉴2024（excel）/2、地级以上城市统计资料/2-8_地方一般公共预算收支状况(全市).xlsx",
    },
}


def _clean_header_text(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).replace("_x000D_", " ")
    text = re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
    return text


def _is_data_row(values: list[object]) -> bool:
    if len(values) < 2:
        return False
    first = _clean_header_text(values[0])
    second = _clean_header_text(values[1])
    if not first or not second:
        return False
    if "city" in second.lower() or "地区生产总值" in first or "人口" in first:
        return False
    return bool(re.search(r"[\u4e00-\u9fff]", first)) and bool(re.search(r"[A-Za-z]", second))


def read_yearbook_table_with_flat_headers(path: str | Path) -> pd.DataFrame:
    preview = pd.read_excel(path, header=None, nrows=12)
    data_start = None
    for idx, row in preview.iterrows():
        if _is_data_row(row.tolist()):
            data_start = idx
            break
    if data_start is None:
        raise ValueError(f"Could not locate first data row in {path}")

    header_rows = preview.iloc[:data_start].fillna("")
    flattened_headers: list[str] = []
    for col_idx in range(preview.shape[1]):
        parts: list[str] = []
        for value in header_rows.iloc[:, col_idx].tolist():
            cleaned = _clean_header_text(value)
            if cleaned and cleaned not in parts:
                parts.append(cleaned)
        flattened_headers.append(" | ".join(parts) if parts else f"col_{col_idx}")

    data = pd.read_excel(path, header=None, skiprows=data_start)
    data = data.iloc[:, : len(flattened_headers)].copy()
    data.columns = flattened_headers
    return data


def _find_column(columns: list[str], patterns: list[str]) -> str:
    for column in columns:
        normalized = column.lower()
        if all(pattern.lower() in normalized for pattern in patterns):
            return column
    raise KeyError(f"Could not find column matching patterns={patterns}")


def normalize_city_name_cn(name: object) -> str:
    if pd.isna(name):
        return ""
    text = str(name).replace("\u3000", " ")
    text = re.sub(r"\s+", "", text)
    return text.strip()


def extract_gdp_table(path: str | Path, stats_year: int) -> pd.DataFrame:
    frame = read_yearbook_table_with_flat_headers(path)
    columns = list(frame.columns)
    city_cn = columns[0]
    city_en = columns[1]
    gdp_col = _find_column(columns, ["地区生产总值", "total city"])
    result = frame[[city_cn, city_en, gdp_col]].copy()
    result.columns = ["city_name_cn", "city_name_en", "gdp_total"]
    result["year"] = stats_year
    return result


def extract_secondary_industry_table(path: str | Path, stats_year: int) -> pd.DataFrame:
    frame = read_yearbook_table_with_flat_headers(path)
    columns = list(frame.columns)
    city_cn = columns[0]
    city_en = columns[1]
    industry_col = _find_column(columns, ["第二产业", "total city"])
    result = frame[[city_cn, city_en, industry_col]].copy()
    result.columns = ["city_name_cn", "city_name_en", "secondary_industry_share"]
    result["year"] = stats_year
    return result


def extract_population_table(path: str | Path, stats_year: int) -> pd.DataFrame:
    frame = read_yearbook_table_with_flat_headers(path)
    columns = list(frame.columns)
    city_cn = columns[0]
    city_en = columns[1]
    population_col = _find_column(columns, ["total city"])
    population_candidates = [
        column for column in columns if "total city" in column.lower() and ("常住人口" in column or "户籍人口" in column)
    ]
    if not population_candidates:
        population_candidates = [population_col]
    result = frame[[city_cn, city_en, population_candidates[0]]].copy()
    result.columns = ["city_name_cn", "city_name_en", "population_raw"]
    result["year"] = stats_year
    return result


def extract_fiscal_table(path: str | Path, stats_year: int) -> pd.DataFrame:
    frame = read_yearbook_table_with_flat_headers(path)
    columns = list(frame.columns)
    city_cn = columns[0]
    city_en = columns[1]
    fiscal_col = None
    for column in columns:
        normalized = column.lower()
        if "预算支出" in normalized or "public budget expenditure" in normalized:
            fiscal_col = column
            break
    if fiscal_col is None:
        raise KeyError(f"Could not find fiscal expenditure column in {path}")
    result = frame[[city_cn, city_en, fiscal_col]].copy()
    result.columns = ["city_name_cn", "city_name_en", "fiscal_expenditure"]
    result["year"] = stats_year
    return result


def build_core_controls_panel(root_dir: str | Path, pku_city_reference: pd.DataFrame) -> pd.DataFrame:
    root = Path(root_dir)
    tables: list[pd.DataFrame] = []
    reference = pku_city_reference.copy()
    reference["city_name_cn_norm"] = reference["pku_city_name_cn"].astype(str).map(normalize_city_name_cn)
    pku_names = set(reference["city_name_cn_norm"])

    for stats_year, spec in YEARBOOK_CORE_SPECS.items():
        gdp = extract_gdp_table(root / spec["gdp"], stats_year)
        industry = extract_secondary_industry_table(root / spec["industry"], stats_year)
        population = extract_population_table(root / spec["population"], stats_year)
        fiscal = extract_fiscal_table(root / spec["fiscal"], stats_year)

        merged = (
            gdp.merge(industry, on=["city_name_cn", "city_name_en", "year"], how="outer")
            .merge(population, on=["city_name_cn", "city_name_en", "year"], how="outer")
            .merge(fiscal, on=["city_name_cn", "city_name_en", "year"], how="outer")
        )
        merged["city_name_cn"] = merged["city_name_cn"].map(normalize_city_name_cn)
        merged = merged.loc[merged["city_name_cn"].isin(pku_names)].copy()
        merged = merged.merge(
            reference[["city_name_cn_norm", "pku_city_code", "pku_city_name_cn", "pku_city_name_eng"]].drop_duplicates(),
            left_on="city_name_cn",
            right_on="city_name_cn_norm",
            how="left",
            validate="many_to_one",
        ).drop(columns=["city_name_cn_norm"])
        tables.append(merged)

    combined = pd.concat(tables, ignore_index=True)
    aggregated = (
        combined.groupby(["pku_city_code", "year"], as_index=False)
        .agg(
            yearbook_city_name_cn=("city_name_cn", lambda series: next((value for value in series if pd.notna(value)), None)),
            city_name_en=("city_name_en", lambda series: next((value for value in series if pd.notna(value)), None)),
            gdp_total=("gdp_total", lambda series: next((value for value in series if pd.notna(value)), None)),
            secondary_industry_share=(
                "secondary_industry_share",
                lambda series: next((value for value in series if pd.notna(value)), None),
            ),
            population_raw=("population_raw", lambda series: next((value for value in series if pd.notna(value)), None)),
            fiscal_expenditure=(
                "fiscal_expenditure",
                lambda series: next((value for value in series if pd.notna(value)), None),
            ),
            pku_city_name_cn=("pku_city_name_cn", lambda series: next((value for value in series if pd.notna(value)), None)),
            pku_city_name_eng=("pku_city_name_eng", lambda series: next((value for value in series if pd.notna(value)), None)),
        )
    )
    return aggregated.sort_values(["year", "pku_city_code"]).reset_index(drop=True)
