# Statistical Modeling Competition Project

## Overview

This repository contains the implementation workflow for the 2026 statistical modeling competition topic:

"Dual-carbon strategy and the carbon reduction effect of digital economy: causal inference and heterogeneity analysis based on double machine learning."

The project uses a `B-lite` structure:

- Numbered scripts under `src/` map to research steps.
- Reusable logic lives in `src/stat_modeling/`.
- Policy-text features remain an auxiliary mechanism/moderation lane; they do not replace the main identification design.

## Setup

Create the conda environment:

```bash
conda env create -f environment.yml
conda activate stat-modeling
```

## Reproducibility

- Global random seed: `RANDOM_SEED = 42`
- Required directories are managed by `stat_modeling.config.ensure_project_directories()`
- Policy-text artifacts are stored under `data/interim/policy_text`, `data/processed/policy_text`, and `logs/policy_text`
- Raw HTML pages and downloaded attachments are organized beneath `data/interim/policy_text/raw_html` and `data/interim/policy_text/attachments`

## Policy Text Module

Use the policy-text scaffold when you need reproducible document discovery, normalization, rule extraction, scoring payload preparation, and `city-year` aggregation for the approved double-carbon corpus window.

```bash
python3 src/08_policy_text.py --help
```

## Planned Run Order

1. `src/01_data_clean.py`
2. `src/02_dea_efficiency.py`
3. `src/03_eda.py`
4. `src/04_dml_main.py`
5. `src/05_heterogeneity.py`
6. `src/06_robustness.py`
7. `src/07_spatial.py` (optional)
8. `src/08_policy_text.py` (mechanism/moderation support lane)

## Policy-text corpus lane

Use the policy-text scaffold to prepare the corpus workspace and record the expected pipeline stage:

```bash
python3 src/08_policy_text.py --help
python3 src/08_policy_text.py --stage discover --dry-run
```

Current scaffold behavior:

- creates the policy-text interim / processed / log folders when missing
- writes a UTF-8 summary under `logs/policy_text/`
- keeps the policy-text module scoped to mechanism and moderation analysis rather than the headline treatment effect

Planned policy-text stages:

- `discover` — identify candidate policy documents on approved official sites
- `normalize` — standardize metadata and text capture
- `rules` — extract rule-based indicators such as deadlines or quantitative targets
- `score` — attach validated LLM scoring outputs
- `aggregate` — roll document scores into city-year features
- `full` — run the full staged pipeline once the package implementation is in place

## Current DML status

The repository now includes a first-pass runnable DML main-regression workflow and a synchronized `Table 2` result export.

Current first-pass mainline:

- sample: `294` cities / `1456` city-year observations
- treatment: `digital_inclusive_finance_index`
- outcome: `co2_emission_intensity`
- controls: `gdp_total`, `secondary_industry_share`, `fiscal_expenditure`
- cross-fitting: `GroupKFold(pku_city_code)`
- covariance: `cluster(pku_city_code)`

Current first-pass robustness result uses `co2_emission_total` as the outcome under the same control set.

## Heterogeneity runtime note

The heterogeneity input-preparation path is runnable in the main environment, but full `econml + shap` CATE / SHAP execution currently depends on a compatible Python environment.

The compatible local runtime currently used in-session is a repo-local virtual environment:

```bash
python3 -m venv .omx/venvs/heterogeneity
./.omx/venvs/heterogeneity/bin/python -m pip install --upgrade pip
./.omx/venvs/heterogeneity/bin/python -m pip install econml==0.15.1 shap==0.43.0 doubleml==0.8.1
PYTHONPATH=src ./.omx/venvs/heterogeneity/bin/python src/05_heterogeneity.py --check-deps
```

Note:

- `econml==0.15.1` is compatible with `shap<0.44`
- therefore `shap==0.43.0` is pinned in `environment.yml`


  项目主题                                                   
                                                             
  "双碳战略与数字经济的碳减排效应：基于双机器学习的因果推断与
  异质性分析"                                                
                                                             
  项目结构        

  - src/ 下的编号脚本对应研究步骤                            
  - src/stat_modeling/ 存放可复用逻辑
  - 政策文本功能作为辅助机制/调节变量分析                    
                  
  运行顺序

  1. 01_data_clean.py - 数据清洗
  2. 02_dea_efficiency.py - DEA效率分析
  3. 03_eda.py - 探索性数据分析                              
  4. 04_dml_main.py - 双机器学习主回归
  5. 05_heterogeneity.py - 异质性分析                        
  6. 06_robustness.py - 稳健性检验                           
  7. 07_spatial.py - 空间分析（可选）                        
  8. 08_policy_text.py - 政策文本模块                        
                                                             
  当前DML状态                                                
                                                             
  - 样本：294个城市 / 1456个城-年观测值                      
  - 处理变量：数字普惠金融指数
  - 结果变量：CO₂排放强度                                    
  - 已有首轮主回归和稳健性结果                               
                                                             
  环境配置                                                   
                                                             
  - 使用conda环境，配置文件为 environment.yml                
  - 全局随机种子：42
  - 异质性分析需要单独的虚拟环境（econml + shap）  