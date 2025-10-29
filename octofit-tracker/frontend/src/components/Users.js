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
      <h2 className="mb-4">Users</h2>
      <div className="card mb-3">
        <div className="card-body">
          <h5 className="card-title">Listado de usuarios</h5>
          <p className="card-text">Total: {users.length}</p>
          <button className="btn btn-success">Agregar usuario</button>
        </div>
      </div>
      <table className="table table-striped table-bordered">
        <thead className="table-dark">
          <tr>
            <th>#</th>
            <th>Usuario</th>
            <th>Bio</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user, idx) => (
            <tr key={user.id || idx}>
              <td>{idx + 1}</td>
              <td>{user.username}</td>
              <td>{user.bio}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Users;
