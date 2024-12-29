import { Button } from "@/components/ui/button";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { MoreHorizontal } from "lucide-react";
import { Appointment } from "@/lib/types/appointment";
import CompleteScheduledAppointmentDialog from "./CompleteScheduledAppointmentDialog";
import { useState } from "react";

const ScheduledAppointmentActions: React.FC<{appointment: Appointment}> = ({appointment}) => {
    const [showCompleteDialog, setShowCompleteDialog] = useState(false);
    
    return (
        <>
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="h-8 w-8 p-0">
                        <span className="sr-only">Open menu</span>
                        <MoreHorizontal className="h-4 w-4" />
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Actions</DropdownMenuLabel>
                    <DropdownMenuItem onSelect={() => setShowCompleteDialog(true)}>
                        Complete Appointment
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>

            <CompleteScheduledAppointmentDialog 
                appointment={appointment}
                open={showCompleteDialog}
                onOpenChange={setShowCompleteDialog}
            />
        </>
    );
};

export default ScheduledAppointmentActions;