import { create } from 'zustand';
import { AuthState } from './types';
import { persist } from 'zustand/middleware';

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => {
      return {
        user: null,
        setUser: (user) => set({ user }),
      };
    },
    { name: 'user' },
  ),
);
