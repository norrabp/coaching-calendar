import { Button } from "@/components/ui/button";
import { Appointment } from "@/lib/types/appointment";

interface AppointmentSelectionButtonProps {
    appointment: Appointment;
    selected: boolean;
    onClick: () => void;
}

export const AppointmentSelectionButton: React.FC<AppointmentSelectionButtonProps> = ({appointment, selected, onClick}) => {
    const datetime = new Date(appointment.appointment_time);

    const day = datetime.toLocaleDateString()
    const startTime = datetime.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
    const endDatetime = new Date(datetime)
    endDatetime.setMinutes(endDatetime.getMinutes() + 120)
    const endTime = endDatetime.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
    const coach = appointment.coach_username;
    
    return (
        <Button 
            variant={selected ? "default" : "outline"} 
            onClick={onClick}
            className="w-full h-full p-4" // Added full width and padding
        >
            <div className="flex flex-col items-start w-full h-full"> {/* Added items-start and w-full */}
                <h3 className="font-semibold text-left">{coach}</h3>
                <p className="text-sm text-left">{day}</p>
                <p className="text-sm text-left">{startTime} to {endTime}</p>
            </div>
        </Button>
    );
};