import { useUser } from "@/context/UserContext";
import api from "@/services/api";
import { useEffect, useState } from "react";
import { Appointment } from "@/core/appointments/types/appointment";
import AppointmentTable from "@/core/appointments/components/AppointmentTable";

const CoachHome: React.FC = () => {
    const { user } = useUser();
    const [isLoading, setIsLoading] = useState(true);
    const [appointments, setAppointments] = useState<Appointment[]>([]);

    useEffect(() => {
        const fetchData = async () => {
          const token = localStorage.getItem('token');
          if (!token) {
            return;
          }
          
          try {
            const appointmentsResponse = await api.get('/appointments/me', { data: { filter: { status: 'SCHEDULED' }, query_opts: { pagination: { page_size: 50 } } } });
            setAppointments(appointmentsResponse.data.appointments);
            setIsLoading(false);
          } catch (error) {
            console.error('Error fetching data:', error);
            setIsLoading(false);
          }
        };
        fetchData();
      }, [setIsLoading, setAppointments]);
    return (
        <div>
            <h1>Coach Home</h1>
            <p>Welcome, {user?.username}!</p>
            <h2>Upcoming Appointments</h2>
            <AppointmentTable />
        </div>
    );
};

export default CoachHome;