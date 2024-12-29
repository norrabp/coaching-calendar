export const convertTo24Hour = (time12h: string) => {
    const [time, modifier] = time12h.split(' ');
    let [hours, minutes] = time.split(':');
    
    if (hours === '12') {
      hours = '00';
    }
    
    if (modifier === 'PM') {
      hours = (parseInt(hours, 10) + 12).toString();
    }
    
    return { hours, minutes };
  };

export const convertTo12Hour = (time24h: string) => {
    const [hours, minutes] = time24h.split(':');
    const modifier = parseInt(hours, 10) >= 12 ? 'PM' : 'AM';
    const hour = parseInt(hours, 10) % 12 || 12;
    return `${hour}:${minutes} ${modifier}`;
}