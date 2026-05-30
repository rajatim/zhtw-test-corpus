# zhtw-test-corpus - AI 開發指南

## 重要警告

**此 repo 存放簡體中文測試資料，請勿執行任何轉換！**

```
❌ 不要執行 zhtw fix
❌ 不要設定 pre-commit hooks
❌ 不要自動轉換任何內容
```

## 關聯專案

此 repo 是 [zhtw](https://github.com/rajatim/zhtw) 的配套測試語料庫。

## 編輯規則

1. **保持簡體** - `input` 欄位必須是簡體中文
2. **人工校驗** - `expected` 欄位需人工確認正確的台灣繁體
3. **格式一致** - 遵循 README.md 定義的 JSON 格式

## 常見任務

### 新增語料

```bash
# 在對應目錄新增或編輯 JSON
vim tech/new_samples.json
```

### 驗證格式

```bash
# 確認 JSON 格式正確
python3 -m json.tool news/samples.json > /dev/null && echo "Valid JSON"
```

## 目錄結構

| 目錄 | 用途 |
|------|------|
| `news/` | 新聞正式用語 |
| `tech/` | IT 技術術語 |
| `social/` | 社群口語 |
| `wiki/` | 百科知識 |
| `regressions/` | Bug 迴歸案例 |
| `large/` | 大型語料（本地，不入 git） |
| `samples/` | 自動抽樣結果（需校驗） |
| `scripts/` | 下載與抽樣腳本 |

---

## 📋 進度紀錄（2026-01-03）

### ✅ 已完成

1. **Repo 建立**
   - 建立 zhtw-test-corpus 獨立 repo
   - 精選樣本：news/, tech/, social/, wiki/, regressions/
   - README.md, CLAUDE.md, LICENSE, .gitignore

2. **下載腳本** (`scripts/download_corpus.py`)
   - 支援 5 種語料：wiki, news, webtext, baike, translation
   - 從 Google Drive 下載並解壓
   - 已測試 wiki (519MB) 下載成功

3. **抽樣腳本** (`scripts/sample_corpus.py`)
   - 從大型語料庫隨機抽樣
   - 支援 `--use-zhtw` 自動生成預期輸出
   - 已修正 wiki 檔案格式偵測（wiki_00 格式）

### 🔄 待處理

1. **人工校驗**
   - `samples/wiki/sampled.json` 已產生 20 條
   - 需人工確認 expected 欄位是否正確
   - 校驗後移至 `wiki/verified.json`

2. **其他語料**
   - 可選下載：news (3.6GB), webtext (1.7GB), baike (663MB)
   - 執行：`python scripts/download_corpus.py --dataset news`

3. **整合到 zhtw 測試**
   - 在 zhtw 專案建立 `tests/test_corpus.py`
   - 讀取此 repo 的語料執行批次驗證

### 📝 下次可以做

```bash
# 下載更多語料
python scripts/download_corpus.py --dataset news

# 抽樣並用 zhtw 生成預期
python scripts/sample_corpus.py --count 50 --use-zhtw

# 人工校驗 samples/ 目錄下的檔案
```
