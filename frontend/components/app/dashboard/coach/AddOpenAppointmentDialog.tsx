import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useEffect, useState } from "react";
import { startOfToday } from "date-fns";
import { DatePicker } from "@/components/ui/date-picker";
import api from "@/lib/api";
import { useUser } from "@/lib/context/UserContext";
import { convertTo12Hour, convertTo24Hour } from "@/lib/util/time-to-24-hour";
import { toISOFormat } from "@/lib/util/to-iso-format";


export default function AddOpenAppointmentDialog() {
  const [date, setDate] = useState<Date>(startOfToday());
  const [selectedTime, setSelectedTime] = useState<string>();
  const [open, setOpen] = useState(false);
  const [error, setError] = useState<string>();
  const [timeSlots, setTimeSlots] = useState<string[]>([]);
  const { user } = useUser();


  const handleSubmit = async () => {
    if (!date || !selectedTime || !user) return;

    try {
      // Combine date and time
      const {hours, minutes} = convertTo24Hour(selectedTime);
      const appointmentTime = new Date(date);
      appointmentTime.setHours(parseInt(hours));
      appointmentTime.setMinutes(parseInt(minutes));
      appointmentTime.setSeconds(0);
      appointmentTime.setMilliseconds(0);

      await api.post('/appointments', {
        coach_id: user.id,
        appointment_time: toISOFormat(appointmentTime),
      });

      // Close dialog and reset form
      setOpen(false);
      setDate(startOfToday());
      setSelectedTime(undefined);
      setError(undefined);

      // TODO: Refresh appointments list
      window.location.reload();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create appointment');
    }
  };

  const resetTime = async(date: Date) => {
    setTimeSlots([]);
    setSelectedTime(undefined);
    const response = await api.post('/appointments/available-slots', {
      start_time: toISOFormat(date),
    });
    setTimeSlots(response.data.slots.map(convertTo12Hour));
  };

  useEffect(() => {
    resetTime(date);
  }, [date]);

  const handleDateChange = async(date: Date | undefined) => {
    if (!date) return;
    setDate(date);
    resetTime(date);
  };

  

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline"
            className="p-4 inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4"
        >
            Add Open Appointment Slot
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add Open Appointment Slot</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <DatePicker date={date} setDate={handleDateChange} />
          </div>

          {date && (
            <div className="grid grid-cols-4 gap-2">
              {timeSlots.map((time) => (
                <Button
                  key={time}
                  variant={selectedTime === time ? "default" : "outline"}
                  onClick={() => setSelectedTime(time)}
                >
                  {time}
                </Button>
              ))}
            </div>
          )}

          {error && (
            <div className="text-sm text-red-500">
              {error}
            </div>
          )}

          <Button 
            onClick={handleSubmit}
            disabled={!date || !selectedTime}
          >
            Create
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}