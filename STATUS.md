# zhtw-test-corpus Status

> 此檔保留從 AGENTS.md 移出的歷史進度，內容未改寫。

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
