import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Appointment } from "@/lib/types/appointment";
import { Notebook } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { useState } from "react";

interface Props {
  appointment: Appointment;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export default function ViewNotesDialog({ appointment}: Props) {
    const [open, setOpen] = useState(false);

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <TooltipProvider>
                <Tooltip>
                    <TooltipTrigger asChild>
                    <DialogTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                        <Notebook className="h-4 w-4" />
                        <span className="sr-only">View Notes</span>
                        </Button>
                    </DialogTrigger>
                    </TooltipTrigger>
                    <TooltipContent>
                    <p>View Notes</p>
                    </TooltipContent>
                </Tooltip>
            </TooltipProvider>
            
        <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
            <DialogTitle>Appointment Notes</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
            <div className="grid gap-2">
                <div className="text-sm">
                <div className="mb-2 font-bold">Student Satisfaction</div>
                <div className="mb-4">{appointment.student_satisfaction} / 5</div>
                <div className="font-bold">Notes</div>
                <div className="whitespace-pre-wrap">{appointment.notes}</div>
                </div>
            </div>

            <Button onClick={() => onOpenChange(false)}>
                Close
            </Button>
            </div>
        </DialogContent>
        </Dialog>
    );
}