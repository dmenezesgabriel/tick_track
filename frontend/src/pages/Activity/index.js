import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import api from '../../services/api';
import './styles.css';


function _onFocus(event) {
    event.currentTarget.type = "date";
}

function _onBlur(event) {
    event.currentTarget.type = "text";
}

class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      totalDuration: [],
      totalIdle: [],
      barData: [],
      drillLevel: 'main_description',
      search: '',
      startDate: '',
      endDate: '',
    };

    this.onFormSubmit = this.onFormSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.getActivities('activities/today', {});
}

  getActivities(url, data) {
    setTimeout(() => {
      api.post(url, data)
      .then((response) => {
        console.log(response)

        // Prepare data
        const totalDuration = response.data['total_duration']
        const totalIdle = response.data['total_idle']
        const tableData = response.data['table_data']

        // Set state
        this.setState(
          {
            totalDuration: totalDuration,
            totalIdle: totalIdle,
            barData: tableData
          });
      })
    }, 2000);
  }

  handleChange(event) {
    this.setState({ drillLevel: event.target.value }, () => {this.onFormSubmit(event)});
  }

  onFormSubmit(event) {
    event.preventDefault();
    const text = this.state.search;
    const startDate = this.state.startDate;
    const endDate = this.state.endDate;
    const drillLevel = this.state.drillLevel

    console.log(`submit ${this.state.drillLevel}`);
    const data = {
      text: text,
      start_date: startDate,
      end_date: endDate,
      drill_level: drillLevel,
    }

    if(text) {
      this.getActivities('activities/search', data)
    } else if(startDate || endDate) {
      this.getActivities('activities/date.range', data)
    } else {
      this.getActivities('activities/today', data)
    };

    console.log(`end ${this.state.drillLevel}`);
  }

  render() {
    console.log(this.state.drillLevel);
    return (
      <div className="container-fluid">
          <div className="topnav">
              <div className="left-align application-name">
                <a href="#home">Tick Track</a>
              </div>
              <div className="rigth-align">
                <a href="#about">About</a>
              </div>
          </div>

          <div className="sidebar">
            <a className="active" href="#home"><i className="fas fa-chart-line"></i> Dashboard</a>
            <a href="#news"><i className="fal fa-clock"></i> Pomodoro Timer</a>
            <a href="#contact"><i className="fal fa-border-all"></i> Board</a>
            <a href="#about"><i className="far fa-bookmark"></i> Bookmark</a>
          </div>

        <div className="main-content">
            <div className="search-bar">
              <form className="search" onSubmit={this.onFormSubmit}>
                <div className="row">
                  <div className="col-20">
                    <input
                      type="text"
                      className="search-input"
                      value={this.state.search}
                      onChange={event => this.setState({search: event.target.value})}
                      placeholder="Search"
                    />
                  </div>
                  <div className="col-15">
                    <input
                      placeholder="From: Date"
                      className="first-date"
                      value={this.state.startDate}
                      onChange={event => this.setState({startDate: event.target.value})}
                      type="text"
                      onFocus={_onFocus}
                      onBlur={_onBlur}
                    />
                  </div>
                  <div className="col-15">
                    <input
                      placeholder="To: Date"
                      className="last-date"
                      value={this.state.endDate}
                      onChange={event=> this.setState({endDate: event.target.value})}
                      type="text"
                      onFocus={_onFocus}
                      onBlur={_onBlur}
                    />
                  </div>
                  <button type="submit" className="btn-search">search</button>
                </div>
              </form>
            </div>

            <div className="row">
              <div className="col-33 total-duration">
                <div className="kpi total-duration">
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
              <div className="col-33 total-idle">
                <div className="kpi total-idle">
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
                <div className="col-25 level-filter">
                <span className="title">Time Spent on Activity</span>
                  <form>
                    <select className="description-level" value={this.state.drillLevel} onChange={this.handleChange}>
                      <option value="main_description">Main Description</option>
                      <option value="detailed_description">Detailed Description</option>
                      <option value="more_details">More Details</option>
                    </select>
                  </form>
                </div>
                  <div className="chart-wrapper">
                    <div className="bar-chart">
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

        </div>
      </div>
    )
  }
}

export default Dashboard;