'use client';

import { useUser } from "@/lib/context/UserContext";
import StudentScheduledAppointments from "@/components/app/dashboard/student/StudentScheduledAppointments";
import Link from "next/link";
import WithUserContext from "@/components/app/WithUserContext";

const StudentPage: React.FC = () => {
    const { user } = useUser();
    return (
        <WithUserContext>
            <h1 className="text-xl font-bold py-2">Appointments</h1>
            <div className="py-2">
                <Link 
                    href="/student/schedule" 
                className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4"
            >
                Schedule Appointment
                </Link>
            </div>
            <StudentScheduledAppointments />
        </WithUserContext>
    );
};

export default StudentPage;