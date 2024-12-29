import { Button } from "@/components/ui/button";
import { useEffect, useState, useRef } from "react";
import api from "@/lib/api";
import { useUser } from "@/lib/context/UserContext";
import { toISOFormat } from "@/lib/util/to-iso-format";
import { DatePicker } from "@/components/ui/date-picker";
import { Appointment } from "@/lib/types/appointment";
import { AppointmentSelectionButton } from "./AppointmentSelectionButton";
import { useRouter } from "next/navigation";

export default function ScheduleAppointmentDialog() {
  const [date, setDate] = useState<Date>(new Date());
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment>();
  const [error, setError] = useState<string>();
  const [openAppointments, setOpenAppointments] = useState<Appointment[]>([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const appointmentsContainerRef = useRef<HTMLDivElement>(null);
  const { user } = useUser();
  const router = useRouter();

  const handleSubmit = async () => {
    if (!date || !selectedAppointment || !user) return;

    try {
      await api.post(`/appointments/${selectedAppointment.id}`, {
        student_id: user.id,
        status: "SCHEDULED",
      });

      setDate(new Date());
      setSelectedAppointment(undefined);
      setError(undefined);

      router.push('/student');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to schedule appointment');
    }
  };

  const fetchAppointments = async (selectedDate: Date, currentPage: number) => {
    setIsLoading(true);
    try {
      const response = await api.post('/appointments/open', {
        start_time: toISOFormat(selectedDate),
        pagination_info: {
          page: currentPage,
          page_size: 5,
        },
      });
      
      const newAppointments = response.data.appointments;
      setHasMore(response.data.has_next_page);
      
      if (currentPage === 1) {
        setOpenAppointments(newAppointments);
      } else {
        setOpenAppointments(prev => [...prev, ...newAppointments]);
      }
      setError(undefined);
    } catch (error) {
      setError('Failed to load appointments');
    } finally {
      setIsLoading(false);
    }
  };

  const handleScroll = () => {
    if (!appointmentsContainerRef.current || isLoading || !hasMore) return;

    const container = appointmentsContainerRef.current;
    const { scrollTop, scrollHeight, clientHeight } = container;

    if (scrollHeight - scrollTop <= clientHeight + 50) {
      setPage(prev => prev + 1);
    }
  };

  useEffect(() => {
    setPage(1);
    fetchAppointments(date, 1);
  }, [date]);

  useEffect(() => {
    if (page > 1) {
      fetchAppointments(date, page);
    }
  }, [page]);

  const handleDateChange = async(date: Date | undefined) => {
    if (!date) return;
    setDate(date);
    setSelectedAppointment(undefined);
    setPage(1);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold py-2">Schedule Appointment</h1>
      <div className="grid gap-4 py-4">
        <div className="grid gap-2">    
          <DatePicker date={date} setDate={handleDateChange} />
        </div>

        {date && (
          <div 
            ref={appointmentsContainerRef}
            className="grid grid-cols-1 gap-2 max-h-[400px] overflow-y-auto"
            onScroll={handleScroll}
          >
            {openAppointments.map((appointment) => (
              <AppointmentSelectionButton 
                appointment={appointment} 
                key={appointment.id}
                selected={selectedAppointment?.id === appointment.id} 
                onClick={() => setSelectedAppointment(appointment)}
              />
            ))}
            {isLoading && (
              <div className="text-center py-2">Loading...</div>
            )}
          </div>
        )}

        

      <div className="sticky bottom-0 mt-4 bg-background py-4 border-t">
        {error && (
            <div className="text-sm text-red-500">
              {error}
            </div>
        )}
        <Button 
          onClick={handleSubmit}
          disabled={!date || !selectedAppointment}
          className="w-full"
        >
          Schedule
        </Button>
      </div>
      </div>
    </div>
  );
}