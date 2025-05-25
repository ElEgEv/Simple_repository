export interface User {
  id: string;
  login: string;
  password: string;
}

export interface AuthState {
  user: User | null;
  setUser: (user: User | null) => void;
}
