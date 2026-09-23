import json
import os
import random

def evaluate_answerability():
    manifest_path = "data/manifests/answerability.jsonl"
    results_path = "results/answerability_results.jsonl"

    if not os.path.exists(manifest_path) or not os.path.exists(results_path):
        print("Hata: Manifest veya sonuç dosyası bulunamadı.")
        return

    ground_truths = {}
    with open(manifest_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                ground_truths[data["sample_id"]] = data["ground_truth"]

    correct = 0
    total = 0
    
    # Unanswerable sınıfını "Pozitif" sınıf olarak kabul ediyoruz (Yönerge gereği)
    TP = 0 # Doğru bilinen Unanswerable
    FP = 0 # Yanlışlıkla Unanswerable denilenler (Aslında Answerable)
    FN = 0 # Yanlışlıkla Answerable denilenler (Aslında Unanswerable)
    TN = 0 # Doğru bilinen Answerable
    
    hatali_istek = 0
    hatali_ornekler = []

    with open(results_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                sample_id = data["sample_id"]
                prediction = data.get("prediction")
                reason = data.get("reason_tr", "Sebep belirtilmemiş")
                
                if sample_id not in ground_truths:
                    continue
                    
                truth = ground_truths[sample_id]
                total += 1
                
                if prediction == "error" or prediction is None:
                    hatali_istek += 1
                    continue

                if prediction == truth:
                    correct += 1
                    if truth == "unanswerable":
                        TP += 1
                    else:
                        TN += 1
                else:
                    hatali_ornekler.append({"id": sample_id, "truth": truth, "pred": prediction, "reason": reason})
                    if prediction == "unanswerable":
                        FP += 1  # Model unanswerable dedi ama gerçekte answerable
                    else:
                        FN += 1  # Model answerable dedi ama gerçekte unanswerable

    accuracy = (correct / total) * 100 if total > 0 else 0
    precision = (TP / (TP + FP)) * 100 if (TP + FP) > 0 else 0
    recall = (TP / (TP + FN)) * 100 if (TP + FN) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print("\n=== Modül B (Cevaplanabilirlik) Gelişmiş Metrikler ===")
    print(f"Toplam İşlenen Görsel: {total} | Hatalı İstek: {hatali_istek}")
    print(f"Accuracy (Genel Başarı):  %{accuracy:.2f}")
    print(f"Precision (Kesinlik):     %{precision:.2f}")
    print(f"Recall (Duyarlılık):      %{recall:.2f}  <-- Yönerge Ana Metriği")
    print(f"F1 Score:                 %{f1_score:.2f}")
    print("-" * 55)
    print("Confusion Matrix (Karmaşıklık Matrisi):")
    print(f"True Positive (Doğru Unanswerable): {TP}")
    print(f"True Negative (Doğru Answerable):   {TN}")
    print(f"False Positive (Yanlış Unanswerable):{FP}")
    print(f"False Negative (Yanlış Answerable): {FN}")
    
    print("\n=== YÖNERGE ZORUNLULUĞU: HATA ANALİZİ İÇİN 5 ÖRNEK ===")
    if len(hatali_ornekler) > 0:
        secilen_hatalar = random.sample(hatali_ornekler, min(5, len(hatali_ornekler)))
        for idx, hata in enumerate(secilen_hatalar, 1):
            print(f"{idx}. Görsel ID: {hata['id']}")
            print(f"   Gerçekte: {hata['truth']} | Modelin Tahmini: {hata['pred']}")
            print(f"   Modelin Gerekçesi: {hata['reason']}\n")
    else:
        print("Harika! Hiç hata bulunamadı.")

if __name__ == "__main__":
    evaluate_answerability()