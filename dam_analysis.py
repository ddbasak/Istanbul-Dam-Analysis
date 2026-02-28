import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import os
matplotlib.use('TkAgg') # Grafik penceresinin açılması için 

file_path = "dam_data.csv"

try:
    # Veriyi Oku
    print(f"'{file_path}' dosyasını okumaya çalışıyorum...")
    df = pd.read_csv(file_path)
    print("Veri başarıyla okundu. İlk 3 satır:")
    print(df.head(3))
    print("\nSütun isimleri:")
    print(df.columns.tolist())

    # Tarih Sütununu Doğru Formata Çevir ve Sırala
    if 'Tarih' in df.columns:
        print("\n'Tarih' sütunu bulundu. Dönüştürülüyor...")
        df['Tarih'] = pd.to_datetime(df['Tarih'], errors='coerce') # Hatalı tarihleri NaN yapar
        df.dropna(subset=['Tarih'], inplace=True) # NaN olan tarih satırlarını kaldır
        df.sort_values('Tarih', inplace=True)
        print("Tarih sütunu dönüştürüldü ve sıralandı.")
    else:
        raise ValueError("Hata: 'Tarih' adında bir sütun bulunamadı. Lütfen CSV başlıklarını kontrol edin.")

    # Baraj Sütunları Belirle
    baraj_sutunlari = ['Omerli', 'Darlik', 'Elmali', 'Terkos', 'Alibey',
                       'Buyukcekmece', 'Sazlidere', 'Kazandere', 'Pabucdere', 'Istrancalar']

    # Veri setinizde bu sütunların var olup olmadığını kontrol.
    mevcut_baraj_sutunlari = [col for col in baraj_sutunlari if col in df.columns]
    if not mevcut_baraj_sutunlari:
        raise ValueError("Hata: Belirtilen baraj sütunlarından hiçbiri veri setinde bulunamadı. Lütfen sütun isimlerini kontrol edin.")
    
    print(f"\nGrafiğe dahil edilecek baraj sütunları: {mevcut_baraj_sutunlari}")

    # Doluluk oranlarını sayısal türe çevir ve eksik/hatalı değerleri temizle
    for col in mevcut_baraj_sutunlari:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=mevcut_baraj_sutunlari, inplace=True) # Sayısal olmayan veya eksik değerleri içeren satırları at

    # Veri kontrolü
    print(f"Veri temizleme sonrası kalan satır sayısı: {len(df)}")
    if len(df) == 0:
        raise ValueError("Hata: Veri temizleme sonrası grafiği çizecek yeterli veri kalmadı. Veri setinizi kontrol edin.")

    # Veriyi Grafiğe Hazırla 
    df_melted = df.melt(id_vars=['Tarih'], value_vars=mevcut_baraj_sutunlari,
                        var_name='Baraj', value_name='Doluluk Oranı')
    
    print("\nVeri grafik için hazırlandı (melted DataFrame'in ilk 3 satırı):")
    print(df_melted.head(3))


    # Grafiği Çiz
    print("\nGrafik oluşturuluyor...")
    plt.figure(figsize=(16, 8)) # Geniş ekranlar için daha uygun boyut
    sns.lineplot(x='Tarih', y='Doluluk Oranı', hue='Baraj', data=df_melted)

    # Grafik Başlık ve Etiketleri
    plt.title('İstanbul Barajları Günlük Doluluk Oranları Zaman Serisi', fontsize=20, pad=20)
    plt.xlabel('Tarih', fontsize=14)
    plt.ylabel('Doluluk Oranı (%)', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(title='Barajlar', bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, fontsize=9, title_fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Grafiği Göster
    plt.tight_layout(rect=[0, 0, 0.98, 1]) # Lejantın dışarıda kalması için düzenleme
    print("Grafik gösteriliyor...")
    plt.show()

    print("\nKod başarıyla tamamlandı.")

except FileNotFoundError:
    print(f"\n**HATA: '{file_path}' dosyası bulunamadı.**")
    print("Lütfen dosyanın, Python betiğinizle aynı klasörde olduğundan emin olun.")
    print(f"Mevcut çalışma dizini: {os.getcwd()}")
except ValueError as ve:
    print(f"\n**HATA: Veri işleme sırasında bir sorun oluştu.**")
    print(f"Detay: {ve}")
    print("Lütfen CSV dosyanızdaki sütun isimlerini ve veri formatlarını kontrol edin.")
except Exception as e:
    print(f"\n**BEKLENMEDİK BİR HATA OLUŞTU:** {e}")
    print("Yukarıdaki çıktıları inceleyerek hatanın nedenini anlamaya çalışabilirsiniz.")
