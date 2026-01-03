#!/usr/bin/env python3
"""
下載中文語料庫

資料來源：https://github.com/brightmart/nlp_chinese_corpus

使用方式：
    pip install gdown
    python scripts/download_corpus.py [--dataset DATASET] [--all]

範例：
    python scripts/download_corpus.py --dataset wiki      # 只下載維基百科
    python scripts/download_corpus.py --dataset news      # 只下載新聞語料
    python scripts/download_corpus.py --all               # 下載全部（需大量空間）
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Google Drive 檔案 ID
DATASETS = {
    "wiki": {
        "name": "維基百科 (wiki2019zh)",
        "gdrive_id": "1EdHUZIDpgcBoSqbjlfNKJ3b1t0XIUjbt",
        "filename": "wiki2019zh.zip",
        "size": "519MB",
        "description": "104萬條維基詞條",
    },
    "news": {
        "name": "新聞語料 (news2016zh)",
        "gdrive_id": "1TMKu1FpTr6kcjWXWlQHX7YJsMfhhcVKp",
        "filename": "news2016zh.zip",
        "size": "3.6GB",
        "description": "250萬篇新聞文章",
    },
    "baike": {
        "name": "百科問答 (baike2018qa)",
        "gdrive_id": "1_vgGQZpfSxN_Ng9iTAvE7hM3Z7NVwXP2",
        "filename": "baike2018qa.zip",
        "size": "663MB",
        "description": "150萬問答對",
    },
    "webtext": {
        "name": "社區問答 (webtext2019zh)",
        "gdrive_id": "1u2yW_XohbYL2YAK6Bzc5XrngHstQTf0v",
        "filename": "webtext2019zh.zip",
        "size": "1.7GB",
        "description": "410萬社區問答",
    },
    "translation": {
        "name": "翻譯語料 (translation2019zh)",
        "gdrive_id": "1EX8eE5YWBxCaohBO8Fh4e2j3b9C2bTVQ",
        "filename": "translation2019zh.zip",
        "size": "596MB",
        "description": "520萬中英翻譯對",
    },
}

# 推薦的最小測試集
RECOMMENDED = ["wiki", "news"]


def check_gdown():
    """檢查 gdown 是否已安裝"""
    try:
        import gdown  # noqa: F401
        return True
    except ImportError:
        return False


def install_gdown():
    """安裝 gdown"""
    print("正在安裝 gdown...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])


def download_dataset(dataset_key: str, output_dir: Path, force: bool = False):
    """下載單一資料集"""
    import gdown

    if dataset_key not in DATASETS:
        print(f"❌ 未知的資料集: {dataset_key}")
        print(f"   可用選項: {', '.join(DATASETS.keys())}")
        return False

    dataset = DATASETS[dataset_key]
    output_path = output_dir / dataset["filename"]
    extracted_dir = output_dir / dataset_key

    # 檢查是否已下載
    if extracted_dir.exists() and not force:
        print(f"✅ {dataset['name']} 已存在，跳過下載")
        return True

    print(f"\n📥 下載 {dataset['name']}")
    print(f"   大小: {dataset['size']}")
    print(f"   說明: {dataset['description']}")

    # 下載
    url = f"https://drive.google.com/uc?id={dataset['gdrive_id']}"
    try:
        gdown.download(url, str(output_path), quiet=False)
    except Exception as e:
        print(f"❌ 下載失敗: {e}")
        print(f"   請手動下載: https://drive.google.com/file/d/{dataset['gdrive_id']}/view")
        return False

    # 解壓縮
    if output_path.exists():
        print(f"📦 解壓縮 {output_path.name}...")
        import zipfile
        try:
            with zipfile.ZipFile(output_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            # 刪除 zip 檔
            output_path.unlink()
            print(f"✅ {dataset['name']} 下載完成")
            return True
        except zipfile.BadZipFile:
            print(f"❌ 解壓縮失敗，檔案可能損壞")
            return False

    return False


def list_datasets():
    """列出所有可用的資料集"""
    print("\n可用的資料集：\n")
    print(f"{'名稱':<12} {'大小':<8} {'說明'}")
    print("-" * 60)
    for key, ds in DATASETS.items():
        rec = " ⭐" if key in RECOMMENDED else ""
        print(f"{key:<12} {ds['size']:<8} {ds['description']}{rec}")
    print("\n⭐ = 建議下載（涵蓋最常見場景）")
    print(f"\n總計: {len(DATASETS)} 個資料集")


def main():
    parser = argparse.ArgumentParser(
        description="下載中文 NLP 語料庫",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
    %(prog)s --list                    # 列出所有資料集
    %(prog)s --dataset wiki            # 下載維基百科
    %(prog)s --dataset wiki news       # 下載維基和新聞
    %(prog)s --recommended             # 下載建議資料集
    %(prog)s --all                     # 下載全部（約 7GB）
        """,
    )
    parser.add_argument("--list", action="store_true", help="列出所有可用的資料集")
    parser.add_argument("--dataset", nargs="+", help="指定要下載的資料集")
    parser.add_argument("--recommended", action="store_true", help="下載建議的資料集")
    parser.add_argument("--all", action="store_true", help="下載所有資料集")
    parser.add_argument("--force", action="store_true", help="強制重新下載")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "large",
        help="輸出目錄（預設: large/）",
    )

    args = parser.parse_args()

    if args.list:
        list_datasets()
        return

    # 確保 gdown 已安裝
    if not check_gdown():
        install_gdown()

    # 決定要下載的資料集
    datasets_to_download = []
    if args.all:
        datasets_to_download = list(DATASETS.keys())
    elif args.recommended:
        datasets_to_download = RECOMMENDED
    elif args.dataset:
        datasets_to_download = args.dataset
    else:
        parser.print_help()
        print("\n請指定要下載的資料集，或使用 --list 查看可用選項")
        return

    # 建立輸出目錄
    args.output.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 輸出目錄: {args.output}")
    print(f"📊 將下載 {len(datasets_to_download)} 個資料集: {', '.join(datasets_to_download)}")

    # 下載
    success = 0
    for ds in datasets_to_download:
        if download_dataset(ds, args.output, args.force):
            success += 1

    print(f"\n✅ 完成: {success}/{len(datasets_to_download)} 個資料集下載成功")

    if success > 0:
        print(f"\n下一步：執行抽樣腳本生成測試資料")
        print(f"    python scripts/sample_corpus.py --source {args.output}")


if __name__ == "__main__":
    main()
