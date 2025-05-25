import { Button, MenuItem, Select, TextField, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { useNavigate, useParams } from 'react-router-dom';

import styles from './styles.module.css';
import { createEntity, getEntity, updateEntity } from 'entities/entity';
import { getUsers, User } from 'entities/user';

export const EntityPage = () => {
  const [users, setUsers] = useState<User[]>([]);

  const { id } = useParams();
  const isNew = id === 'new';

  const navigate = useNavigate();

  const fetchEntity = async () => {
    const entity = await getEntity(id);
    reset(entity);
  };

  const fetchUsers = async () => {
    const users = await getUsers();
    setUsers(users);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm();

  useEffect(() => {
    if (!isNew) {
      fetchEntity();
    } else {
      reset({ id: null });
    }
  }, [id]);

  const handleFormSubmit = async (values) => {
    if (isNew) {
      const entity = await createEntity(values);
      navigate(`/entity/${entity.id}`);
    } else {
      await updateEntity(values);
      navigate('/entity');
    }
  };

  return (
    <div className={styles.page}>
      <form className={styles.form} onSubmit={handleSubmit(handleFormSubmit)}>
        <Typography>{isNew ? 'Создание' : 'Редактирование'}</Typography>
        <Controller
          name="name"
          control={control}
          rules={{ validate: (v) => Boolean(v?.trim()) }}
          render={({ field: { value = '', onChange } }) => (
            <TextField
              label="Имя"
              value={value}
              onChange={onChange}
              error={Boolean(errors.login)}
            />
          )}
        />
        <Controller
          name="description"
          control={control}
          rules={{ validate: (v) => Boolean(v?.trim()) }}
          render={({ field: { value = '', onChange } }) => (
            <TextField
              label="Описание"
              value={value}
              onChange={onChange}
              error={Boolean(errors.login)}
            />
          )}
        />
        <Controller
          name="userId"
          control={control}
          rules={{ validate: (v) => Boolean(v?.trim()) }}
          render={({ field: { value = '', onChange } }) => (
            <Select
              label="Тип"
              value={value}
              onChange={onChange}
              error={Boolean(errors.login)}
            >
              {users.map((user) => (
                <MenuItem value={user.id} key={user.id}>
                  {user.login}
                </MenuItem>
              ))}
            </Select>
          )}
        />
        <Button variant="contained" type="submit">
          {isNew ? 'Создать' : 'Сохранить'}
        </Button>
      </form>
    </div>
  );
};
