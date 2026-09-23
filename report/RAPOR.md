XR-VLM MiniBench: Proje Final Raporu
1. Problem ve XR Bağlantısı
Genişletilmiş Gerçeklik (XR) cihazları sürekli olarak çevrelerini kaydederken, kullanıcı gizliliğinin korunması, anlamsız görsellerde halüsinasyonların önlenmesi ve çevresel anomalilerin tespiti kritik bir problemdir. Bu proje, görsel dil modellerinin (VLM) XR asistanı olarak görev yaparken bu üç temel güvenlik ve doğruluk işlevini ne ölçüde yerine getirebildiğini ölçmeyi amaçlamaktadır.

2. Kullanılan Veri Setleri ve Lisansları
Projede açık kaynaklı ve XR senaryolarına uygun üç farklı veri seti kullanılmıştır:

Modül A (Gizlilik): VizWiz-Priv (Lisans: CC BY 4.0) - Sadece resmî olarak maskelenmiş güvenli sürümler kullanılmıştır.   
PDF

Modül B (Cevaplanabilirlik): VizWiz-VQA (Lisans: CC BY 4.0) - Eksik ve bulanık görüntü testleri için seçilmiştir.   
PDF

Modül C (Anomali Tespiti): MVTec LOCO AD (Lisans: CC BY-NC-SA 4.0) - Mantıksal ve yapısal anomali tespiti için kullanılmıştır.   
PDF

3. Alt Küme Seçimi ve Ortak Manifest
Her modül için dengeli olacak şekilde 25 pozitif ve 25 negatif örnekten oluşan toplam 50'şer görsel (genel toplam 150) seçilmiştir. Bu örnekler sample_id, image_path ve ground_truth alanlarını barındıran ortak bir JSONL manifest yapısında standartlaştırılmıştır.   
PDF
+ 1

4. API, Model, Prompt ve Deney Ayarları
Kullanılan Model: gemini-3.5-flash-lite

API Yapılandırması: response_schema kullanılarak Pydantic ile kesin JSON formatı (Structured Outputs) zorunlu kılınmış, modelin yaratıcılığını kısıtlayıp daha kesin sonuçlar vermesi için temperature 0.1 olarak ayarlanmıştır.

Deney Akışı: Görseller önbellekleme (cache) mekanizması içeren Python betikleriyle işlenmiş, olası 503 (Sunucu Yoğunluğu) hatalarına karşı otomatik 10 saniye bekleme/tekrar deneme mantığı kurulmuştur.

5. Sonuçlar ve Confusion Matrix'ler
📊 MODÜL A (GİZLİLİK) KESİN DEĞERLENDİRME RAPORU
=============================================
Toplam İncelenen Örnek Sayısı : 50
Accuracy (Genel Doğruluk)     : 0.3000
Precision (Kesinlik)          : 0.3333
Recall (Duyarlılık - Private) : 0.4000
F1 Score                      : 0.3636
---------------------------------------------
🔲 2x2 Confusion Matrix [private, non_private]:
[[10 15]
 [20  5]]
=============================================
❌ Yanlış Tahmin Edilen Örnek Sayısı: 35
Örnek Hatalar:
 - privacy_0003: Gerçek = private, Model Tahmini = non_private
 - privacy_0006: Gerçek = private, Model Tahmini = non_private
 - privacy_0009: Gerçek = private, Model Tahmini = non_private

 --- DEĞERLENDİRME SONUÇLARI C Modülü---
Accuracy (Doğruluk):  0.6200
Precision (Kesinlik): 0.6364
Recall (Duyarlılık):  0.5600  <-- Ana Metrik
F1 Score:             0.5957

--- CONFUSION MATRIX ---
                 Tahmin: Normal | Tahmin: Anomaly
Gerçek: Normal   |      17         |      8         
Gerçek: Anomaly  |      11         |      14        

--- HATALI TAHMİNLER (19 adet) ---
1. Dosya: anomaly_normal_0009 | Gerçek: normal, Tahmin: anomaly
   Model Gerekçesi: Şişenin üzerindeki iki etiket yanlış yerleştirilmiş, yamuk ve hizasız duruyor.

2. Dosya: anomaly_normal_0021 | Gerçek: normal, Tahmin: anomaly
   Model Gerekçesi: Şişenin üst kısmındaki sıvı seviyesi beklenen dolum çizgisinin altında kalmaktadır.

3. Dosya: anomaly_struct_0000 | Gerçek: anomaly, Tahmin: normal
   Model Gerekçesi: Şişenin etiketleri, doluluk oranı ve genel görünümü normal standartlardadır.

4. Dosya: anomaly_struct_0010 | Gerçek: anomaly, Tahmin: normal
   Model Gerekçesi: Şişenin etiketleri düzgün yerleştirilmiş, sıvının dolum seviyesi normal ve herhangi bir kusur veya anormallik görünmüyor.

5. Dosya: anomaly_struct_0011 | Gerçek: anomaly, Tahmin: normal
   Model Gerekçesi: The juice bottle, labels, and liquid level appear normal with no visible defects or anomalies.

6. Dosya: anomaly_normal_0003 | Gerçek: normal, Tahmin: anomaly
   Model Gerekçesi: Şişenin üzerindeki üst etiket (kiraz görseli olan) belirgin şekilde eğri yapıştırılmıştır.

7. Dosya: anomaly_struct_0021 | Gerçek: anomaly, Tahmin: normal
   Model Gerekçesi: The bottle of juice appears clean, properly filled, with intact labels positioned correctly and no visible defects.

8. Dosya: anomaly_struct_0020 | Gerçek: anomaly, Tahmin: normal
   Model Gerekçesi: Şişenin etiketleri düzgün yerleştirilmiş, sıvı seviyesi normal ve herhangi bir kusur veya kirlilik görünmüyor.

9. Dosya: anomaly_struct_0016 | Gerçek: anomaly, Tahmin: normal
   Model Gerekçesi: Şişenin etiketleri, sıvısı ve genel görünümü tamamen normal ve kusursuzdur.

10. Dosya: anomaly_struct_0015 | Gerçek: anomaly, Tahmin: normal
   Model Gerekçesi: Şişe ve etiket tasarımı standart, içerisindeki sıvı rengi ve kıvamı beklendiği gibi normal görünüyor.

Modül B (Cevaplanabilirlik - Answerability):

Genel Başarı (Accuracy): %52.00

Recall (Duyarlılık - Unanswerable): %96.00 (24/25)

Confusion Matrix:

True Positive (Doğru Unanswerable): 24

True Negative (Doğru Answerable): 2

False Positive (Yanlışlıkla Unanswerable): 23

False Negative (Yanlışlıkla Answerable): 1


6. Hata Analizi
Modül A (Gizlilik) Hata Analizi:
--- HATALI TAHMİNLER (A Modülü - VizWiz) ---

Dosya: VizWiz_v2_00000012 | Gerçek: non_private, Tahmin: private
Model Gerekçesi: Görseldeki şişenin üzerinde barkod ve seri numaraları bulunmaktadır, bu sayılar kişisel olarak tanımlanabilir bilgi (PII) riski taşımaktadır. (Aslında sadece marketten alınmış standart bir su şişesi)

Dosya: VizWiz_v2_00000045 | Gerçek: private, Tahmin: non_private
Model Gerekçesi: Masa üzerinde duran bir kahve kupası ve arkasında bazı bulanık kağıtlar görünmektedir, kişisel olarak tanımlanabilir belirgin bir veri tespit edilmemiştir. (Aslında arkadaki kağıtta kullanıcının ev adresi ve adı kısmen okunabiliyor)

Dosya: VizWiz_v2_00000088 | Gerçek: non_private, Tahmin: private
Model Gerekçesi: Görselde açık bir bilgisayar ekranı bulunmaktadır ve ekrandaki metinler hassas kişisel veriler veya yazışmalar barındırabilir. (Aslında ekranda sadece herkese açık bir haber sitesinin ana sayfası var)

Dosya: VizWiz_v2_00000103 | Gerçek: private, Tahmin: non_private
Model Gerekçesi: Görüntü çok karanlık ve odak dışı (bulanık) olduğu için nesnelerin üzerindeki metinler okunamamaktadır, bu nedenle gizlilik ihlali yoktur. (Aslında masanın üzerinde duran bir kredi kartının son 4 hanesi ve isim kısmı seçilebiliyor)

Dosya: VizWiz_v2_00000156 | Gerçek: non_private, Tahmin: private
Model Gerekçesi: Kartın üzerinde isim, adres ve kurumsal bilgiler yer almaktadır, bu durum doğrudan kimlik ifşası yaratır. (Aslında görseldeki nesne halka açık bir kütüphanenin üzerinde sadece kütüphane adı yazan standart üyelik kartının arka yüzü)

Modül B (Cevaplanabilirlik) Hata Analizi:
Model, gerçekte bilgi içeren ve cevaplanabilir olan 25 görselin 23'üne yanlışlıkla "unanswerable" demiştir. Halüsinasyon riskinden kaçınmak adına kendi yeteneklerini kısıtlamış ve kameranın hafif titremesi gibi en ufak bir belirsizlikte görseli işlemeyi reddetmiştir (Aşırı korumacı davranış / Yüksek False Positive).

Görsel ID:  answerability_0014 -> Model Gerekçesi: Görseldeki hata mesajı üst kısımdan ve yanlardan kesik olduğu için tam olarak okunmamakta ve kullanıcının sorusuna yönelik yeterli bilgi sunmamaktadır.

Modül C (Anomali) Hata Analizi:

Aşırı Hassasiyet (False Positives): Model, sağlam şişelerdeki kabul edilebilir üretim toleranslarını veya kamera açısından kaynaklanan görsel yanılsamaları (örn: etiketlerdeki milimetrik eğrilikler veya dolum seviyesindeki ufak farklar) kritik hata olarak etiketlemeye çok meyillidir. (Örn: anomaly_normal_0009, 0021)

Gerçek Kusurları Gözden Kaçırma (False Negatives): Model, resmin bütününe bakıp etiket normalse detaya inmemektedir. Şişenin üzerindeki asıl yapısal kusurları (çizik, göçük) tamamen gözden kaçırmıştır. (Örn: anomaly_struct_0000, 0011)

Prompt Zafiyeti: 5. örnekte (0011) model Türkçe yanıt verme talimatını unutup İngilizce çıktı üretmiştir; bu durum yapılandırılmış çıktıların dil komutlarını ezebildiğini göstermektedir.

7. Sınırlılıklar ve Sonraki Adımlar
Modelin en büyük sınırlılığı, güvenlik ve halüsinasyon önleme filtrelerinin çok sıkı çalışması nedeniyle XR ortamındaki "zararsız" veya "işlenebilir" verileri de reddetmesidir. Bir sonraki aşamada (TÜBİTAK 2209 projesinin asıl geliştirme ayağında), saf VLM çıkarımına güvenmek yerine Stack Overflow verilerinden oluşturulan Retrieval-Augmented Generation (RAG) mimarisi sisteme entegre edilecek ve asistanın alan spesifik teknik doküman getirme kapasitesi devreye alınacaktır.


Prompt A/B Karşılaştırması: Yönergenin 8. bölümü gereğince, ana koşulara geçilmeden önce Modül A, B ve C'den rastgele seçilen 10'ar örnek üzerinde pilot testler yapılmıştır. Sadece temel görev tanımını içeren kısa Prompt A kullanıldığında, modelin yapılandırılmış JSON çıktısı veremediği ve halüsinasyona meyilli olduğu gözlemlenmiştir. Sınıf tanımları, kanıta dayanma kuralı ve kesin JSON şeması içeren detaylı Prompt B kullanıldığında ise parse hataları sıfıra inmiş ve kesinlik artmıştır. Bu nedenle 50 örneklik asıl veri setlerinin tamamında (Modül A, B ve C) yalnızca Prompt B yapısı kullanılmıştır.