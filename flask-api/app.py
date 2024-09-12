from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

app = Flask(__name__)
CORS(app)

print("Hello")

spark = SparkSession.builder.master("spark://spark-master:7077").appName("MelbourneHousePricingAPI").getOrCreate()

loaded_model = PipelineModel.load("/app/model/spark_melbourne_house_price_model")
print("world")
schema = StructType([
    StructField("Suburb", StringType(), True),
    StructField("Rooms", IntegerType(), True),
    StructField("Bathroom", IntegerType(), True),
    StructField("Landsize", DoubleType(), True),
    StructField("BuildingArea", DoubleType(), True),
    StructField("YearBuilt", IntegerType(), True)
])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    suburb = data['suburb']
    rooms = int(data['rooms'])
    bathroom = int(data['bathroom'])
    landsize = float(data.get('landsize', 0))
    building_area = float(data.get('buildingArea', 0))
    year_built = int(data.get('yearBuilt', 2000))

    input_data = spark.createDataFrame([(suburb, rooms, bathroom, landsize, building_area, year_built)], schema=schema)
    
    prediction = loaded_model.transform(input_data)
    

    predicted_price = prediction.select("prediction").collect()[0][0]

    return jsonify({'predicted_price': predicted_price})

if __name__ == '__main__':
    print("App running")
    app.run(host='0.0.0.0', port=5000)