import { baseURL } from 'app/api';
import { Entity } from '../types';

type GetParams = {
  _page: string;
  _limit: string;
  name_like: string;
};

export const getEntities = async (params: GetParams) => {
  const search = new URLSearchParams(params).toString();
  const url = `${baseURL}/entities?${search}&_expand=user`;
  const response = await fetch(url);
  const entities: Entity[] = await response.json();
  const count = Number(response.headers.get('X-Total-Count'));
  const pageCount = Math.ceil(count / Number(params._limit));
  return { items: entities, pageCount };
};

export const getEntity = async (id: string) => {
  const url = `${baseURL}/entities/${id}`;
  const response = await fetch(url);
  const entity: Entity = await response.json();
  return entity;
};

interface CreateParams {
  name: string;
  description: string;
  type: string;
}

export const createEntity = async (params: CreateParams) => {
  const url = `${baseURL}/entities`;
  const response = await fetch(url, {
    method: 'POST',
    body: JSON.stringify(params),
    headers: { 'Content-Type': 'application/json' },
  });
  const entity: Entity = await response.json();
  return entity;
};

interface UpdateParams {
  id: string;
  name: string;
  description: string;
  userId: string;
}

export const updateEntity = async (params: UpdateParams) => {
  const url = `${baseURL}/entities/${params.id}`;
  const response = await fetch(url, {
    method: 'PUT',
    body: JSON.stringify(params),
    headers: { 'Content-Type': 'application/json' },
  });
  const entity: Entity = await response.json();
  return entity;
};

export const deleteEntity = async (id: string) => {
  const url = `${baseURL}/entities/${id}`;
  const response = await fetch(url, {
    method: 'DELETE',
  });
  const entity: Entity = await response.json();
  return entity;
};
