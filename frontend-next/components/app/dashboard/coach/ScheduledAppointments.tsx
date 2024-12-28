'use client';

import { useUser } from '@/lib/context/UserContext';

const ScheduledAppointments: React.FC = () => {

    const { user } = useUser();


    return (
        <div>
            <h2>{user?.username} Scheduled Appointments</h2>
        </div>
    );
};

export default ScheduledAppointments;