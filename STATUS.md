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

## 📋 進度紀錄（2026-11-24）— AI 對話句抽樣

### ✅ 已完成

1. **新增 `samples/ai-prompts/sampled-2026-11.json`（25 句）**
   - 來源：`allenai/WildChat-1M`（ODC-BY-1.0，版本 `7d6490e4`），使用者寫的中文短句
   - 挑選 zhtw 4.5.0 轉換後仍含常見大陸 IT／對話用語的句子
   - 已排除個人資料、商業往來內容、攻擊類文字，以及原文是繁體的句子
   - Codex 先提出 expected，Gemini（經 `agy`）只看 input 與規則獨立審查；兩者原始建議在
     `samples/ai-prompts/sampled-2026-11.ai-review.json`

2. **AI 審查結果（advisory，尚未經人工確認）**
   - 11 句兩者一致認為 zhtw 需改：程序→程式（寫程式）、默認→預設、質量→品質（速度和品質）、
     支持→支援（軟體功能）、刷新→重新整理（網頁）、保存→儲存（存檔）、项目式学习→專題式學習、
     抠图→去背、实体类→實體類別、cad文件→cad檔案
   - 3 句兩者一致認為 zhtw 正確（寧可少轉）：實現（達成目標）、程序（流程）、保存（文物）
   - 8 句兩者都接受 zhtw 輸出，只是首選不同（大模型、智慧體、實現／實作等）
   - 3 句意見不同，需要維護者決定：安卓app、本项目、支持向量机
   - 其他觀察：「安卓app」被轉成「Androidapp」（中間沒有空格）；「借书记录」的名詞用法可寫「紀錄」

### 🔄 待處理

1. **人工確認** `samples/ai-prompts/sampled-2026-11.json` 的 25 句（tags 有 `unverified`）
2. 確認後移到 `tech/` 或 `regressions/`，再另案評估 zhtw 字典修改
