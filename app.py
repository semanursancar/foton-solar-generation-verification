from flask import Flask, render_template, request
import pandas as pd
import requests
import json


app = Flask(__name__)

def MonthlyAverageSolarGeneration(lat, lon, peakpower):

    # GET isteği yapacağımız URL'yi belirtiyoruz
    url = 'https://re.jrc.ec.europa.eu/api/PVcalc?lat={}&lon={}&peakpower={}&loss=0&angle=35&outputformat=json'.format(lat, lon, peakpower)
    
    # GET isteğini gönderiyoruz
    response = requests.get(url)
    
    # Yanıtı kontrol ediyoruz
    if response.status_code == 200:
        # Yanıtın içeriğini alıyoruz
        content = response.text
    
        # İçeriği yazdırıyoruz
        # print(content)
    else:
        print('İstek başarısız oldu. Hata kodu:', response.stat.us_code)
    
    # Metin verisini JSON formatına dönüştürüyoruz
    data = json.loads(content)
    
    # 'outputs' ve 'monthly' verilerini alıyoruz
    outputs_monthly = data['outputs']['monthly']['fixed']
    
    # DataFrame oluşturmak için verileri düzenliyoruz
    df = pd.DataFrame(outputs_monthly)

    table = df[["month","E_m", "SD_m"]]

    table.rename(columns={"month":"Months", "E_m": "Average Generation [kW]", "SD_m":"Standart Dev."}, inplace=True)

    # years
    year_min = data['inputs']['meteo_data']['year_min']
    year_max = data['inputs']['meteo_data']['year_max']

    note = "The data includes the average of {} and {}.".format(year_min, year_max)    
    
    # DataFrame'i yazdırıyoruz
    # print(df)

    return table, note

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # HTML formundan girilen değerleri alın
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        num3 = float(request.form['num3'])
        
        # Fonksiyonu çağırıp ortalamayı hesaplayın
        table, user_note = MonthlyAverageSolarGeneration(num1, num2, num3)

        plant_data = "Latitude: {} Longitude: {} Installed Power [kW]: {}".format(num1, num2, num3)  
        
        # DataFrame'i HTML olarak render eden 'result.html' sayfasına yönlendirin
        return render_template('result.html', df=table.to_html(index=False), user_note=user_note, inputs = plant_data)
    
    # İlk defa sayfayı yüklerken veya GET isteği yapıldığında
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
