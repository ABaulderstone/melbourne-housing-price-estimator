import { HouseFormData } from '../components/HouseDataForm/schema';

interface GetSuburbsResponse {
  suburbs: string[];
}

interface PredictionResponse {
  predicted_price: number;
}

const BASE_URL = import.meta.env.VITE_API_URL;

export const getAllSuburbs = async () => {
  const response = await fetch(BASE_URL + '/suburbs');
  if (!response.ok) throw new Error('Failed to get suburbs');
  return (await response.json()) as GetSuburbsResponse;
};

export const getPrediction = async (data: HouseFormData) => {
  const response = await fetch(BASE_URL + '/predict', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) throw new Error('Failed to predict');
  return (await response.json()) as PredictionResponse;
};
