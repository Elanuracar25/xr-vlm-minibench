import os
import json
import random

def build_answerability_subset():
    os.makedirs("data/manifests", exist_ok=True)
    
    annotation_path = "data/raw/val.json" 
    manifest_path = "data/manifests/answerability.jsonl"
    
    if not os.path.exists(annotation_path):
        print(f"Uyarı: {annotation_path} bulunamadı!")
        return

    with open(annotation_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    answerable_samples = []
    unanswerable_samples = []
    
    for item in data:
        image_name = item.get("image")
        answers = [a["answer"] for a in item.get("answers", [])]
        
        is_unanswerable = any(ans == "unanswerable" for ans in answers)
        
        # Resimler data/raw/val/ klasörünün içinde
        image_path = f"data/raw/val/{image_name}"
        
        sample_info = {
            "source_dataset": "VizWiz-VQA",
            "split": "validation",
            "license": "CC BY 4.0"
        }
        
        if os.path.exists(image_path):
            sample_info["image_path"] = image_path
            
            if is_unanswerable and len(unanswerable_samples) < 25:
                sample_info["sample_id"] = f"answerability_{len(unanswerable_samples)+26:04d}"
                sample_info["task"] = "answerability"
                sample_info["ground_truth"] = "unanswerable"
                unanswerable_samples.append(sample_info)
            elif not is_unanswerable and len(answerable_samples) < 25:
                sample_info["sample_id"] = f"answerability_{len(answerable_samples)+1:04d}"
                sample_info["task"] = "answerability"
                sample_info["ground_truth"] = "answerable"
                answerable_samples.append(sample_info)
                
        if len(answerable_samples) >= 25 and len(unanswerable_samples) >= 25:
            break
            
    final_samples = answerable_samples + unanswerable_samples
    random.shuffle(final_samples)
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        for sample in final_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            
    print(f"Harika! Toplam {len(final_samples)} örnek (25 answerable, 25 unanswerable) seçildi.")
    print(f"Manifest dosyası oluşturuldu: {manifest_path}")

if __name__ == "__main__":
    build_answerability_subset()