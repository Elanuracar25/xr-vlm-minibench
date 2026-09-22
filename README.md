# XR-VLM MiniBench - Modül A: Gizlilik Değerlendirmesi

Bu depo, TÜBİTAK projesi kapsamında VizWiz-Priv veri seti kullanılarak Görsel Dil Modellerinin (VLM) gizlilik modülünün değerlendirilmesi için hazırlanmıştır.

## Proje Yapısı
- `data/manifests/privacy.jsonl`: 50 örnekten oluşan test manifesti (25 private, 25 non_private).
- `src/run_benchmark.py`: Görselleri modele gönderip sonuçları cache'leyen ana test betiği.
- `src/evaluate.py`: scikit-learn kullanarak metrikleri (Accuracy, Precision, Recall, F1 ve Confusion Matrix) hesaplayan değerlendirme betiği.
- `results/privacy_results.jsonl`: Modelin ham tahmin çıktıları.

## Kurulum ve Çalıştırma Adımları
1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install google-genai pillow pydantic python-dotenv scikit-learn

   Ana deneyi koşturmak için:

Bash
python src/run_benchmark.py

Metrikleri ve Confusion Matrix tablosunu görmek için:

Bash
python src/evaluate.py



## Modül C: Anomali Tespiti Hata Analizi
MVTec LOCO AD - "Juice Bottle" Hata Analizi

Aşırı Hassasiyet ve Yanlış Alarmlar (False Positives): Model, sağlam (normal) şişelerdeki kabul edilebilir üretim toleranslarını veya kamera açısından kaynaklanan görsel yanılsamaları "kritik hata" olarak etiketlemeye çok meyilli. 1. ve 6. örneklerde (anomaly_normal_0009 ve 0003) etiketlerdeki milimetrik eğrilikleri, 2. örnekte (anomaly_normal_0021) ise dolum seviyesindeki ufak bir farkı anomali sanmış. Model, "mükemmel" bir referans şişe hayal edip en ufak sapmada alarm veriyor.

Gerçek Kusurları Gözden Kaçırma (False Negatives): Model, resmin bütününe bakıp etiket ve dolum oranı normalse detaya inmiyor. 3, 4 ve 5 numaralı örneklerde (anomaly_struct_0000, 0010, 0011) şişenin üzerindeki asıl yapısal kusurları (çizik, göçük veya kirlilik gibi) tamamen gözden kaçırmış ve "her şey normal standartlarda" diyerek asıl yakalaması gereken arızalı ürünleri üretim bandından geçirmiş.

Talimat (Prompt) Zafiyeti: 5. örnekte (anomaly_struct_0011), model kendisine verilen reason_tr (Türkçe açıklama) talimatını anlık olarak unutup İngilizce çıktı üretmiş. Bu durum, LLM'lerde sıklıkla karşılaşılan ve yapılandırılmış çıktıların (JSON) dil komutlarını ezebildiğini gösteren klasik bir prompt hizalama sorunudur.