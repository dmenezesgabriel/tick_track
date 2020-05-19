import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';

import api from '../../services/api';

import './styles.css';

export default function Activity() {
  const [activities, setActivities] = useState([]);
  let chartData = [];
  let drillLevel = 1;

  useEffect(() => {
    setTimeout(() => {
      api.get('activities/today')
      .then(response => {
        setActivities(response.data)
      })
    }, 2000);
  });

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

  // Group by property and sum
  function groupBy(originalArray, groupedArray) {
    originalArray.reduce((object, item) => {
    if (!object[item.main_description]) {
      object[item.main_description] = { name: item.main_description, duration: 0 };
      groupedArray.push(object[item.main_description]);
    }
    object[item.main_description].duration += item.duration;
    return object;
   }, {});
  }

  // Sort object by it's properties in descending order
  function sortDescending(array) {
    array.sort((a, b) => parseFloat(b.duration) - parseFloat(a.duration));
  }

  function filterByValue(array, string) {
    return array.filter(obj =>
        Object.keys(obj).some(key => obj[key] === string));
  }

  function CustomTooltip({ label, active }) {
    if (active) {
      let activity = filterByValue(chartData, label);
      let duration = activity[0].duration;
      let time = activity[0].time;

      return (
        <div className="custom-tooltip">
          <p className="label"><strong>Label</strong>: {`${label}`}</p>
          <p className="seconds"><strong>Seconds</strong>: {`${duration}`}</p>
          <p className="time"><strong>Time</strong>: {`${time}`}</p>
        </div>
      );
    }

    return null;
  }

  function onBarClick (data) {
    chartData = filterByValue(activities, data.name);
    drillLevel += 1;
    console.log(data);
    console.log('value: '+ data.name);
  }

  groupBy(activities, chartData);
  sortDescending(chartData);
  convertToTime(chartData);

  return (
      <div className="activity-container">
          <header>
          </header>

          <h1>Activities</h1>

          <div className="container-main-description">
            <BarChart width={1000} height={600} data={chartData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number"/>
              <YAxis width={300} dataKey="name" type="category"/>
              <Tooltip content={<CustomTooltip />}/>
              <Legend />
              <Bar dataKey="duration" fill="#8884d8" onClick={(data) => onBarClick(data)}/>
            </BarChart>
          </div>

      </div>
  );
}