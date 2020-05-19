import React from 'react';
import api from '../../services/api';

// import './styles.css';


// Seconds to time
function secTotime(timeInSeconds) {
  var pad = function(num, size) { return ('000' + num).slice(size * -1); },
  time = parseFloat(timeInSeconds).toFixed(3),
  hours = Math.floor(time / 60 / 60),
  minutes = Math.floor(time / 60) % 60,
  seconds = Math.floor(time - minutes * 60),
  milliseconds = time.slice(-3);

  return pad(hours, 2) + ':' + pad(minutes, 2) + ':' + pad(seconds, 2) + ',' + pad(milliseconds, 3);
}

  function convertToTime(object) {
    object.forEach(item => {
    item.time = secTotime(item.duration);
    })
  }

// Sort object by it's properties in descending order
function sortDescending(array) {
  array.sort((a, b) => parseFloat(b.duration) - parseFloat(a.duration));
}

// Group by property and sum
function groupBy(originalArray, descLevel) {
  const result =[];
  originalArray.reduce((object, item) => {
  if (!object[item[descLevel]]) {
    object[item[descLevel]] = { name: item[descLevel], duration: 0 };
    result.push(object[item[descLevel]]);
  }

  object[item[descLevel]].duration += item.duration;
  return object;
  }, {});

  // Aditional formatting
  return result;
}

class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      activities: [],
      barData: [],
    };
}

  getActivities() {
    const self = this
    setTimeout(() => {
      api.get('activities/today')
      .then((response) => {

        // Prepare data
        const groupedData = groupBy(response.data, 'main_description');
        sortDescending(groupedData);
        convertToTime(groupedData);

        // Set state
        self.setState({activites: groupedData});
      })
    }, 2000);
  }

  render() {
    this.getActivities();
    console.table(this.state.activites);
    return (
      <div>{this.state.activities}</div>
    )
  }
}

export default Dashboard;