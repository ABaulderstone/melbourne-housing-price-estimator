import * as z from 'zod';

export const schema = z.object({
  Suburb: z.string().min(1),
  Bathroom: z.coerce.number().min(1),
  Rooms: z.coerce.number().min(1),
});

export type HouseFormData = z.infer<typeof schema>;
