import os
import json
import random

# Senin oluşturduğun klasör yapısına tam uygun dosya yolu
DATA_DIR = "data/mvtec/juice_bottle"
OUTPUT_MANIFEST = "data/manifests/anomaly.txt"

def create_manifest():
    samples = []
    
    # 1. Normal görüntüleri topla (25 adet)
    normal_dir = os.path.join(DATA_DIR, "train", "good")
    if not os.path.exists(normal_dir):
        print(f"HATA: {normal_dir} bulunamadı. Lütfen juice_bottle klasörünün içeriğini kontrol et.")
        return

    normal_images = [f for f in os.listdir(normal_dir) if f.endswith(('.png', '.jpg'))]
    selected_normals = random.sample(normal_images, 25)
    
    for i, img in enumerate(selected_normals):
        samples.append({
            "sample_id": f"anomaly_normal_{i:04d}",
            "task": "anomaly",
            "image_path": os.path.join(normal_dir, img).replace("\\", "/"),
            "ground_truth": "normal",
            "source_dataset": "MVTec LOCO AD",
            "split": "validation",
            "license": "CC BY-NC-SA 4.0"
        })

    # 2. Anomali görüntülerini topla (25 adet)
    anomaly_dir = os.path.join(DATA_DIR, "test", "structural_anomalies")
    if not os.path.exists(anomaly_dir):
        print(f"HATA: {anomaly_dir} bulunamadı.")
        return

    anomaly_images = [f for f in os.listdir(anomaly_dir) if f.endswith(('.png', '.jpg'))]
    selected_anomalies = random.sample(anomaly_images, min(25, len(anomaly_images)))
    
    for i, img in enumerate(selected_anomalies):
        samples.append({
            "sample_id": f"anomaly_struct_{i:04d}",
            "task": "anomaly",
            "image_path": os.path.join(anomaly_dir, img).replace("\\", "/"),
            "ground_truth": "anomaly",
            "source_dataset": "MVTec LOCO AD",
            "split": "validation",
            "license": "CC BY-NC-SA 4.0"
        })

    # 3. Listeyi karıştır ve JSONL olarak kaydet
    random.shuffle(samples)
    
    os.makedirs(os.path.dirname(OUTPUT_MANIFEST), exist_ok=True)
    with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            
    print(f"Başarılı! Toplam {len(samples)} kayıt {OUTPUT_MANIFEST} dosyasına yazıldı.")

if __name__ == "__main__":
    create_manifest()