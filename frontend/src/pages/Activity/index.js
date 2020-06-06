import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import Sidebar from '../../components/sidebar';
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
      showing: 'Today',
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
    }, 0);
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
      this.setState(
        {
          showing: 'All',
        });
    } else if(startDate || endDate) {
      this.getActivities('activities/date.range', data)
      this.setState(
        {
          showing: `From ${startDate} to ${endDate}`,
        });
    } else {
      this.getActivities('activities/today', data)
      this.setState(
        {
          showing: 'Today',
        });
    };

    console.log(`end ${this.state.drillLevel}`);
  }

  toggleClass = () => {
    const sidebarCollapse = document.querySelector('#sidebarCollapse');
    const sidebar = document.querySelector('#sidebar');
    const content = document.querySelector('#content');

    sidebar.classList.toggle('active');
    content.classList.toggle('active');
    sidebarCollapse.classList.toggle('active');
  };

  render() {
    console.log(this.state.drillLevel);
    return (
      <div class="container-fluid bg-light">
        <div class="row">
          <Sidebar />
          <div class="col-md-9 col-lg-10 pt-3 px-4" id="content">
            <nav class="navbar">
              <div class="container-fluid">
                  <button type="button" id="sidebarCollapse" onClick={this.toggleClass} class="btn">
                    <span></span>
                    <span></span>
                    <span></span>
                  </button>
                  <form className="form-inline mt-2 mt-md-0" onSubmit={this.onFormSubmit}>
                    <div className="row">
                    <div className="col-20">
                      <input
                      type="text"
                      className="form-control mr-sm-2"
                      value={this.state.search}
                      onChange={event => this.setState({search: event.target.value})}
                      placeholder="Search"
                      />
                    </div>
                    <div className="col-15">
                      <input
                      placeholder="From: Date"
                      className="form-control mr-sm-2"
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
                      className="form-control mr-sm-2"
                      value={this.state.endDate}
                      onChange={event=> this.setState({endDate: event.target.value})}
                      type="text"
                      onFocus={_onFocus}
                      onBlur={_onBlur}
                      />
                    </div>
                    <button type="submit" className="btn bg-info text-white">search</button>
                  </div>
                </form>
              </div>
            </nav>
            <div className="row">

              <div className="col-xl-3 col-md-6 mb-4">
                <div className="card bg-primary border-primary shadow h-100 py-2">
                  <div className="card-body">
                    <div className="row no-gutters align-items-center">
                      <div className="col mr-2">
                        <div className="text-xs font-weight-bold text-white text-uppercase mb-1">Total Duration</div>
                        <hr></hr>
                        <span className="h5 text-white">{this.state.totalDuration}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="col-xl-3 col-md-6 mb-4">
                <div className="card bg-warning border-warning shadow h-100 py-2">
                  <div className="card-body">
                    <div className="row no-gutters align-items-center">
                      <div className="col mr-2">
                        <div className="text-xs font-weight-bold text-white text-uppercase mb-1">Total Idle</div>
                        <hr></hr>
                        <span className="h5 text-white">{this.state.totalIdle}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
            <div className="row">
              <div className="col-md-8 col-lg-7">
                <div className="card shadow mb-4">
                  <div className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                    <div className="text-xs font-weight-bold text-dark text-uppercase mb-1">
                      Ativities
                    </div>
                  </div>
                  <div className="card-body">
                    <form className="form-inline mt-2 mt-md-0">
                      <select className="form-control mr-sm-2" value={this.state.drillLevel} onChange={this.handleChange}>
                        <option value="main_description">Main Description</option>
                        <option value="detailed_description">Detailed Description</option>
                        <option value="more_details">More Details</option>
                      </select>
                    </form>
                    <hr></hr>
                    <span className="ml-1 text-xs mb-1">{this.state.showing}</span>
                    <div className="bar-chart">
                      <ResponsiveContainer width="99%" aspect={1.5}>
                        <BarChart width={1000} height={600} data={this.state.barData} layout="vertical">
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis type="number"/>
                          <YAxis width={200} dataKey="name" type="category"/>
                          <Tooltip />
                          <Legend />
                          <Bar dataKey="duration" fill="#4e73df" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
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