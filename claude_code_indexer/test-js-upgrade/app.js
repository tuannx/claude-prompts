// Test JavaScript file
import React from 'react';
import { useState } from 'react';

export default function App() {
  const [count, setCount] = useState(0);
  
  const increment = () => setCount(count + 1);
  
  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={increment}>Increment</button>
    </div>
  );
}

class UserService {
  constructor() {
    this.users = [];
  }
  
  addUser(user) {
    this.users.push(user);
  }
}

export { UserService };
EOF < /dev/null