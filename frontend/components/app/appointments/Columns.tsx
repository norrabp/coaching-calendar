"use client"

import { Appointment } from "@/lib/types/appointment"
import { ColumnDef } from "@tanstack/react-table"
import { normalizePhoneNumber } from "@/lib/util/normalize-phone-number"
import ScheduledAppointmentActions from "@/components/app/dashboard/coach/ScheduledAppointmentActions"
import ViewNotesDialog from "@/components/app/dashboard/coach/ViewNotesDialog"

export const OpenColumns: ColumnDef<Appointment>[] = [
    {
      id: "appointment_date",
      header: "Date",
      cell: ({ row }) => {
        const date = new Date(row.original.appointment_time);
        return date.toLocaleDateString();
      }
    },
    {
      id: "appointment_start",
      header: "Start Time",
      cell: ({ row }) => {
        const date = new Date(row.original.appointment_time);
        return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
      }
    },
    {
        id: "appointment_end",
        header: "End Time",
        cell: ({ row }) => {
            const date = new Date(row.original.appointment_time);
            date.setMinutes(date.getMinutes() + 120);
            return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
        }
    },
]

export const CoachScheduledColumns: ColumnDef<Appointment>[] = OpenColumns.concat([
    {
      accessorKey: "student_username",
      header: "Student",
    },
    {
      accessorKey: "student_phone",
      header: "Student Phone",
      cell: ({ row }) => {
        const phone = row.getValue("student_phone");
        return (
            <div className="min-w-[140px]">
              {phone ? normalizePhoneNumber(phone) : ''}
            </div>
        );
      }
    },
    {
        accessorKey: "actions",
        header: "Actions",
        cell: ({ row }) => {
            return <ScheduledAppointmentActions appointment={row.original} />;
        }
    }
  ]);

export const StudentScheduledColumns: ColumnDef<Appointment>[] = OpenColumns.concat([
    {
      accessorKey: "coach_username",
      header: "Coach",
    },
    {
      accessorKey: "coach_phone",
      header: "Coach Phone",
      cell: ({ row }) => {
        const phone = row.getValue("coach_phone");
        return (
            <div className="min-w-[140px]">
              {phone ? normalizePhoneNumber(phone) : ''}
            </div>
        );
      }
    },
  ]);

export const CoachCompletedColumns: ColumnDef<Appointment>[] = OpenColumns.concat([
    {
        accessorKey: "student_username",
        header: "Student",
    },
    {
        accessorKey: "student_phone",
        header: "Student Phone",
        cell: ({ row }) => {
            const phone = row.getValue("student_phone");
            return (
                <div className="min-w-[140px]">
                  {phone ? normalizePhoneNumber(phone) : ''}
                </div>
            );
        }
    },
    {
        accessorKey: "student_satisfaction",
        header: "Student Satisfaction",
    },
    {
        accessorKey: "notes",
        header: "Notes",
        cell: ({ row }) => {
            return <ViewNotesDialog appointment={row.original} />;
        }
    },
]);