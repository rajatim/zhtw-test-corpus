# zhtw-test-corpus

> zhtw 簡繁轉換測試語料庫

此 repo 存放**簡體中文**測試語料，用於驗證 [zhtw](https://github.com/rajatim/zhtw) 轉換準確度。

## 為什麼需要獨立 repo？

zhtw 工具會自動轉換簡體字，如果測試語料放在主 repo：
- Git hooks 可能意外轉換測試資料
- CI/CD 流程可能觸發轉換
- 測試資料失去原本意義

獨立 repo 確保測試語料保持**原始簡體狀態**。

## 結構

```
zhtw-test-corpus/
├── news/              # 新聞語料（正式用語）
├── tech/              # 技術文檔（IT 術語）
├── social/            # 社群媒體（口語化）
├── wiki/              # 維基百科（百科知識）
├── regressions/       # 用戶回報的轉換問題
├── samples/           # 自動抽樣結果（需人工校驗）
├── large/             # 大型語料庫（本地下載，不入 git）
└── scripts/           # 下載與抽樣腳本
    ├── download_corpus.py
    └── sample_corpus.py
```

## 快速開始

### 方式一：使用精選樣本（推薦）

```bash
# Clone repo
git clone https://github.com/rajatim/zhtw-test-corpus

# 精選樣本已包含在 news/, tech/, social/ 等目錄
```

### 方式二：下載大型語料庫

```bash
# 安裝依賴
pip install gdown

# 列出可用的語料庫
python scripts/download_corpus.py --list

# 下載建議的語料庫（約 4GB）
python scripts/download_corpus.py --recommended

# 或下載特定語料庫
python scripts/download_corpus.py --dataset wiki news
```

### 方式三：從大型語料庫抽樣

```bash
# 下載語料後，執行抽樣
python scripts/sample_corpus.py --count 100

# 使用 zhtw 自動生成預期輸出（仍需人工校驗）
python scripts/sample_corpus.py --count 100 --use-zhtw
```

## 可用的大型語料庫

| 資料集 | 大小 | 內容 | 下載指令 |
|--------|------|------|----------|
| **wiki** | 519MB | 104萬維基詞條 | `--dataset wiki` |
| **news** | 3.6GB | 250萬篇新聞 | `--dataset news` |
| **webtext** | 1.7GB | 410萬社區問答 | `--dataset webtext` |
| **baike** | 663MB | 150萬百科問答 | `--dataset baike` |
| **translation** | 596MB | 520萬翻譯對 | `--dataset translation` |

資料來源：[brightmart/nlp_chinese_corpus](https://github.com/brightmart/nlp_chinese_corpus)

## 語料格式

每個 JSON 檔案格式如下：

```json
{
  "metadata": {
    "source": "來源名稱",
    "source_url": "https://...",
    "license": "CC-BY-4.0",
    "collected_date": "2026-01-03",
    "description": "語料描述"
  },
  "corpus": [
    {
      "id": "news_001",
      "input": "简体中文原文",
      "expected": "繁體中文預期結果",
      "tags": ["news", "politics"],
      "notes": "備註（可選）"
    }
  ]
}
```

### 欄位說明

| 欄位 | 必填 | 說明 |
|------|------|------|
| `id` | 是 | 唯一識別碼 |
| `input` | 是 | 簡體中文輸入 |
| `expected` | 是 | 台灣繁體預期輸出 |
| `tags` | 否 | 分類標籤 |
| `notes` | 否 | 特殊備註（如：測試一字多義） |

## 在 zhtw 中使用

### 下載語料

```bash
# 在 zhtw 專案目錄
git clone https://github.com/rajatim/zhtw-test-corpus tests/data/corpus
```

### 執行測試

```bash
# 執行語料測試
pytest tests/test_corpus.py

# 或使用 zhtw 內建測試
zhtw test --corpus tests/data/corpus
```

## 語料來源與授權

### 精選樣本

| 目錄 | 來源 | 授權 |
|------|------|------|
| `news/` | 原創模擬 | CC-BY-4.0 |
| `tech/` | 原創模擬 | CC-BY-4.0 |
| `social/` | 原創模擬 | CC-BY-4.0 |
| `wiki/` | 原創模擬 | CC-BY-4.0 |
| `regressions/` | 用戶回報 | CC-BY-4.0 |

### 大型語料庫

| 資料集 | 來源 | 授權 |
|--------|------|------|
| wiki2019zh | brightmart/nlp_chinese_corpus | 待確認 |
| news2016zh | brightmart/nlp_chinese_corpus | 待確認 |
| webtext2019zh | brightmart/nlp_chinese_corpus | 待確認 |

### 參考語料庫

- [brightmart/nlp_chinese_corpus](https://github.com/brightmart/nlp_chinese_corpus) - 大規模中文語料
- [liuhuanyong/ChineseNLPCorpus](https://github.com/liuhuanyong/ChineseNLPCorpus) - 中文 NLP 語料集
- [didi/ChineseNLP](https://github.com/didi/ChineseNLP) - 滴滴 NLP 資料集

## 貢獻

歡迎貢獻語料！請確保：

1. **來源合法** - 確認語料授權允許使用
2. **格式正確** - 遵循上述 JSON 格式
3. **人工校驗** - `expected` 欄位需人工確認
4. **避免敏感內容** - 不含個人資訊或不當內容

### 新增語料流程

1. Fork 此 repo
2. 在對應目錄新增 JSON 檔案
3. 確保 `expected` 欄位正確
4. 提交 PR

### 校驗自動抽樣

如果您想幫忙校驗自動抽樣的語料：

1. 執行 `python scripts/sample_corpus.py --use-zhtw`
2. 檢查 `samples/` 目錄下的 `sampled.json`
3. 人工校驗 `expected` 欄位
4. 將校驗後的內容移至對應目錄（如 `wiki/verified.json`）
5. 提交 PR

## 授權

此 repo 的原創內容採用 [CC-BY-4.0](LICENSE) 授權。

各語料來源的授權請參考上方表格。

---

*此 repo 為 [zhtw](https://github.com/rajatim/zhtw) 專案的配套測試資源*
