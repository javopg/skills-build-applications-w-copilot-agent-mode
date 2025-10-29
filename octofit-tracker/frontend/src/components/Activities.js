import React, { useEffect, useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespace
    ? `https://${codespace}-8000.app.github.dev/api/activities/`
    : 'http://localhost:8000/api/activities/';

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Activities endpoint:', endpoint);
        console.log('Fetched activities:', results);
      });
  }, [endpoint]);

  return (
    <div>
      <h2 className="mb-4">Activities</h2>
      <button className="btn btn-primary mb-3" data-bs-toggle="modal" data-bs-target="#activityModal">Agregar actividad</button>
      <div className="card mb-3">
        <div className="card-body">
          <h5 className="card-title">Resumen de actividades</h5>
          <p className="card-text">Total: {activities.length}</p>
        </div>
      </div>
      <table className="table table-striped table-bordered">
        <thead className="table-dark">
          <tr>
            <th>#</th>
            <th>Usuario</th>
            <th>Tipo</th>
            <th>Distancia (km)</th>
            <th>Duración</th>
          </tr>
        </thead>
        <tbody>
          {activities.map((activity, idx) => (
            <tr key={activity.id || idx}>
              <td>{idx + 1}</td>
              <td>{activity.username}</td>
              <td>{activity.type}</td>
              <td>{activity.distance}</td>
              <td>{activity.duration}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {/* Modal ejemplo */}
      <div className="modal fade" id="activityModal" tabIndex="-1" aria-labelledby="activityModalLabel" aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="activityModalLabel">Agregar actividad</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              <form>
                <div className="mb-3">
                  <label className="form-label">Usuario</label>
                  <input type="text" className="form-control" />
                </div>
                <div className="mb-3">
                  <label className="form-label">Tipo</label>
                  <input type="text" className="form-control" />
                </div>
                <div className="mb-3">
                  <label className="form-label">Distancia (km)</label>
                  <input type="number" className="form-control" />
                </div>
                <div className="mb-3">
                  <label className="form-label">Duración</label>
                  <input type="text" className="form-control" />
                </div>
                <button type="submit" className="btn btn-success">Guardar</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Activities;
