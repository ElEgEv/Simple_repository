import { Button, Paper, TextField, Typography } from '@mui/material';
import React from 'react';

import styles from './styles.module.css';
import { Controller, useForm } from 'react-hook-form';
import { createUser } from 'entities/user/api';
import { Link, useNavigate } from 'react-router-dom';

export const SignUpForm = () => {
  const navigate = useNavigate();

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const handleFormSubmit = async (values) => {
    const user = await createUser(values);
    if (user) {
      navigate('/sign-in');
    }
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <Paper className={styles.form}>
        <Typography>Создать учетную запись</Typography>
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
          Создать
        </Button>
        <Link to="/sign-in">
          <Button type="submit">Войти</Button>
        </Link>
      </Paper>
    </form>
  );
};
