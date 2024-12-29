import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useState } from "react";
import api from "@/lib/api";
import { Appointment } from "@/lib/types/appointment";
import { Textarea } from "@/components/ui/textarea";

interface Props {
  appointment: Appointment;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export default function CompleteScheduledAppointmentDialog({ appointment, open, onOpenChange }: Props) {
  const [error, setError] = useState<string>();
  const [satisfaction, setSatisfaction] = useState<number>();
  const [notes, setNotes] = useState<string>("");

  const handleSubmit = async () => {
    if (!satisfaction || !notes) return;

    try {
      await api.post(`/appointments/${appointment.id}`, {
        status: 'COMPLETED',
        student_satisfaction: satisfaction,
        notes: notes,
      });

      // Close dialog and reset form
      onOpenChange(false);
      setSatisfaction(undefined);
      setNotes("");
      setError(undefined);

      // Refresh the page to show updated data
      window.location.reload();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to complete appointment');
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Complete Appointment</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <label className="text-sm font-medium">Student Satisfaction (1-5)</label>
            <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map((value) => (
                <Button
                  key={value}
                  variant={satisfaction === value ? "default" : "outline"}
                  onClick={() => setSatisfaction(value)}
                  className="w-10 h-10 p-0"
                >
                  {value}
                </Button>
              ))}
            </div>
          </div>

          <div className="grid gap-2">
            <label className="text-sm font-medium">Notes</label>
            <Textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Enter appointment notes..."
              className="h-32"
            />
          </div>

          {error && (
            <div className="text-sm text-red-500">
              {error}
            </div>
          )}

          <Button 
            onClick={handleSubmit}
            disabled={!satisfaction || !notes}
          >
            Complete
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}