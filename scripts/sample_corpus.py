#!/usr/bin/env python3
"""
從大型語料庫抽樣生成測試資料

使用方式：
    python scripts/sample_corpus.py --source large/ --output samples/
    python scripts/sample_corpus.py --source large/ --count 100

功能：
    1. 從下載的語料庫隨機抽樣
    2. 轉換為 zhtw-test-corpus JSON 格式
    3. 可選擇使用 zhtw 生成預期輸出（需人工校驗）
"""

import argparse
import json
import random
import re
from datetime import datetime
from pathlib import Path


def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""
    # 移除多餘空白
    text = re.sub(r'\s+', ' ', text.strip())
    # 移除 HTML 標籤
    text = re.sub(r'<[^>]+>', '', text)
    # 限制長度
    if len(text) > 500:
        # 找到句號位置截斷
        pos = text.find('。', 100)
        if pos > 0:
            text = text[:pos + 1]
        else:
            text = text[:200] + '...'
    return text


def has_simplified_chinese(text: str) -> bool:
    """檢查是否包含簡體中文（簡單判斷）"""
    # 常見簡體字
    simplified_chars = set('简体国际发这为个着时会种长来东说对动机关进经给学实现点开问题还样')
    return any(c in simplified_chars for c in text)


def sample_wiki(source_dir: Path, count: int) -> list:
    """從維基百科抽樣"""
    samples = []
    # 嘗試不同可能的目錄名稱
    possible_dirs = ["wiki_zh", "wiki2019zh", "wiki"]
    wiki_dir = None
    for name in possible_dirs:
        if (source_dir / name).exists():
            wiki_dir = source_dir / name
            break

    if wiki_dir is None:
        print(f"⚠️ 找不到 wiki 語料，跳過")
        return samples

    # 找所有檔案（可能是 JSON 或 wiki_00 格式）
    json_files = list(wiki_dir.glob("*.json")) + list(wiki_dir.glob("**/*.json"))
    if not json_files:
        # 嘗試找 wiki_xx 格式檔案（每行是 JSON）
        json_files = list(wiki_dir.glob("**/wiki_*"))
    if not json_files:
        # 嘗試找 txt 檔
        json_files = list(wiki_dir.glob("*.txt"))

    print(f"   找到 {len(json_files)} 個檔案")

    all_texts = []
    for f in json_files[:10]:  # 只讀前 10 個檔案
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                for line in fp:
                    try:
                        data = json.loads(line.strip())
                        text = data.get('text', '') or data.get('content', '')
                        if text and len(text) > 50 and has_simplified_chinese(text):
                            all_texts.append(clean_text(text))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"   讀取 {f.name} 失敗: {e}")

    # 隨機抽樣
    if all_texts:
        sampled = random.sample(all_texts, min(count, len(all_texts)))
        for i, text in enumerate(sampled):
            samples.append({
                "id": f"wiki_{i+1:03d}",
                "input": text,
                "expected": "",  # 需人工填寫
                "tags": ["wiki", "encyclopedia"],
                "notes": "自動抽樣，需人工校驗 expected",
            })

    return samples


def sample_news(source_dir: Path, count: int) -> list:
    """從新聞語料抽樣"""
    samples = []
    news_dir = source_dir / "news2016zh"

    if not news_dir.exists():
        print(f"⚠️ 找不到 news2016zh，跳過")
        return samples

    json_files = list(news_dir.glob("*.json")) + list(news_dir.glob("**/*.json"))
    print(f"   找到 {len(json_files)} 個檔案")

    all_texts = []
    for f in json_files[:10]:
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                for line in fp:
                    try:
                        data = json.loads(line.strip())
                        # 新聞格式：title, content, desc
                        title = data.get('title', '')
                        content = data.get('content', '') or data.get('desc', '')
                        text = f"{title}。{content}" if title else content
                        if text and len(text) > 50 and has_simplified_chinese(text):
                            all_texts.append(clean_text(text))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"   讀取 {f.name} 失敗: {e}")

    if all_texts:
        sampled = random.sample(all_texts, min(count, len(all_texts)))
        for i, text in enumerate(sampled):
            samples.append({
                "id": f"news_{i+1:03d}",
                "input": text,
                "expected": "",
                "tags": ["news", "formal"],
                "notes": "自動抽樣，需人工校驗 expected",
            })

    return samples


def sample_webtext(source_dir: Path, count: int) -> list:
    """從社區問答抽樣"""
    samples = []
    webtext_dir = source_dir / "webtext2019zh"

    if not webtext_dir.exists():
        print(f"⚠️ 找不到 webtext2019zh，跳過")
        return samples

    json_files = list(webtext_dir.glob("*.json")) + list(webtext_dir.glob("**/*.json"))
    print(f"   找到 {len(json_files)} 個檔案")

    all_texts = []
    for f in json_files[:10]:
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                for line in fp:
                    try:
                        data = json.loads(line.strip())
                        # 問答格式
                        question = data.get('title', '') or data.get('question', '')
                        answer = data.get('content', '') or data.get('answer', '')
                        if question and has_simplified_chinese(question):
                            all_texts.append(clean_text(question))
                        if answer and has_simplified_chinese(answer):
                            all_texts.append(clean_text(answer))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"   讀取 {f.name} 失敗: {e}")

    if all_texts:
        sampled = random.sample(all_texts, min(count, len(all_texts)))
        for i, text in enumerate(sampled):
            samples.append({
                "id": f"social_{i+1:03d}",
                "input": text,
                "expected": "",
                "tags": ["social", "qa", "informal"],
                "notes": "自動抽樣，需人工校驗 expected",
            })

    return samples


def sample_baike(source_dir: Path, count: int) -> list:
    """從百科問答抽樣"""
    samples = []
    baike_dir = source_dir / "baike2018qa"

    if not baike_dir.exists():
        print(f"⚠️ 找不到 baike2018qa，跳過")
        return samples

    json_files = list(baike_dir.glob("*.json")) + list(baike_dir.glob("**/*.json"))
    print(f"   找到 {len(json_files)} 個檔案")

    all_texts = []
    for f in json_files[:10]:
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                for line in fp:
                    try:
                        data = json.loads(line.strip())
                        question = data.get('title', '') or data.get('question', '')
                        answer = data.get('answer', '') or data.get('content', '')
                        text = f"問：{question} 答：{answer}" if question and answer else (question or answer)
                        if text and len(text) > 30 and has_simplified_chinese(text):
                            all_texts.append(clean_text(text))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"   讀取 {f.name} 失敗: {e}")

    if all_texts:
        sampled = random.sample(all_texts, min(count, len(all_texts)))
        for i, text in enumerate(sampled):
            samples.append({
                "id": f"baike_{i+1:03d}",
                "input": text,
                "expected": "",
                "tags": ["baike", "qa", "encyclopedia"],
                "notes": "自動抽樣，需人工校驗 expected",
            })

    return samples


def generate_expected_with_zhtw(samples: list) -> list:
    """使用 zhtw 生成預期輸出（需已安裝 zhtw）"""
    try:
        from zhtw.dictionary import load_dictionary
        from zhtw.matcher import Matcher

        terms = load_dictionary(sources=["cn", "hk"])
        matcher = Matcher(terms)

        for sample in samples:
            if not sample["expected"]:
                sample["expected"] = matcher.replace_all(sample["input"])
                sample["notes"] = "由 zhtw 自動生成，需人工校驗"

        print("✅ 已使用 zhtw 生成預期輸出")
    except ImportError:
        print("⚠️ 未安裝 zhtw，expected 欄位保持空白")
        print("   安裝方式: pip install zhtw")

    return samples


def save_samples(samples: list, output_path: Path, category: str):
    """儲存樣本為 JSON"""
    output_data = {
        "metadata": {
            "source": "brightmart/nlp_chinese_corpus",
            "source_url": "https://github.com/brightmart/nlp_chinese_corpus",
            "license": "待確認",
            "collected_date": datetime.now().strftime("%Y-%m-%d"),
            "description": f"{category} 語料自動抽樣",
            "auto_generated": True,
        },
        "corpus": samples,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"   💾 儲存 {len(samples)} 條到 {output_path}")


def main():
    parser = argparse.ArgumentParser(description="從大型語料庫抽樣生成測試資料")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).parent.parent / "large",
        help="語料庫來源目錄（預設: large/）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "samples",
        help="輸出目錄（預設: samples/）",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=50,
        help="每個類別抽樣數量（預設: 50）",
    )
    parser.add_argument(
        "--use-zhtw",
        action="store_true",
        help="使用 zhtw 自動生成 expected（仍需人工校驗）",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="隨機種子（預設: 42）",
    )

    args = parser.parse_args()
    random.seed(args.seed)

    print(f"📁 語料來源: {args.source}")
    print(f"📁 輸出目錄: {args.output}")
    print(f"📊 每類別抽樣: {args.count} 條")
    print()

    if not args.source.exists():
        print(f"❌ 來源目錄不存在: {args.source}")
        print(f"   請先執行: python scripts/download_corpus.py --recommended")
        return

    # 各類別抽樣
    all_samples = {}

    print("📖 抽樣維基百科...")
    all_samples["wiki"] = sample_wiki(args.source, args.count)

    print("📰 抽樣新聞語料...")
    all_samples["news"] = sample_news(args.source, args.count)

    print("💬 抽樣社區問答...")
    all_samples["social"] = sample_webtext(args.source, args.count)

    print("📚 抽樣百科問答...")
    all_samples["baike"] = sample_baike(args.source, args.count)

    # 使用 zhtw 生成 expected
    if args.use_zhtw:
        print("\n🔄 使用 zhtw 生成預期輸出...")
        for category, samples in all_samples.items():
            all_samples[category] = generate_expected_with_zhtw(samples)

    # 儲存
    print("\n💾 儲存樣本...")
    total = 0
    for category, samples in all_samples.items():
        if samples:
            save_samples(samples, args.output / category / "sampled.json", category)
            total += len(samples)

    print(f"\n✅ 完成！共抽樣 {total} 條")
    print(f"\n⚠️ 重要：expected 欄位需要人工校驗！")
    print(f"   即使使用 --use-zhtw，仍可能有誤轉，請人工確認。")


if __name__ == "__main__":
    main()
