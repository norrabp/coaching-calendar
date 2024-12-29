'use client';

import { useUser } from "@/lib/context/UserContext";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import OpenAppointments from "@/components/app/dashboard/coach/OpenAppointments";
import ScheduledAppointments from "@/components/app/dashboard/coach/CoachScheduledAppointments";
import PastAppointments from "@/components/app/dashboard/coach/PastAppointments";
import AddOpenAppointmentDialog from "@/components/app/dashboard/coach/AddOpenAppointmentDialog";
import { Root } from "postcss";
import WithUserContext from "@/components/app/WithUserContext";

const CoachPage: React.FC = () => {
    const { user } = useUser();
    return (
        <WithUserContext>
            <h1 className="text-xl font-bold py-2">Appointments</h1>
            <div className="py-2">
                <AddOpenAppointmentDialog />
            </div>
            <Tabs defaultValue="scheduled" className="w-full">
                <TabsList>
                    <TabsTrigger value="scheduled">Scheduled</TabsTrigger>
                    <TabsTrigger value="open">Open</TabsTrigger>
                    <TabsTrigger value="past">Past</TabsTrigger>
                </TabsList>
                <TabsContent value="scheduled" className="flex flex-col items-center justify-center">
                    <ScheduledAppointments />
                </TabsContent>
                <TabsContent value="open" className="flex flex-col items-center justify-center">
                    <OpenAppointments />
                </TabsContent>
                <TabsContent value="past" className="flex flex-col items-center justify-center">
                    <PastAppointments />
                </TabsContent>
            </Tabs>
        </WithUserContext>
    );
};

export default CoachPage;