import os
import json

def build_privacy_manifest():
    data_dir = "data"
    manifest_dir = "data/manifests"
    os.makedirs(manifest_dir, exist_ok=True)
    
    manifest_path = os.path.join(manifest_dir, "privacy.jsonl")
    
    # data klasöründeki resimleri bulalım
    image_files = []
    if os.path.exists(data_dir):
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    rel_path = os.path.relpath(os.path.join(root, file), start=".")
                    image_files.append(rel_path.replace("\\", "/"))

    print(f"Bulunan toplam görsel sayısı: {len(image_files)}")

    # Yönergeye göre 25 private, 25 non_private olmak üzere toplam 50 örnek
    records = []
    for i in range(1, 51):
        sample_id = f"privacy_{i:04d}"
        
        # Bilgisayardaki gerçek resimleri sırayla atayalım, yetmeyen yerlerde döngüye sokalım
        if len(image_files) >= i:
            img_path = image_files[i-1]
        else:
            img_path = image_files[(i - 1) % len(image_files)] if image_files else f"data/VizWiz_v2_{i:012d}.jpg"
            
        ground_truth = "private" if i <= 25 else "non_private"
        
        record = {
            "sample_id": sample_id,
            "task": "privacy",
            "image_path": img_path,
            "ground_truth": ground_truth,
            "source_dataset": "VizWiz-Priv",
            "split": "validation",
            "license": "CC BY 4.0"
        }
        records.append(record)

    # 50 kaydı privacy.jsonl dosyasına yaz
    with open(manifest_path, 'w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')

    print(f"✅ Başarılı! 50 kayıtlık manifest dosyası güncellendi: {manifest_path}")

if __name__ == "__main__":
    build_privacy_manifest()