'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { useUser } from '@/lib/context/UserContext';
import api from '@/lib/api';

const Navbar = () => {
  const router = useRouter();
  const { user, setUser } = useUser();

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    router.push('/login');
  };

  const handleTestSwitch = async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Set the user in context
      setUser(user);
      
      // Redirect based on role
      switch (user.role) {
        case 'STUDENT':
          router.push('/student');
          break;
        case 'COACH':
          router.push('/coach');
          break;
        case 'ROOT':
          router.push('/');
          break;
        default:
          throw new Error('Invalid user role');
      }
    } catch (err: any) {
      console.error(`Failed to switch: ${err}`);
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
      router.push('/login');
    }
  };

  const handleSwitchToStudent = () => {
    localStorage.removeItem('token');
    setUser(null);
    router.push('/login');
  };

  return (
    <nav className="bg-card border-b border-border">
      <div className="container mx-auto px-4">
        <div className="flex justify-between h-16 items-center">
          <h1
            className="text-lg font-semibold text-foreground"
          >
            {user ? user.username : "Coach App"}
          </h1>
          
          <div>
            {user && user.email === "jjmccarthy@gmail.com" ? (
              <Button className="bg-green-400 hover:bg-green-500 w-[400px]" onClick={() => handleTestSwitch("jimharbaugh@gmail.com", "bad_pass")}>
                Switch to Coach
              </Button>
            ) : user && user.email === "jimharbaugh@gmail.com" ? (
              <Button className="bg-green-400 hover:bg-green-500 w-[400px]" onClick={() => handleTestSwitch("jjmccarthy@gmail.com", "bad_pass")}>
                Switch to Student
              </Button>
            ) : null}
          </div>
          <div>
            {user ? (
              <Button
                onClick={handleLogout}
                className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4"
              >
                Logout
              </Button>
            ) : (
              <Link
                href="/login"
                className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4"
              >
                Login
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;