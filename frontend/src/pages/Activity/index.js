import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
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
      <div className="container-fluid">
          <div class="topnav">
            <a href="#about">About</a>
          </div>

          <div class="sidebar">
            <a class="active" href="#home"><i class="fas fa-chart-line"></i> Dashboard</a>
            <a href="#news"><i class="fal fa-clock"></i> Pomodoro Timer</a>
            <a href="#contact"><i class="fal fa-border-all"></i> Board</a>
            <a href="#about"><i class="far fa-bookmark"></i> Bookmark</a>
          </div>

        <div className="main-content">
            <div className="search-bar">
              <form className="search">
                <div className="row">
                  <div className="col-20">
                    <input type="text" className="search-input"/>
                  </div>
                  <div className="col-15">
                    <input type="date" className="first-date"/>
                  </div>
                  <div className="col-15">
                    <input type="date" className="last-date"/>
                  </div>
                  <button type="submit" className="btn-search">search</button>
                </div>
              </form>
            </div>

            <div className="row">
              <div className="col-33">
                <div className="kpi">
                  <div className="kpi-heading">
                    <div>
                      Total Duration
                    </div>
                  </div>
                  <div className="kpi-value">
                    <span>{this.state.totalDuration}</span>

                  </div>
                </div>
              </div>
              <div className="col-33">
                <div className="kpi">
                  <div className="kpi-heading">
                    <div>
                      Total Idle
                    </div>
                  </div>
                  <div className="kpi-value">
                    <span>{this.state.totalIdle}</span>

                  </div>
                </div>
              </div>
            </div>

            <div className="row">
              <div className="col-100">
                <span className="title">Time Spent on Activity</span>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart width={1000} height={600} data={this.state.barData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number"/>
                    <YAxis width={300} dataKey="name" type="category"/>
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="duration" fill="rgb(113, 89, 193)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

        </div>
      </div>
    )
  }
}

export default Dashboard;