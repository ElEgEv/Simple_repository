import React from 'react';

import styles from './styles.module.css';
import { Button, Typography } from '@mui/material';
import { useAuthStore } from 'entities/user';
import { Link } from 'react-router-dom';

export const Header = () => {
  const { user, setUser } = useAuthStore();

  const handleLogOutButtonClick = () => {
    setUser(null);
  };

  return (
    <header className={styles.header}>
      <nav className={styles.nav}>
        <Typography>Application</Typography>
        <Link to="/entity">
          <Typography>Entities</Typography>
        </Link>
      </nav>
      <div className={styles.auth}>
        <Typography>{user?.login}</Typography>
        <Button
          size="small"
          variant="contained"
          onClick={handleLogOutButtonClick}
        >
          Выйти
        </Button>
      </div>
    </header>
  );
};
