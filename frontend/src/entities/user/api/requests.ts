import { baseURL } from 'app/api';
import { User } from '../types';

interface UserParams {
  login: string;
  password: string;
}

export const getUsers = async () => {
  const url = `${baseURL}/users`;
  const response = await fetch(url);
  const users: User[] = await response.json();
  return users;
};

export const getUser = async (
  { login, password }: UserParams,
  checkPassword = true,
) => {
  const url = `${baseURL}/users?login=${login}`;
  const response = await fetch(url);
  const [user]: User[] = await response.json();
  if (checkPassword) {
    return user?.password === password ? user : null;
  }
  return user ?? null;
};

export const createUser = async (params: UserParams) => {
  const overlap = await getUser(params, false);
  if (overlap) {
    alert('Такой пользователь уже есть');
    return;
  }
  console.log('createUser');
  const url = `${baseURL}/users`;
  const response = await fetch(url, {
    method: 'POST',
    body: JSON.stringify(params),
    headers: { 'Content-Type': 'application/json' },
  });
  const user: User = await response.json();
  return user;
};
