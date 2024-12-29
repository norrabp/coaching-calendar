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

const registerSchema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  phone_number: z.string()
    .transform((val) => val.replace(/\D/g, '')) // Strip non-digits
    .refine(
        (val) => val.length === 10,
        "Phone number must have exactly 10 digits"
    )
});

export default function RegisterPage() {
  const router = useRouter();
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<z.infer<typeof registerSchema>>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
      phone_number: ""
    },
  });

  async function onSubmit(values: z.infer<typeof registerSchema>) {
    if (isLoading) return;
    
    setError('');
    setIsLoading(true);
    
    try {
      await api.post('/auth/register', values);
      router.push('/login');
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || err.message || 'Registration failed';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-sm space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold">Create an Account</h1>
        <p className="text-gray-500 dark:text-gray-400">
          Enter your information to create an account
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
            name="username"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Username</FormLabel>
                <FormControl>
                  <Input placeholder="johndoe" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input placeholder="email@example.com" type="email" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="phone_number"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Phone Number</FormLabel>
                <FormControl>
                  <Input placeholder="(123) 456-7890" type="tel" {...field} />
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
            {isLoading ? 'Creating Account...' : 'Register'}
          </Button>
        </form>
      </Form>

      <div className="text-center text-sm">
        Already have an account?{' '}
        <Link 
          href="/login" 
          className="text-primary hover:underline"
        >
          Login here
        </Link>
      </div>
    </div>
  );
}