import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def evaluate_results():
    manifest_file = "data/manifests/anomaly.txt"
    results_file = "results/anomaly_results.jsonl"
    
    # Gerçek etiketleri yükle
    ground_truths = {}
    with open(manifest_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                ground_truths[item["sample_id"]] = item["ground_truth"]
                
    predictions = []
    actuals = []
    errors = []
    
    with open(results_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                s_id = item["sample_id"]
                
                # API'den gelen cevabı küçük harfe çevir ve boşlukları temizle
                raw_pred = str(item.get("prediction", "error")).lower().strip()
                
                # Esnek eşleştirme (Normal/normal, Anomali/anomaly/anomal vb.)
                if "normal" in raw_pred:
                    pred = "normal"
                elif "anomal" in raw_pred:
                    pred = "anomaly"
                else:
                    pred = "normal" if ground_truths.get(s_id) == "anomaly" else "anomaly"
                    
                actual = ground_truths.get(s_id)
                if actual:
                    predictions.append(pred)
                    actuals.append(actual)
                    
                    if pred != actual:
                        errors.append({
                            "sample_id": s_id,
                            "gercek": actual,
                            "tahmin": pred,
                            "neden_tr": item.get("reason_tr", "Belirtilmemiş")
                        })

    # Metrikleri hesapla
    acc = accuracy_score(actuals, predictions)
    prec = precision_score(actuals, predictions, pos_label="anomaly", zero_division=0)
    rec = recall_score(actuals, predictions, pos_label="anomaly", zero_division=0)
    f1 = f1_score(actuals, predictions, pos_label="anomaly", zero_division=0)
    cm = confusion_matrix(actuals, predictions, labels=["normal", "anomaly"])

    print("\n--- DEĞERLENDİRME SONUÇLARI ---")
    print(f"Accuracy (Doğruluk):  {acc:.4f}")
    print(f"Precision (Kesinlik): {prec:.4f}")
    print(f"Recall (Duyarlılık):  {rec:.4f}  <-- Ana Metrik")
    print(f"F1 Score:             {f1:.4f}")
    
    print("\n--- CONFUSION MATRIX ---")
    print(f"                 Tahmin: Normal | Tahmin: Anomaly")
    print(f"Gerçek: Normal   |      {cm[0][0]:<10} |      {cm[0][1]:<10}")
    print(f"Gerçek: Anomaly  |      {cm[1][0]:<10} |      {cm[1][1]:<10}")
    
    print(f"\n--- HATALI TAHMİNLER ({len(errors)} adet) ---")
    for i, err in enumerate(errors[:10]): 
        print(f"{i+1}. Dosya: {err['sample_id']} | Gerçek: {err['gercek']}, Tahmin: {err['tahmin']}")
        print(f"   Model Gerekçesi: {err['neden_tr']}\n")
        
if __name__ == "__main__":
    evaluate_results()