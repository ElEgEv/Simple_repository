import { User } from 'entities/user';

export interface Entity {
  id: string;
  name: string;
  description: string;
  user: User;
}
