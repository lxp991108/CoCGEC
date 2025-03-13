# CoCGEC: A Chain-of-Task Framework for Instruction Tuning of LLMs Based on Chinese Grammatical Error Correction

本仓库公开了用于中文语病纠错（CGEC）的 CoCGEC 数据集以及自动标注语病范围的代码。这些资源基于我们在 COLING 2025 接收的论文  
**“A Chain-of-Task Framework for Instruction Tuning of LLMs Based on Chinese Grammatical Error Correction”**  
中提出的方法。

## 目录结构

```
CoCGEC/
├── data/
│   └── CoCGEC_train.json      # 包含训练数据及语病错误、错误类型和错误范围的标注信息
├── LICENSE                    # 项目许可证（Apache-2.0）
├── README.md                  # 中文自述文件
├── README_EN.md               # 英文自述文件
└── addErrorRange.py           # 自动标注语病范围的代码
```

## 数据集说明

- **CoCGEC_train.json**：该文件包含用于训练的中文语病纠错数据，每个样本均附带语法错误及对应错误类型和错误范围的标注信息。
- 数据集采用多粒度自动标注方法构建，旨在降低模型在纠正过程中的过度修改现象，提高纠正精度。

## 代码说明

- **addErrorRange.py**：实现了自动标注语病范围的算法，支持字符级、词级和句子级标注。用户可根据需要调整和扩展代码。

## 使用方法

1. 克隆本仓库：
   ```bash
   git clone https://github.com/lxp991108/CoCGEC.git
   ```
2. 数据集文件位于 `data/CoCGEC_train.json`，可直接用于模型训练与评估。
3. 运行自动标注代码：
   ```bash
   python addErrorRange.py
   ```

## 论文引用

如果您在研究中使用了该数据集或代码，请引用我们的论文：
```
@inproceedings{liu-etal-2025-chain,
    title = "A Chain-of-Task Framework for Instruction Tuning of {LLM}s Based on {C}hinese Grammatical Error Correction",
    author = "Liu, Xinpeng  and
      Xu, Bing  and
      Yang, Muyun  and
      Cao, Hailong  and
      Zhu, Conghui  and
      Zhao, Tiejun  and
      Lu, Wenpeng",
    booktitle = "Proceedings of the 31st International Conference on Computational Linguistics",
    month = jan,
    year = "2025",
    address = "Abu Dhabi, UAE",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.coling-main.577/",
    pages = "8623--8639"
}
```

## 许可证

本项目采用 [Apache-2.0 License](LICENSE) 开源许可证。

## 联系方式

如有任何疑问或建议，请联系：[dtldlcy@gmail.com](mailto:dtldlcy@gmail.com)
```
