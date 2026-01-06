from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pickle
import sys

sys.dont_write_bytecode = True

app = FastAPI()
templates = Jinja2Templates(directory="templates")

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

TAVSIYELER = {
    "Soğuk algınlığı": "Bol sıvı tüketimi ve dinlenme önerilir.",
    "Grip": "İstirahat, bol sıvı tüketimi faydalı olabilir.",
    "Astım": "Tetikleyici faktörlerden kaçının ve düzenli ilaç kullanın.",
    "Migren": "Sessiz ve karanlık ortamda dinlenmek önerilir.",
    "Gastrit": "Asitli ve baharatlı yiyeceklerden kaçının.",
    "Diyabet": "Kan şekeri takibi ve dengeli beslenme önemlidir.",
    "Hipertansiyon": "Tuz tüketimini azaltın ve tansiyonunuzu takip edin.",
    "Eklem iltihabı": "Eklem zorlanmalarından kaçının.",
    "Depresyon": "Uzman desteği ve sosyal destek önemlidir.",
    "Kalp hastalığı": (
        "⚠️ Göğüs ağrısı ve nefes darlığında DERHAL 112’yi arayınız."
    )
}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/tahmin", response_class=HTMLResponse)
def tahmin(request: Request, belirti: str = Form(...)):

    sonuc = None
    tavsiye = None
    acil = False
    aciklama = None

    if not belirti.strip():
        aciklama = "Lütfen bir şikayet giriniz."
    else:
        try:
            sonuc = model.predict([belirti])[0]
            tavsiye = TAVSIYELER.get(sonuc)

            if sonuc == "Kalp hastalığı":
                acil = True

        except Exception:
            aciklama = "Tahmin sırasında bir hata oluştu."

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "sonuc": sonuc,
            "tavsiye": tavsiye,
            "acil": acil,
            "aciklama": aciklama,
            "belirti": belirti
        }
    )
