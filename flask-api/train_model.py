from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder, StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator

spark = SparkSession.builder.appName("MelbourneHousePricingPrediction").getOrCreate()
data = spark.read.csv("melbourne_housing_data.csv", header=True, inferSchema=True)

features = ['Suburb', 'Rooms', 'Bathroom', 'Landsize', 'BuildingArea', 'YearBuilt', 'Price']
data = data.select(features)


data = data.na.drop(subset=['Suburb', 'Rooms', 'Bathroom', 'Price'])
data = data.na.fill(data.select([c for c in data.columns if c != 'Suburb']).summary().collect()[1])


indexer = StringIndexer(inputCol="Suburb", outputCol="SuburbIndex")


encoder = OneHotEncoder(inputCol="SuburbIndex", outputCol="SuburbVec")


numericCols = ['Rooms', 'Bathroom', 'Landsize', 'BuildingArea', 'YearBuilt']
assembler = VectorAssembler(inputCols=numericCols + ["SuburbVec"], outputCol="features")


scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")


lr = LinearRegression(featuresCol="scaledFeatures", labelCol="Price")


pipeline = Pipeline(stages=[indexer, encoder, assembler, scaler, lr])

train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)


model = pipeline.fit(train_data)


predictions = model.transform(test_data)


evaluator = RegressionEvaluator(labelCol="Price", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE) on test data = {rmse}")

r2_evaluator = RegressionEvaluator(labelCol="Price", predictionCol="prediction", metricName="r2")
r2 = r2_evaluator.evaluate(predictions)
print(f"R2 on test data = {r2}")


model.write().overwrite().save("/app/model/spark_melbourne_house_price_model")


spark.stop()
