export const toISOFormat = (date: Date) => {
    // TODO: Remove when allowing locales outside UTC
    const pad = (num: number) => String(num).padStart(2, '0');
    
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}.${String(date.getMilliseconds()).padStart(3, '0')}`;
};