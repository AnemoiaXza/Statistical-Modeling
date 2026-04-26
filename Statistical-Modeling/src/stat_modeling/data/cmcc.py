from __future__ import annotations

from calendar import isleap
from collections import defaultdict
from pathlib import Path
import re

import pandas as pd


CMCC_USECOLS = ["city", "date", "sector", "value"]

OBVIOUS_FOREIGN_CITIES = {
    "Amsterdam",
    "Bangkok",
    "Barcelona",
    "Berlin",
    "Bogota",
    "Cape Town",
    "Chicago",
    "Copenhagen",
    "Helsinki",
    "Houston",
    "Istanbul",
    "London",
    "Los Angeles",
    "Lyon",
    "Madrid",
    "Marseille",
    "Melbourne",
    "Mexico City",
    "Miami",
    "Milan",
    "Moscow",
    "Munich",
    "New Delhi",
    "New York",
    "Nice",
    "Osaka",
    "Oslo",
    "Paris",
    "Rome",
    "San Francisco",
    "Santiago",
    "Seattle",
    "Seoul",
    "Singapore",
    "Stockholm",
    "Sydney",
    "Tokyo",
    "Toronto",
    "Vienna",
    "Warsaw",
    "Washington",
}

MANUAL_CITY_ALIASES = {
    "Baoding": ("baoji", "保定市", 1306),
    "Baoji": ("baoji", "宝鸡市", 6103),
    "Bayin'gholin Mongol": ("Bayinguoling", "巴音郭楞蒙古自治州", 6528),
    "Baynnur": ("Bayannaoer", "巴彦淖尔市", 1508),
    "Chamdo": ("Changdu", "昌都市", 5403),
    "Dêqên Tibetan": ("Diqing", "迪庆藏族自治州", 5334),
    "Fuzhou_jiangxi": ("Fuzhou", "抚州市", 3610),
    "Garzê Tibetan": ("Ganzi", "甘孜藏族自治州", 5133),
    "Golog Tibetan": ("Guoluo", "果洛藏族自治州", 6326),
    "Gyêgu Tibetan": ("Yushu", "玉树藏族自治州", 6327),
    "Honghe Hani and Yi": ("Honghe", "红河哈尼族彝族自治州", 5325),
    "Ili Kazakh": ("Yili", "伊犁哈萨克自治州", 6540),
    "Jiyuan shi": ("Jiyuan", "济源市", 4190),
    "Kashgar": ("Kashi", "喀什地区", 6531),
    "Kizilsu Kirghiz": ("Kizilesu Kirgiz", "克孜勒苏柯尔克孜自治州", 6530),
    "Nyingtri": ("Linzhi", "林芝市", 5404),
    "Qiandongnan Miao and Dong": ("Qiandongnan", "黔东南苗族侗族自治州", 5226),
    "Shangqiu": ("Shangqiu", "商丘市", 4114),
    "Shaoguan": ("Shaoguan", "韶关市", 4402),
    "Suzhou": ("Suzhou", "苏州市", 3205),
    "Suzhou_anhui": ("Suzhou", "宿州市", 3413),
    "Taizhou": ("Taizhou", "台州市", 3310),
    "Taizhou_jiangsu": ("Taizhou", "泰州市", 3212),
    "Fuzhou": ("Fuzhou", "福州市", 3501),
    "Ürümqi": ("Urumqi", "乌鲁木齐市", 6501),
    "Wenshan Zhuang and Miao": ("Wenshan", "文山壮族苗族自治州", 5326),
    "Xing'an": ("Hinggan", "兴安盟", 1522),
    "Xishuangbanna Dai": ("Xishuangbanna", "西双版纳傣族自治州", 5328),
    "Yichun": ("Yichun", "宜春市", 3609),
    "Yichun_heilongjiang": ("Yichun", "伊春市", 2307),
    "Yulin": ("Yulin", "玉林市", 4509),
    "Yulin_shanxi": ("Yulin", "榆林市", 6108),
    "Maoming": ("Maoming", "茂名市", 4409),
    "Ngawa Tibetan and Qiang": ("Aba", "阿坝藏族羌族自治州", 5132),
}

MANUAL_UNMATCHED_OVERRIDES = {
    "Hainan",
}


def normalize_city_name_for_match(name: str) -> str:
    normalized = name.strip().lower()
    normalized = normalized.replace("_", " ")
    normalized = normalized.replace("'", "")
    normalized = normalized.replace("-", " ")
    normalized = re.sub(r"\s+", " ", normalized)

    replacements = {
        "mongol and tibetan": "",
        "mongol": "",
        "tibetan and qiang": "",
        "tibetan": "",
        "yi": "",
        "hui": "",
        "kazakh": "",
        "kirghiz": "",
        "kirgiz": "",
        "dai and jingpo": "",
        "tujia and miao": "",
        "buyei and miao": "",
        "hani and yi": "",
        "bai": "",
        "lisu": "",
        "zhuang and miao": "",
        "korean": "",
        "shi": "",
    }
    for source, target in replacements.items():
        normalized = normalized.replace(source, target)

    special_cases = {
        "daxinganling": "da hinggan ling",
        "bayinngholin": "bayinguoling",
        "bortala": "börtala",
        "lvliang": "luliang",
        "maanshan": "ma anshan",
        "ji an": "jian",
        "ji'an": "jian",
        "pu'er": "puer",
        "qiqihaer": "qiqihar",
        "urumqi": "urumchi",
        "kashi": "kashgar",
        "hetian": "khotan",
        "naqu": "nagchu",
        "ali": "ngari",
        "linzhi": "nyingtri",
        "sanmingshi": "sanming",
        "sanshashi": "sansha",
        "taian": "tai'an",
        "nnaning": "nanning",
        "ulanchab": "ulaan chab",
        "xilin gol": "xilingol",
        "xiangfan": "xiangyang",
        "turfan": "turpan",
    }
    for source, target in special_cases.items():
        normalized = normalized.replace(source, target)

    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def build_match_candidates(
    cmcc_cities: list[str],
    pku_reference: pd.DataFrame,
) -> pd.DataFrame:
    reference = pku_reference.copy()
    reference["pref_name_year18_eng"] = reference["pref_name_year18_eng"].astype(str)
    reference["norm_name"] = reference["pref_name_year18_eng"].map(normalize_city_name_for_match)

    grouped_candidates: dict[str, list[tuple[str, str, int]]] = defaultdict(list)
    direct_candidates: dict[str, list[tuple[str, str, int]]] = defaultdict(list)
    for _, row in reference.iterrows():
        candidate = (
            row["pref_name_year18_eng"],
            row["pref_name_year18"],
            int(row["pref_code_year18"]),
        )
        grouped_candidates[row["norm_name"]].append(candidate)
        direct_candidates[row["pref_name_year18_eng"]].append(candidate)

    rows: list[dict[str, object]] = []
    for city in sorted(cmcc_cities):
        norm_name = normalize_city_name_for_match(city)
        candidates = grouped_candidates.get(norm_name, [])
        direct_matches = direct_candidates.get(city, [])
        manual_alias = MANUAL_CITY_ALIASES.get(city)
        if city in OBVIOUS_FOREIGN_CITIES:
            match_status = "unmatched"
            candidate_count = 0
            candidate_eng = ""
            candidate_cn = ""
            candidate_code = ""
        elif city in MANUAL_UNMATCHED_OVERRIDES:
            match_status = "unmatched"
            candidate_count = 0
            candidate_eng = ""
            candidate_cn = ""
            candidate_code = ""
        elif manual_alias is not None:
            candidate_eng, candidate_cn, candidate_code = manual_alias
            match_status = "manual_alias"
            candidate_count = 1
        elif len(direct_matches) == 1:
            candidate_eng, candidate_cn, candidate_code = direct_matches[0]
            match_status = "direct"
            candidate_count = 1
        elif len(direct_matches) > 1:
            candidate_eng = " | ".join(candidate[0] for candidate in direct_matches)
            candidate_cn = " | ".join(candidate[1] for candidate in direct_matches)
            candidate_code = " | ".join(str(candidate[2]) for candidate in direct_matches)
            match_status = "ambiguous"
            candidate_count = len(direct_matches)
        elif len(candidates) == 1:
            candidate_eng, candidate_cn, candidate_code = candidates[0]
            match_status = "normalized_candidate"
            candidate_count = len(candidates)
        elif len(candidates) > 1:
            candidate_eng = " | ".join(candidate[0] for candidate in candidates)
            candidate_cn = " | ".join(candidate[1] for candidate in candidates)
            candidate_code = " | ".join(str(candidate[2]) for candidate in candidates)
            match_status = "ambiguous"
            candidate_count = len(candidates)
        else:
            match_status = "unmatched"
            candidate_count = len(candidates)
            candidate_eng = ""
            candidate_cn = ""
            candidate_code = ""

        rows.append(
            {
                "cmcc_city": city,
                "norm_city": norm_name,
                "direct_match": len(direct_matches) == 1,
                "candidate_count": candidate_count,
                "candidate_eng": str(candidate_eng),
                "candidate_cn": str(candidate_cn),
                "candidate_code": str(candidate_code),
                "is_obvious_foreign": city in OBVIOUS_FOREIGN_CITIES,
                "match_status": match_status,
            }
        )

    return pd.DataFrame(rows)


def annualize_total_emissions(
    frame: pd.DataFrame,
    expected_days_by_year: dict[int, int] | None = None,
) -> pd.DataFrame:
    working = frame.copy()
    working["date"] = pd.to_datetime(working["date"])
    working["year"] = working["date"].dt.year
    total_rows = working.loc[working["sector"] == "Total", ["city", "date", "year", "value"]]
    grouped = (
        total_rows.groupby(["city", "year"], as_index=False)
        .agg(
            annual_total_value=("value", "sum"),
            observed_days=("date", "nunique"),
        )
        .sort_values(["city", "year"])
        .reset_index(drop=True)
    )
    if expected_days_by_year is None:
        expected_days_by_year = {year: 366 if isleap(year) else 365 for year in grouped["year"].unique()}
    grouped["expected_days"] = grouped["year"].map(expected_days_by_year)
    grouped["is_complete_year"] = grouped["observed_days"] == grouped["expected_days"]
    return grouped.loc[grouped["is_complete_year"]].reset_index(drop=True)


def collect_unique_cities(cmcc_path: str | Path, chunksize: int = 250_000) -> list[str]:
    cities: set[str] = set()
    for chunk in pd.read_csv(cmcc_path, usecols=["city"], chunksize=chunksize):
        cities.update(chunk["city"].dropna().astype(str))
    return sorted(cities)


def annualize_total_emissions_from_csv(
    cmcc_path: str | Path,
    max_year: int | None = 2024,
    chunksize: int = 250_000,
) -> pd.DataFrame:
    sums: dict[tuple[str, int], float] = defaultdict(float)
    counts: dict[tuple[str, int], int] = defaultdict(int)

    for chunk in pd.read_csv(cmcc_path, usecols=CMCC_USECOLS, chunksize=chunksize):
        total = chunk.loc[chunk["sector"] == "Total", ["city", "date", "value"]].copy()
        total["date"] = pd.to_datetime(total["date"])
        total["year"] = total["date"].dt.year
        if max_year is not None:
            total = total.loc[total["year"] <= max_year]

        grouped = (
            total.groupby(["city", "year"], as_index=False)
            .agg(annual_total_value=("value", "sum"), observed_days=("date", "nunique"))
        )
        for _, row in grouped.iterrows():
            key = (row["city"], int(row["year"]))
            sums[key] += float(row["annual_total_value"])
            counts[key] += int(row["observed_days"])

    result = pd.DataFrame(
        [
            {
                "city": city,
                "year": year,
                "annual_total_value": sums[(city, year)],
                "observed_days": counts[(city, year)],
            }
            for city, year in sorted(sums)
        ]
    )
    if result.empty:
        return result

    result["expected_days"] = result["year"].map(lambda year: 366 if isleap(year) else 365)
    result["is_complete_year"] = result["observed_days"] == result["expected_days"]
    return result.loc[result["is_complete_year"]].reset_index(drop=True)


def build_resolved_annualized_panel(
    annualized: pd.DataFrame,
    match_candidates: pd.DataFrame,
) -> pd.DataFrame:
    matched = match_candidates.loc[
        match_candidates["match_status"].isin(["direct", "normalized_candidate", "manual_alias"])
    ].copy()
    matched = matched.loc[~matched["is_obvious_foreign"]].copy()
    matched["pku_city_name_eng"] = matched["candidate_eng"]
    matched["pku_city_name_cn"] = matched["candidate_cn"]
    matched["pku_city_code"] = matched["candidate_code"].astype(str)
    merged = annualized.merge(matched, left_on="city", right_on="cmcc_city", how="inner")
    return merged[
        [
            "city",
            "year",
            "annual_total_value",
            "observed_days",
            "expected_days",
            "is_complete_year",
            "pku_city_name_eng",
            "pku_city_name_cn",
            "pku_city_code",
            "match_status",
            "is_obvious_foreign",
        ]
    ].sort_values(["pku_city_code", "year", "city"]).reset_index(drop=True)
