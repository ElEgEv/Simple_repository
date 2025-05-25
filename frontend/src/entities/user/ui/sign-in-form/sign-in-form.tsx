import { Button, Paper, TextField, Typography } from '@mui/material';
import React from 'react';

import styles from './styles.module.css';
import { Controller, useForm } from 'react-hook-form';
import { getUser } from 'entities/user/api';
import { Link } from 'react-router-dom';
import { useAuthStore } from 'entities/user/store';

export const SignInForm = () => {
  const { setUser } = useAuthStore();

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const handleFormSubmit = async (values) => {
    const user = await getUser(values);
    setUser(user);
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <Paper className={styles.form}>
        <Typography>Вход</Typography>
        <Controller
          name="login"
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
          name="password"
          control={control}
          rules={{ validate: (v) => Boolean(v?.trim()) }}
          render={({ field: { value = '', onChange } }) => (
            <TextField
              label="Пароль"
              value={value}
              onChange={onChange}
              error={Boolean(errors.password)}
            />
          )}
        />
        <Button variant="contained" type="submit">
          Войти
        </Button>
        <Link to="/sign-up">
          <Button type="submit">Создать аккаунт</Button>
        </Link>
      </Paper>
    </form>
  );
};
