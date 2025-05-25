import { SignUpForm } from 'entities/user';
import React from 'react';

import styles from './styles.module.css';

export const SignUpPage = () => {
  return (
    <div className={styles.page}>
      <SignUpForm />
    </div>
  );
};
