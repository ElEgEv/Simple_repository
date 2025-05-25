import { SignInForm } from 'entities/user';
import React from 'react';

import styles from './styles.module.css';

export const SignInPage = () => {
  return (
    <div className={styles.page}>
      <SignInForm />
    </div>
  );
};
