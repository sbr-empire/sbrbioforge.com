import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { auth } from '../config/firebase';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from 'firebase/auth';

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      token: null,
      loading: false,
      error: null,

      login: async (email, password) => {
        set({ loading: true, error: null });
        try {
          const result = await signInWithEmailAndPassword(auth, email, password);
          const token = await result.user.getIdToken();
          localStorage.setItem('auth_token', token);
          set({ user: result.user, token, loading: false });
          return { success: true };
        } catch (error) {
          set({ error: error.message, loading: false });
          return { success: false, error: error.message };
        }
      },

      register: async (email, password, profile) => {
        set({ loading: true, error: null });
        try {
          const result = await createUserWithEmailAndPassword(auth, email, password);
          const token = await result.user.getIdToken();
          localStorage.setItem('auth_token', token);
          set({ user: result.user, token, loading: false });
          return { success: true };
        } catch (error) {
          set({ error: error.message, loading: false });
          return { success: false, error: error.message };
        }
      },

      logout: async () => {
        await signOut(auth);
        localStorage.removeItem('auth_token');
        set({ user: null, token: null });
      },

      setUser: (user) => set({ user }),
      setToken: (token) => set({ token })
    }),
    {
      name: 'auth-store-bioforge',
      partialize: (state) => ({ user: state.user, token: state.token })
    }
  )
);
