'use client';

import { AppointmentTable } from '@/components/app/appointments/AppointmentTable';
import { OpenColumns } from '@/components/app/appointments/Columns';
import { Appointment} from '@/lib/types/appointment';
import { useState, useEffect } from 'react';
import api from '@/lib/api';
const OpenAppointments: React.FC = () => {

    const [appointments, setAppointments] = useState<Appointment[]>([]);

    useEffect(() => {
        const fetchAppointments = async () => {
            const response = await api.post('/appointments/my', { query_opts: { filter: { status: 'OPEN' } }, as_student: false });
            setAppointments(response.data.appointments);
        };
        fetchAppointments();
    }, []);

    return (
        <AppointmentTable columns={OpenColumns} data={appointments} />
    );
};

export default OpenAppointments;