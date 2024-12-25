export interface User {
    id: number;
    username: string;
    email: string;
    phone_number: string;
    role: UserRole;
  }

export type UserRole = "STUDENT" | "COACH" | "ROOT";