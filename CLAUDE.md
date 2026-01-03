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
