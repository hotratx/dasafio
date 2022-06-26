export default function isEmail (email: string): boolean {
  // Regular Expression (Not accepts second @ symbol
  // before the @gmail.com and accepts everything else)
  const regexp = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    
  // Converting the email to lowercase
  return regexp.test(String(email).toLowerCase());
}
