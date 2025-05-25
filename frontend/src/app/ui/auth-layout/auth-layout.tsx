import { useAuthStore } from 'entities/user';
import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { Header } from '../header/header';
import { Footer } from '../footer/footer';
import styles from './styles.module.css';

export const AuthLayout = () => {
  const { pathname } = useLocation();

  const { user } = useAuthStore();

  if (user && (pathname === '/sign-in' || pathname === '/sign-up')) {
    return <Navigate to="/entity" />;
  }

  if (!user && pathname !== '/sign-in' && pathname !== '/sign-up') {
    return <Navigate to="/sign-in" />;
  }

  if (!user) {
    return <Outlet />;
  }

  return (
    <div className={styles.layout}>
      <Header />
      <Outlet />
      <Footer />
    </div>
  );
};
