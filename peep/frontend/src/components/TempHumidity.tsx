import { useEffect } from 'react';
import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const summarizeData = (data: TempHumid[]) => {
    let output : HourSummary[] = [];
    data.sort((a, b) => a.timestamp - b.timestamp)
    let currentHour = new Date(data[0].timestamp*1000);
    currentHour.setHours(currentHour.getHours() + 1)

    let currentHourSummary : HourSummary = {
        temp: 0,
        tempcount: 0,
        humidity: 0,
        humiditycount: 0,
        timestamp: currentHour
    }
    
    data.forEach(record => {
        if (new Date(record.timestamp*1000) < currentHourSummary.timestamp)
        {
            currentHourSummary.tempcount += 1;
            currentHourSummary.temp += record.temp;

            currentHourSummary.humiditycount += 1;
            currentHourSummary.humidity += record.humidity;
        }
        else {
            currentHourSummary.temp = currentHourSummary.temp / currentHourSummary.tempcount;
            currentHourSummary.humidity = currentHourSummary.humidity / currentHourSummary.humiditycount;

            output.push(currentHourSummary);

            currentHour = new Date(currentHour.setHours(currentHour.getHours() + 1));
            
            currentHourSummary = {
                temp: 0,
                tempcount: 0,
                humidity: 0,
                humiditycount: 0,
                timestamp: currentHour
            }
        }
    });

    console.log(output);
    return output;
}

type TempHumid = {
    humidity: number;
    temp: number;
    timestamp: number;
}

type HourSummary = {
    temp: number;
    tempcount: number;
    humidity: number;
    humiditycount: number;
    timestamp: Date;
}

const TempHumidityChart = () => {
    const [data, setData] = useState<HourSummary[]>();
    useEffect(() => {
        fetch('/api/temphumid/all').then(async (response) => {
            if (response.status === 400) {
              return null;
            }
            const resp = await response.json();
            return resp;
          })
          .then((data:TempHumid[]) => {
            if (data != null) {
              setData(summarizeData(data));         }
          });
    }, [])
    return (
        <LineChart
          width={800}
          height={400}
          data={data}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="temp" stroke="#FF5733" activeDot={{ r: 8 }} />
          <Line type="monotone" dataKey="humidity" stroke="#3386FF" activeDot={{ r: 8 }} />
        </LineChart>
    );
}

export default TempHumidityChart;
