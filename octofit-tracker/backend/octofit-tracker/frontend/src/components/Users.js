import React, { useEffect, useState } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespace
    ? `https://${codespace}-8000.app.github.dev/api/users/`
    : 'http://localhost:8000/api/users/';

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setUsers(results);
        console.log('Users endpoint:', endpoint);
        console.log('Fetched users:', results);
      });
  }, [endpoint]);

  return (
    <div>
      <h2>Users</h2>
      <ul className="list-group">
        {users.map((user, idx) => (
          <li key={user.id || idx} className="list-group-item">
            {user.username} - {user.bio}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Users;
