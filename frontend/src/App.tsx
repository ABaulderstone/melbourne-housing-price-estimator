import { useEffect, useState } from 'react';
import './App.css';
import { getAllSuburbs, getPrediction } from './services/prediction-service';
import HouseDataForm from './components/HouseDataForm/HouseDataForm';
import { HouseFormData } from './components/HouseDataForm/schema';

function App() {
  const [suburbs, setSuburbs] = useState<string[]>([]);
  const [predictedPrice, setPredictedPrice] = useState<string>('');
  useEffect(() => {
    getAllSuburbs().then((res) => setSuburbs(res.suburbs));
  }, []);

  const onSubmit = async (data: HouseFormData) => {
    const { predicted_price } = await getPrediction(data);
    setPredictedPrice(predicted_price.toFixed(0));
  };
  return (
    <>
      <HouseDataForm suburbs={suburbs} onSubmit={onSubmit} />
      {predictedPrice && <h4>Estimated Price: ${predictedPrice}</h4>}
    </>
  );
}

export default App;
