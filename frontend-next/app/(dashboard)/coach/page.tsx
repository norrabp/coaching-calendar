'use client';

import { useUser } from "@/lib/context/UserContext";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import OpenAppointments from "@/components/app/dashboard/coach/OpenAppointments";
import ScheduledAppointments from "@/components/app/dashboard/coach/ScheduledAppointments";

const CoachPage: React.FC = () => {
    const { user } = useUser();
    return (
        <div>
            <h1>Coach Home</h1>
            <p>Welcome, {user?.username}!</p>
            <h2>Appointments</h2>
            <Tabs defaultValue="scheduled" className="w-[400px]">
                <TabsList>
                    <TabsTrigger value="scheduled">Scheduled</TabsTrigger>
                    <TabsTrigger value="open">Open</TabsTrigger>
                </TabsList>
                <TabsContent value="scheduled">
                    <ScheduledAppointments />
                </TabsContent>
                <TabsContent value="open">
                    <OpenAppointments />
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default CoachPage;