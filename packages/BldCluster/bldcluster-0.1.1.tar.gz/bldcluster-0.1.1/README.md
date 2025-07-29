# BldCluster

建筑分类工具，根据建筑参数对建筑进行聚类分析。

## 简介

BldCluster 是一个用于建筑分类的工具，它能够根据建筑的各种参数进行聚类。

## 安装

```bash
pip install BldCluster
```

## 依赖项

- Python >= 3.11
- pandas
- numpy
- tqdm

## 使用方法

```python
from BldCluster import BldCluster as bc

BldDirtFile = 'Resources\SanFrancisco_buildings_full.csv'
obj = bc.BldCluster(BldDirtFile)
obj.ClassifyBld(IgnoredLabels=['id','Latitude','Longitude','YearBuilt','ReplacementCost'], 
    **{'PlanArea': 100})
```

## 联系方式

- 维护者：Tian You (youtian@njtech.edu.cn)
- 项目主页：https://github.com/youtian95/BldCluster
- 问题追踪：https://github.com/youtian95/BldCluster/issues