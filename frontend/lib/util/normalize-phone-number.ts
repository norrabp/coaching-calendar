export function normalizePhoneNumber(phoneNumber: string): string {
    // Remove all non-digit characters
    const digits = phoneNumber.replace(/\D/g, '');
    
    // Check if we have a valid number of digits (10)
    if (digits.length !== 10) {
        throw new Error('Phone number must contain exactly 10 digits');
    }
    
    // Format into (xxx) xxx-xxxx
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
}