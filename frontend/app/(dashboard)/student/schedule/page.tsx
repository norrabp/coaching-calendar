'use client';

import ScheduleAppointmentForm from "@/components/app/dashboard/student/ScheduleAppointmentForm";
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb";
import WithUserContext from "@/components/app/WithUserContext";

const SchedulePage: React.FC = () => {
    return (
        <WithUserContext>
            <Breadcrumb>
                <BreadcrumbList>
                <BreadcrumbSeparator />
                    <BreadcrumbItem>
                        <BreadcrumbLink href="/student">Home</BreadcrumbLink>
                    </BreadcrumbItem>
                    <BreadcrumbSeparator />
                    <BreadcrumbItem>
                        <BreadcrumbPage>Schedule</BreadcrumbPage>
                    </BreadcrumbItem>
                </BreadcrumbList>
            </Breadcrumb>
            <ScheduleAppointmentForm />
        </WithUserContext>
    );
};

export default SchedulePage;