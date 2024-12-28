'use client';

import { useUser } from '@/lib/context/UserContext';

const OpenAppointments: React.FC = () => {

    const { user } = useUser();


    return (
        <div>
            <h2>{user?.username} Open Appointments</h2>
        </div>
    );
};

export default OpenAppointments;