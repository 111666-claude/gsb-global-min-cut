# global-min-cut

无向图的全局最小割（Stoer-Wagner 风格），只用 Python 标准库。

```
python3 -m mincut.cli --edges 'a-z:1,z-e:1,a-e:100'
python3 -m mincut.cli --edges 'a-b:1,a-b:1,b-c:5'
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **要求的是全局最小割**：`--edges 'a-z:1,z-e:1,a-e:100'` 里把 `z` 单独割出去只要 2，
  所以按口径是 `cut=2`、`side=z`；现在只求「第一个顶点到最后一个顶点」的 s-t 割，给 `cut=101`。
- **平行边要累加**：`--edges 'a-b:1,a-b:1,b-c:5'` 里 `a` 那一侧有两条容量 1 的平行边，
  按口径 `cut=2`；现在平行边被覆盖成一条，给 `cut=1`。
- 自环忽略；空图或只有一个顶点时给 `cut=0`、`side=`（空）。
- 输出：`cut=` 是割容量，`side=` 是某一侧顶点（按字典序，逗号分隔）；两侧之间的边容量之和必须等于 `cut`。
- 不变量：割容量等于两侧之间所有边的容量之和；`side` 既不是空集也不是全集；同一输入重复求解结果相同。
- 规模：1000 个顶点、50 万条边的稠密图要在 5 秒内跑完，内存 O(V²)；不许对每个源点都跑一遍最大流。

## 现在的行为

- `global_min_cut` 把 `nodes[0]` 当源、`nodes[-1]` 当汇，只做一次 s-t 最小割。
- `weights[(left, right)] = (left, right, value)` 让平行边互相覆盖，容量被吃掉。
- 没有实现 Stoer-Wagner 的收缩过程，也没有把割容量与两侧之间的边核对一遍。

## 计划新增的能力

```
--edges 边表    逗号分隔的 u-v:容量
```

## 输出

```
cut=2
side=z
```

## 目录

```
mincut/cut.py   解析与全局最小割
mincut/cli.py   命令行入口
tests/          unittest 用例
```
