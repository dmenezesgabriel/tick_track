import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';
import api from '../../services/api';

import './styles.css';

class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      totalDuration: [],
      totalIdle: [],
      barData: [],
    };
}

  getActivities() {
    const self = this
    setTimeout(() => {
      api.post('activities/today')
      .then((response) => {

        // Prepare data
        const totalDuration = response.data['total_duration']
        const totalIdle = response.data['total_idle']
        const tableData = response.data['table_data']

        // Set state
        self.setState(
          {
            totalDuration: totalDuration,
            totalIdle: totalIdle,
            barData: tableData
          });
      })
    }, 2000);
  }

  render() {
    this.getActivities();
    return (

      <div className="activity-container">

          <h1>Activities</h1>
          <div className="search-bar">
            <form className="search">
              <input type="text"/>
              <input type="date"/>
            </form>
          </div>

          <div className="row">
            <div className="col-lg-3 col-sm-6">
              <div className="card">
                <div className="card-heading">
                  <div>
                    Total Duration
                  </div>
                </div>
                <div className="card-value">
                  <span>{this.state.totalDuration}</span>

                </div>
              </div>
            </div>
            <div className="col-lg-4 col-sm-6">
              <div className="card">
                <div className="card-heading">
                  <div>
                    Total Idle
                  </div>
                </div>
                <div className="card-value">
                  <span>{this.state.totalIdle}</span>

                </div>
              </div>
            </div>
          </div>

          <div className="container-main-description">
            <BarChart width={1000} height={600} data={this.state.barData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number"/>
              <YAxis width={300} dataKey="name" type="category"/>
              <Tooltip />
              <Legend />
              <Bar dataKey="duration" fill="#8884d8" />
            </BarChart>
          </div>

      </div>
    )
  }
}

export default Dashboard;