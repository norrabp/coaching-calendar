'use client';

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import api from '@/lib/api';
import { useUser } from '@/lib/context/UserContext';
import React from "react";

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const { setUser } = useUser();
  const form = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  async function onSubmit(values: z.infer<typeof loginSchema>) {
    if (isLoading) return;
    
    setError('');
    setIsLoading(true);
    
    try {
      const response = await api.post('/auth/login', values);
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
      const errorMessage = err.response?.data?.error || err.message || 'Login failed';
      setError(errorMessage);
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
    } finally {
      setIsLoading(false);
    }
  }

  const loginWithTestUser = async (email: string, password: string) => {
    onSubmit({ email, password });
  }



  return (
    <div className="mx-auto max-w-sm space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold">Login</h1>
        <p className="text-gray-500 dark:text-gray-400">
          Enter your credentials to access your account
        </p>
      </div>
      
      {error && (
        <div className="p-3 text-sm text-red-500 bg-red-100 dark:bg-red-900/30 rounded-md">
          {error}
        </div>
      )}

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input placeholder="email@example.com" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <Input type="password" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Login'}
          </Button>
        </form>
      </Form>

      <div className="border border-green-200 bg-green-100 rounded-md p-4">
        <h2 className="text-lg font-bold text-center">Test Users</h2>
        <div className="grid grid-cols-2 gap-2">
          <Button className="w-full bg-green-400 hover:bg-green-500" onClick={() => loginWithTestUser("jimharbaugh@gmail.com", "bad_pass")}>Login as Coach (Test)</Button>
          <Button className="w-full bg-green-400 hover:bg-green-500" onClick={() => loginWithTestUser("jjmccarthy@gmail.com", "bad_pass")}>Login as Student (Test)</Button>
        </div>
      </div>
      
      <div className="text-center text-sm">
        Don't have an account?{' '}
        <Link 
          href="/register" 
          className="text-primary hover:underline"
        >
          Register here
        </Link>
      </div>
    </div>
  );
}