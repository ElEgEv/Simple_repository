import { SignInPage } from 'pages/sign-in-page/sign-in-page';
import React from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import './styles.css';
import { SignUpPage } from 'pages/sign-up-page/sign-up-page';
import { AuthLayout } from './auth-layout/auth-layout';
import { EntityListPage } from 'pages/entity-list-page/entity-list-page';
import { EntityPage } from 'pages/entity-page/entity-page';

export const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AuthLayout />}>
          <Route path="/" element={<Navigate to="/sign-in" replace />} />
          <Route path="/sign-in" element={<SignInPage />} />
          <Route path="/sign-up" element={<SignUpPage />} />
          <Route path="entity" element={<EntityListPage />} />
          <Route path="entity/:id" element={<EntityPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};
