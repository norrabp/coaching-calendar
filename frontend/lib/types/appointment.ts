export interface Appointment {
    id: string;
    coach_id: string;
    coach_username: string;
    coach_phone: string;
    student_id: string;
    student_username: string;
    student_phone: string;
    appointment_time: string;
    status: AppointmentStatus;
    notes: string;
    student_satisfaction: 1 | 2 | 3 | 4 | 5 | null;
}

export type AppointmentStatus = 'OPEN' | 'SCHEDULED' | 'COMPLETED' | 'CANCELLED';