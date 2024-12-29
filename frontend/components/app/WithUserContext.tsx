'use client';

import { useUser } from "@/lib/context/UserContext";
import LoadingSpinner from "@/components/app/LoadingSpinner";
import Navbar from "@/components/app/Navbar";

export default function WithUserContext({ 
  children 
}: { 
  children: React.ReactNode 
}) {
  const { loading } = useUser();

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-vh-100 bg-dark text-light">
      <main className="container py-4 ml-10 mr-10">
        {children}
      </main>
    </div>
  );
}