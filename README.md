# CoCGEC: A Chain-of-Task Framework for Instruction Tuning of LLMs Based on Chinese Grammatical Error Correction

This repository contains the CoCGEC dataset for Chinese Grammatical Error Correction (CGEC) and the associated code for automatic error range annotation. These resources are based on the methods proposed in our paper  
**“A Chain-of-Task Framework for Instruction Tuning of LLMs Based on Chinese Grammatical Error Correction”**  
accepted at COLING 2025.

## Repository Structure

```
CoCGEC/
├── data/
│   └── CoCGEC_train.json      # Training dataset with annotated grammatical errors, error types, and error ranges
├── LICENSE                    # Project license (Apache-2.0)
├── README.md                  # English version of this README
├── README_ZH.md               # Chinese version of this README
└── addErrorRange.py           # Code for automatic error range annotation
```

## Dataset Description

- **CoCGEC_train.json**: This file contains the training data for Chinese Grammatical Error Correction, with each sample annotated with grammatical errors and corresponding error types and ranges.
- The dataset is built using a multi-granularity automatic annotation approach to reduce over-correction and improve correction accuracy.

## Code Description

- **addErrorRange.py**: Implements the automatic error range annotation algorithm, supporting character-level, word-level, and sentence-level annotations. The code can be adapted or extended as needed.

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/lxp991108/CoCGEC.git
   ```
2. The dataset file is located in `data/CoCGEC_train.json` and can be used directly for training and evaluation.
3. Run the annotation script:
   ```bash
   python addErrorRange.py
   ```

## Citation

If you use this dataset or code in your research, please cite our paper:
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

## License

This project is licensed under the [Apache-2.0 License](LICENSE).

## Contact

If you have any questions or suggestions, please contact: [dtldlcy@gmail.com](mailto:dtldlcy@gmail.com)
```
