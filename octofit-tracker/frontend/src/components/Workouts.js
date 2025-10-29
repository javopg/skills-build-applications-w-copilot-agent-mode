import React, { useEffect, useState } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespace
    ? `https://${codespace}-8000.app.github.dev/api/workouts/`
    : 'http://localhost:8000/api/workouts/';

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setWorkouts(results);
        console.log('Workouts endpoint:', endpoint);
        console.log('Fetched workouts:', results);
      });
  }, [endpoint]);

  return (
    <div>
      <h2 className="mb-4">Workouts</h2>
      <div className="card mb-3">
        <div className="card-body">
          <h5 className="card-title">Listado de entrenamientos</h5>
          <p className="card-text">Total: {workouts.length}</p>
          <button className="btn btn-warning">Agregar entrenamiento</button>
        </div>
      </div>
      <table className="table table-striped table-bordered">
        <thead className="table-dark">
          <tr>
            <th>#</th>
            <th>Usuario</th>
            <th>Tipo</th>
            <th>Duración</th>
          </tr>
        </thead>
        <tbody>
          {workouts.map((workout, idx) => (
            <tr key={workout.id || idx}>
              <td>{idx + 1}</td>
              <td>{workout.username}</td>
              <td>{workout.type}</td>
              <td>{workout.duration}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Workouts;
