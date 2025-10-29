import React, { useEffect, useState } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespace
    ? `https://${codespace}-8000.app.github.dev/api/leaderboard/`
    : 'http://localhost:8000/api/leaderboard/';

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setLeaderboard(results);
        console.log('Leaderboard endpoint:', endpoint);
        console.log('Fetched leaderboard:', results);
      });
  }, [endpoint]);

  return (
    <div>
      <h2 className="mb-4">Leaderboard</h2>
      <div className="card mb-3">
        <div className="card-body">
          <h5 className="card-title">Ranking de usuarios</h5>
          <p className="card-text">Total: {leaderboard.length}</p>
          <button className="btn btn-info">Actualizar ranking</button>
        </div>
      </div>
      <table className="table table-striped table-bordered">
        <thead className="table-dark">
          <tr>
            <th>#</th>
            <th>Usuario</th>
            <th>Puntaje</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry, idx) => (
            <tr key={entry.id || idx}>
              <td>{idx + 1}</td>
              <td>{entry.username || entry.name}</td>
              <td>{entry.score || entry.total_distance || 0}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Leaderboard;
