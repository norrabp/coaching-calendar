import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || '',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Cache-Control': 'no-cache'
  }
});

// Create a promise that will be resolved when the user context is ready
let userContextReadyPromise: Promise<void>;
let resolveUserContextReady: (() => void) | undefined;

userContextReadyPromise = new Promise((resolve) => {
  resolveUserContextReady = resolve;
});

// List of routes that don't need to wait for user context
const publicRoutes = [
  '/auth/login',
  '/auth/register',
  '/auth/me'
];

// Add request interceptor
api.interceptors.request.use(async (config) => {
  // Skip waiting for context for public routes
  if (config.url && publicRoutes.some(route => config.url?.includes(route))) {
    return config;
  }
  
  // Wait for user context to be ready before proceeding with the request
  await userContextReadyPromise;
  return config;
});

export const setUserContextReady = () => {
  if (resolveUserContextReady) {
    resolveUserContextReady();
  }
};

export default api;