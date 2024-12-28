'use client';

import { useUser } from "@/lib/context/UserContext";

const StudentPage: React.FC = () => {
    const { user } = useUser();
    return (
        <div>
            <h1>Student Home</h1>
            <p>Welcome, {user?.username}!</p>
        </div>
    );
};

export default StudentPage;