import { useForm } from 'react-hook-form';
import { HouseFormData, schema } from './schema';
import { zodResolver } from '@hookform/resolvers/zod';
interface HouseDataFormProps {
  suburbs: string[];
  onSubmit: (data: HouseFormData) => unknown;
}
const HouseDataForm = ({ onSubmit, suburbs }: HouseDataFormProps) => {
  const {
    register,
    reset,
    formState: { isSubmitSuccessful, errors },
    handleSubmit,
  } = useForm<HouseFormData>({
    resolver: zodResolver(schema),
  });
  isSubmitSuccessful && reset();
  console.log(errors);
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Suburb</label>
        <select {...register('Suburb')}>
          {suburbs.map((suburb) => (
            <option key={suburb}>{suburb}</option>
          ))}
        </select>
      </div>
      <div>
        <label>Bedrooms</label>
        <input type="number" {...register('Rooms')} />
      </div>
      <div>
        <label>Bathrooms</label>
        <input type="number" {...register('Bathroom')} />
      </div>
      <div>
        <button type="submit">Predict</button>
      </div>
    </form>
  );
};

export default HouseDataForm;
