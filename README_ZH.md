# CoCGEC

[**English**](README.md) | [**中文**](README_ZH.md)

本仓库是论文 **A Chain-of-Task Framework for Instruction Tuning of LLMs Based
on Chinese Grammatical Error Correction**（COLING 2025）的官方代码与数据发布。

- 论文：[ACL Anthology](https://aclanthology.org/2025.coling-main.577/)
- 页码：8623–8639
- 任务：中文语病纠错（Chinese Grammatical Error Correction, CGEC）

CoCGEC 通过三个依次关联的指令任务减少大语言模型的过度纠错：

1. 语病范围识别；
2. 语病类型判断；
3. 语病纠正。

仓库包含已经发布的 `data/CoCGEC_train.json`、与论文标注结果严格兼容的多粒度
自动标注实现、确定性的两阶段 CoTask 指令构造、预测结果解析以及评测格式导出。
FCGEC 和 NaCGEC 的原始发布文件不在本仓库重复上传，请从原作者仓库获取并遵守
相应许可证。

## 安装

需要 Python 3.10 或更高版本。

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
```

开发环境：

```bash
python -m pip install -e ".[dev]"
pytest
```

## 快速开始

仓库内的 `examples/` 是可公开分发的合成样例。

```bash
# 1. 按论文的多粒度集成策略生成语病范围
cocgec annotate \
  --input examples/sample_fcgec.json \
  --output data/processed/sample_cocgec.json

# 2. 构造 90% 纠错任务 + 10% 范围/类型/纠错任务的两阶段数据
cocgec build-instructions \
  --input data/processed/sample_cocgec.json \
  --output data/processed/sample_instructions.json \
  --stage-two-ratio 0.1 \
  --seed 42

# 3. 计算多参考答案 Exact Match
cocgec evaluate \
  --gold examples/sample_fcgec.json \
  --predictions examples/sample_predictions.jsonl

# 4. 导出 ChERRANT 输入格式
cocgec export \
  --gold examples/sample_fcgec.json \
  --predictions examples/sample_predictions.jsonl \
  --format cherrant \
  --output outputs/sample_cherrant.txt
```

Windows PowerShell 中可以将命令写在同一行，或将行末的 `\` 替换为反引号。

FCGEC 提交 JSON 还需要模型预测的语病类型，默认读取 `error_type` 字段：

```bash
cocgec export \
  --gold examples/sample_fcgec.json \
  --predictions examples/sample_predictions.jsonl \
  --format fcgec \
  --type-key error_type \
  --output outputs/sample_fcgec.json
```

工具不会像早期实验脚本一样随机填写语病类型。如果改写了句子但没有提供 IWO、IWC、
CM、CR、SC、ILL 或 AM 类型预测，程序会直接报错，以避免产生不可复现或不合法的提交。

## 数据格式

推荐输入为 JSON 对象数组：

```json
{
  "id": "demo-1",
  "sentence": "在学习中，我们要及时解决和发现存在的问题。",
  "corrected_sentence": ["在学习中，我们要及时发现和解决存在的问题。"],
  "error_flag": 1,
  "error_type": "语序不当"
}
```

为了兼容论文时期的代码，也支持 `input`、`output`、`flag` 和 `type` 字段别名。
完整字段与标签说明见 [docs/data.md](docs/data.md)。

## 多粒度标注方法

算法从前向和后向比较原句与全部参考答案，支持字符级、Jieba 词级和以中文标点切分的
子句级标注。论文中的集成策略为：

- 成分赘余（CR）和表意不明（AM）使用词级结果；
- 语序不当（IWO）、搭配不当（IWC）、成分残缺（CM）、结构混乱（SC）和
  不合逻辑（ILL）使用子句级结果；
- 未知类型默认使用字符级结果。

可通过 `--granularity char|word|clause` 单独运行某一粒度，用于消融实验。

维护版实现已经在发布的 CoCGEC 训练集上进行了全量回归：19,710 条有错样本的
`error_range` 实现了 19,710/19,710 完全一致。自动范围仍属于启发式标注，将算法迁移
到其他数据集或领域时建议抽样检查。

## 论文训练设置

- 基座模型：Qwen1.5-14B-Chat
- 训练框架：LLaMA-Factory
- 第一阶段：90% 样本，仅使用语病纠正指令
- 第二阶段：剩余 10% 样本，按 Range → Type → Correction 排列
- 初始学习率：`5e-5`
- 学习率调度：cosine
- warmup ratio：`0.003`
- 全局 batch size：`256`
- epoch：`1`
- 推理 temperature：`0.1`

`build-instructions` 输出 LLaMA-Factory 可读取的 `instruction`、`input`、`output`
格式。给定同一个 `--seed`，样本划分、顺序和多参考答案采样均可复现。论文时期没有
记录随机种子，因此无法声称重新生成的 shuffle 与历史训练文件逐样本相同；本项目默认
使用 seed 42，并明确记录在命令行参数中。

## 目录结构

```text
cocgec/       维护中的 Python 包和 CLI
data/         已发布的 CoCGEC 训练标注
tests/        单元测试
examples/     合成输入与预测示例
docs/         数据和复现说明
```

带有硬编码路径、导入即执行或原地覆盖输出行为的论文时期临时脚本不放入公开仓库。
其中与复现有关的粒度、任务顺序、比例、EM 和格式转换能力均已由维护版 CLI 与测试覆盖。

## 本次重构优化

- 整理为可安装的 Python 包和统一 `cocgec` 命令行；
- 保持论文字符级、词级、子句级算法及类型映射不变，并加入全量数据回归测试；
- 为两阶段划分、数据打乱和多参考答案采样增加显式随机种子；
- 移除硬编码路径、导入模块时自动读写文件和覆盖原预测文件等副作用；
- 不再随机伪造 FCGEC 错误类型，改为校验模型的真实类型预测；
- 增加字段与长度校验、合成示例、单元测试、CI、引用元数据和中英文文档；
- 将临时性能探针和重复旧脚本排除在公开仓库之外，其论文相关行为由回归测试固化。

完整列表见 [CHANGELOG.md](CHANGELOG.md)，论文兼容性说明见
[docs/reproduction.md](docs/reproduction.md)。

## 数据获取

- FCGEC：<https://github.com/xlxwalex/FCGEC>
- NaCGEC：<https://github.com/masr2000/NaCGEC>

代码许可证与数据许可证相互独立。下载、使用或再次发布数据和模型前，请检查对应的
上游许可证。

## 测试

```bash
python -m unittest discover -s tests -v
```

GitHub Actions 会在 Python 3.10 和 3.12 上运行测试与静态检查。

## 论文引用

```bibtex
@inproceedings{liu-etal-2025-chain,
    title = "A Chain-of-Task Framework for Instruction Tuning of {LLM}s Based on {C}hinese Grammatical Error Correction",
    author = "Liu, Xinpeng and Xu, Bing and Yang, Muyun and Cao, Hailong and Zhu, Conghui and Zhao, Tiejun and Lu, Wenpeng",
    booktitle = "Proceedings of the 31st International Conference on Computational Linguistics",
    month = jan,
    year = "2025",
    address = "Abu Dhabi, UAE",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.coling-main.577/",
    pages = "8623--8639"
}
```

## 许可证与联系方式

代码采用 [Apache-2.0](LICENSE) 许可证，该许可证已获得所有合作者及所属机构认可。

如有问题或建议，请联系：[dtldlcy@gmail.com](mailto:dtldlcy@gmail.com)。
