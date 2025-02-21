## Тестовое задание в команду ассистеда (Python)

### В папке ```./data``` два XML – это ответы на поисковые запросы

[RS_Via-3.xml](data/RS_Via-3.xml)

[RS_ViaOW.xml](data/RS_ViaOW.xml)

В ответах лежат варианты перелётов (тег `Flights`) со всей необходимой информацией,
чтобы отобразить билет на Aviasales.

На основе этих данных, сделан вебсервис,
в котором есть эндпоинты, отвечающие на следующие запросы:

* ```/onward-flights``` -> Какие варианты перелёта из DXB в BKK мы получили?
* ```/best-flights``` -> Самый дорогой/дешёвый, быстрый/долгий и оптимальный варианты
* ```/compare-flights``` -> В чём отличия между результатами двух запросов (изменение маршрутов/условий)?


Язык реализации: `python3`
Формат ответа: `json`

## Dependencies / Зависимости
```
1. fastapi
2. pydantic
3. uvicorn
4. lxml
```

## Instruction to upload & install / Инструкция по установке и запуску

```1. git clone https://github.com/AntiViruS90/AviaSales.git```

```2. cd AviaSales```

```3. pip install -r requirements.txt```

```4. uvicorn main:app --reload```

```5. go to your browser and enter link http://127.0.0.1:8000/swagger#/```
