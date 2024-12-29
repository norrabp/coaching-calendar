export const toTitleCase = (str: string) => {
    return str.toLowerCase().replace(/\b\w/g, letter => letter.toUpperCase());
};

