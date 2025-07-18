// Test TypeScript file with potential edge cases
export interface User {
  id: number;
  name: string;
  email?: string;
}

export class UserService {
  private users: User[] = [];
  
  constructor() {
    console.log('UserService initialized');
  }
  
  addUser(user: User): void {
    this.users.push(user);
  }
  
  getUser(id: number): User | undefined {
    return this.users.find(u => u.id === id);
  }
}

// Test with null/undefined
const testNull = null;
const testUndefined = undefined;

// Test with empty strings
const emptyString = '';
const whitespaceString = '   ';

// Test function with no name
export default function() {
  return 'anonymous';
}

// Arrow function with no name
export const arrow = () => {
  return 'arrow';
};