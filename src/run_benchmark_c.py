import os
import json
import time
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Literal

load_dotenv()
client = genai.Client()

# Sadece iki kelimeye izin vererek modeli kısıtlıyoruz
class AnomalyResponse(BaseModel):
    prediction: Literal["normal", "anomaly"]
    reason_tr: str
    needs_human_review: bool

def run_anomaly_benchmark():
    prompt_path = "prompts/anomaly.txt"
    manifest_path = "data/manifests/anomaly.txt"
    results_dir = "results"
    cache_dir = "results/cache_anomaly/"
    results_file = "results/anomaly_results.jsonl"

    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        base_prompt = f.read()

    records = []

    if not os.path.exists(manifest_path):
        print(f"HATA: Manifest dosyası bulunamadı: {manifest_path}")
        return

    with open(manifest_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            sample_id = item['sample_id']
            image_path = item['image_path']
            
            if not os.path.exists(image_path):
                alt_name = os.path.basename(image_path)
                if os.path.exists(alt_name):
                    image_path = alt_name
                elif os.path.exists(os.path.join("data", alt_name)):
                    image_path = os.path.join("data", alt_name)

            cache_path = os.path.join(cache_dir, f"{sample_id}.json")

            if os.path.exists(cache_path):
                print(f"[CACHE] {sample_id} atlanıyor...")
                with open(cache_path, 'r', encoding='utf-8') as cf:
                    records.append(json.loads(cf.read()))
                continue

            print(f"[API] İşleniyor: {sample_id} ({image_path})")

            try:
                img = Image.open(image_path)
                start_time = time.time()
                
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=[img, base_prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=AnomalyResponse,
                        temperature=0.1
                    )
                )
                latency_ms = int((time.time() - start_time) * 1000)
                time.sleep(10)

                res_data = json.loads(response.text)
                
                result_record = {
                    "sample_id": sample_id,
                    "prediction": res_data.get("prediction"),
                    "reason_tr": res_data.get("reason_tr"),
                    "needs_human_review": res_data.get("needs_human_review", False),
                    "latency_ms": latency_ms,
                    "api_error": None
                }

                with open(cache_path, 'w', encoding='utf-8') as cf:
                    json.dump(result_record, cf, ensure_ascii=False, indent=2)
                
                records.append(result_record)

            except Exception as e:
                print(f"HATA ({sample_id}): {e}")
                records.append({
                    "sample_id": sample_id,
                    "prediction": "error",
                    "reason_tr": str(e),
                    "needs_human_review": True,
                    "latency_ms": 0,
                    "api_error": str(e)
                })

    with open(results_file, 'w', encoding='utf-8') as rf:
        for record in records:
            rf.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"✅ İşlem tamamlandı! Toplam {len(records)} kayıt {results_file} dosyasına yazıldı.")

if __name__ == "__main__":
    run_anomaly_benchmark()