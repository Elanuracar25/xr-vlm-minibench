import json
import random
import os
import shutil

json_path = "../data/val.json"
manifest_path = "../manifests/privacy.jsonl"
target_img_dir = "../data/"

print("\n--- GÖRSEL CIMBIZLAMA ARACI (UZANTI ESNEK VERSİYON) ---")
source_dir = input("Klasör Yolu: ").strip().strip('"').strip("'")

# 1. Bilgisayardaki mevcut fotoğrafları uzantıdan bağımsız olarak (isimleriyle) haritalandır
print("Mevcut fotoğraflar taranıyor, lütfen bekle...")
available_files = {}
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # Uzantıyı yok sayarak sadece dosya adını anahtar yapıyoruz (örn: VizWiz_v2_000000044179)
        base_name, _ = os.path.splitext(file)
        available_files[base_name] = os.path.join(root, file)

# 2. JSON dosyasını oku
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Var olan fotoğrafları eşleştir
for item in data:
    base_name, _ = os.path.splitext(item['image'])
    if base_name in available_files:
        item['real_path'] = available_files[base_name]

# Filtreleme
valid_data = [item for item in data if 'real_path' in item]
private_list = [item for item in valid_data if item.get('private') == 1]
non_private_list = [item for item in valid_data if item.get('private') == 0]

print(f"Bulunan uygun Private: {len(private_list)}, Non-Private: {len(non_private_list)}")

if len(private_list) < 25 or len(non_private_list) < 25:
    print("HATA: Hâlâ 25'er adet bulunamadı!")
    exit()

# 4. 25'er adet (toplam 50) örnek seç
random.seed(42) 
selected_private = random.sample(private_list, 25)
selected_non_private = random.sample(non_private_list, 25)
all_selected = selected_private + selected_non_private

# 5. Manifest oluştur ve fotoğrafları kopyala
with open(manifest_path, 'w', encoding='utf-8') as outfile:
    for i, item in enumerate(all_selected):
        img_name = item['image'] # Manifestte orijinal adı kalıyor
        label = "private" if item['private'] == 1 else "non_private"
        
        manifest_record = {
            "sample_id": f"privacy_{i+1:04d}",
            "task": "privacy",
            "image_path": f"data/{img_name}",
            "ground_truth": label,
            "source_dataset": "VizWiz-Priv",
            "split": "validation",
            "license": "CC BY 4.0"
        }
        json.dump(manifest_record, outfile)
        outfile.write('\n')
        
        # Gerçek dosyayı bulup data klasörüne kopyala
        src_file = item['real_path']
        dst_file = os.path.join(target_img_dir, img_name)
        shutil.copy2(src_file, dst_file)

print("\n✅ İŞLEM TAMAM! 50 örnek başarıyla seçildi ve kopyalandı.")