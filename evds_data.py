import requests
import json
from urllib.parse import urlencode
import pandas as pd


class GetData():
    def __init__(self,start_date,end_date,api_key) -> None:
        self.series_codes = ["TP.KTF11", ## Tasit kredisi faiz oranları
            "TP.FG.J071", ## Arac satin alimi tüfe
            "TP.FG.J0", ## Genel enflasyon tüfe
            "TP.BRENTPETROL.EUBP", ## Avrupa brent pretrol spot fiyatı
            "TP.KREDI.L013", ## Ticari ve bireysel krediler
            "TP.GY9.N2.MA", ## reel kesim güven endeksi
            "TP.YISGUCU2.G2", ## isgücü
            "TP.YISGUCU2.G8", ## issizlik orani
            "TP.HKFE01", ## konut fiyat endeksi
            "TP.BEK.S01.A.S", ##aylık tüfe beklentisinin standast sapması
            "TP.BEK.S01.D.S", ## yıl sonu tüfe beklenti standart sampası
            "TP.TG2.Y01", ## tüketici güven endeksi
            "TP.APIFON4", ## Faiz
            "TP.TRY.MT02", ## Mevduat faizi
            "TP.TG2.Y08", ## mevcut dönemin dayanıklı tüketim malı almak icin uygunluğu
            "TP.TG2.Y09", ##dayanıklı tüketim mallarına harcama yapma üdşüncesi
            "TP.TG2.Y17", ## otomobil satın alma ihtimali
            "TP.UR.S08", ## toplam otomobil üretimi - binek
            "TP.UR.S11", ## toplam otomobil üretimi - kamyonet
            "TP.KKM.K2", ## kkm orjinal paraların abd milyar doları karşılıgı
            "TP.DK.EUR.A.YTL", ## EURO/TL
            "TP.DK.USD.A.YTL"]  ## USD/TL

        ## Request code
        self.series = "-".join(self.series_codes)
        self.series_code_new = [x.replace(".","_") for x in self.series_codes]
        self.column_mappign = {
            self.series_code_new[0]:"Tasit_Kredi_Faiz_Oran",
            self.series_code_new[1]:"Arac_Satin_Alim_Tufe",
            self.series_code_new[2]:"Genel_Enflasyon_Tufe",
            self.series_code_new[3]:"EU_Brent_Petrol_Spot",
            self.series_code_new[4]:"Ticari_Bireysel_Kredi",
            self.series_code_new[5]:"Guven_Endeksi",
            self.series_code_new[6]:"Isgucu",
            self.series_code_new[7]:"Issizlik_Oran",
            self.series_code_new[8]:"Konut_Fiyat_Endeksi",
            self.series_code_new[9]:"Aylik_Tufe_Beklenti_SS",
            self.series_code_new[10]:"YilSonu_Tufe_Beklenti_SS",
            self.series_code_new[11]:"Tuketici_Guven_Endeksi",
            self.series_code_new[12]:"Faiz",
            self.series_code_new[13]:"Mevduat_Faizi",
            self.series_code_new[14]:"DTM_Uygunluk",
            self.series_code_new[15]:"DTM_Harcama_Dusuncesi",
            self.series_code_new[16]:"Otomobil_Alma_Ihtimali",
            self.series_code_new[17]:"Otomobil_Uretim_Binek",
            self.series_code_new[18]:"Otomobil_Uretim_Kamyonet",
            self.series_code_new[19]:"KKM_Paralari_USD_Karsiligi",
            self.series_code_new[20]:"Euro_TL",
            self.series_code_new[21]:"USD_TL"
        }


        ## Parameters
        self.api_key = api_key
        self.start_date = start_date
        self.end_date= end_date
        self.frequency='5' # Aylık
        self.agg_type = 'avg'
        self.params = {
            'series': self.series,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'frequency': self.frequency,
            'type': 'json'
        }

        print(self.series)

        self.url = f'https://evds2.tcmb.gov.tr/service/evds/{urlencode(self.params)}'


    def request_evds(self):
        response = requests.get(url=self.url, headers={'key': self.api_key})
        formatted_response = json.loads(response.content)
        data = formatted_response['items']
        df = pd.DataFrame(data)
        df = df.drop("UNIXTIME",axis = 1)
        df["Tarih"] = pd.to_datetime(df['Tarih']) + pd.offsets.Day(0)
        object_columns = [x for x in df.columns if df[x].dtype == "object"]
        for col in object_columns:
            df[col] = df[col].astype("float")

        df = df.rename(columns=self.column_mappign)

        ## % Changes
        df["TUFE_Change"] = df["Genel_Enflasyon_Tufe"].pct_change() * 100
        df["Arac_Satin_Alim_Tufe_Change"] = df["Arac_Satin_Alim_Tufe"].pct_change() * 100
        
        return df