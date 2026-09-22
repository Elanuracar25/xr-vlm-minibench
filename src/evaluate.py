import os
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def evaluate_privacy_results():
    manifest_path = "data/manifests/privacy.jsonl"
    results_path = "results/privacy_results.jsonl"
    
    if not os.path.exists(manifest_path) or not os.path.exists(results_path):
        print("HATA: Manifest veya sonuç dosyası bulunamadı!")
        return

    ground_truths = {}
    with open(manifest_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            item = json.loads(line)
            ground_truths[item['sample_id']] = item['ground_truth'].strip().lower()

    predictions = {}
    raw_preds = set()
    with open(results_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            item = json.loads(line)
            pred = str(item.get('prediction', '')).strip().lower()
            raw_preds.add(pred)
            predictions[item['sample_id']] = pred

    print(f"Modelin ürettiği ham tahmin etiketleri: {raw_preds}")

    y_true = []
    y_pred = []
    wrong_samples = []

    for sample_id, true_label in ground_truths.items():
        if sample_id in predictions:
            pred_label = predictions[sample_id]
            y_true.append(true_label)
            y_pred.append(pred_label)
            
            if true_label != pred_label:
                wrong_samples.append({
                    "sample_id": sample_id,
                    "true": true_label,
                    "pred": pred_label
                })

    if not y_true:
        print("Değerlendirilecek geçerli veri bulunamadı.")
        return

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, pos_label="private", zero_division=0)
    rec = recall_score(y_true, y_pred, pos_label="private", zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label="private", zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=["private", "non_private"])

    print("="*45)
    print("📊 MODÜL A (GİZLİLİK) KESİN DEĞERLENDİRME RAPORU")
    print("="*45)
    print(f"Toplam İncelenen Örnek Sayısı : {len(y_true)}")
    print(f"Accuracy (Genel Doğruluk)     : {acc:.4f}")
    print(f"Precision (Kesinlik)          : {prec:.4f}")
    print(f"Recall (Duyarlılık - Private) : {rec:.4f}")
    print(f"F1 Score                      : {f1:.4f}")
    print("-" * 45)
    print("🔲 2x2 Confusion Matrix [private, non_private]:")
    print(cm)
    print("="*45)
    print(f"❌ Yanlış Tahmin Edilen Örnek Sayısı: {len(wrong_samples)}")
    print("Örnek Hatalar:")
    for ws in wrong_samples[:3]:
        print(f" - {ws['sample_id']}: Gerçek = {ws['true']}, Model Tahmini = {ws['pred']}")

if __name__ == "__main__":
    evaluate_privacy_results()