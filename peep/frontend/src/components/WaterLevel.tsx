import { useEffect } from 'react';
import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const summarizeData = (data: WaterLevel[]) => {
    let output : HourSummary[] = [];
    data.sort((a, b) => a.timestamp - b.timestamp)
    let currentHour = new Date(data[0].timestamp*1000);
    currentHour.setHours(currentHour.getHours() + 1)

    let currentHourSummary : HourSummary = {
        sensor0: 0,
        sensor0count: 0,
        sensor1: 0,
        sensor1count: 0,
        sensor2: 0,
        sensor2count: 0,
        sensor3: 0,
        sensor3count: 0,
        timestamp: currentHour
    }
    
    data.forEach(record => {
        if (new Date(record.timestamp*1000) < currentHourSummary.timestamp)
        {
            switch (record.sensor) {
                case 0:
                    currentHourSummary.sensor0count += 1;
                    currentHourSummary.sensor0 += record.voltage;
                break;
                case 1:
                    currentHourSummary.sensor1count += 1;
                    currentHourSummary.sensor1 += record.voltage;
                break;
                case 2:
                    currentHourSummary.sensor2count += 1;
                    currentHourSummary.sensor2 += record.voltage;
                break;
                case 3:
                    currentHourSummary.sensor3count += 1;
                    currentHourSummary.sensor3 += record.voltage;
                break;
            }
        }
        else {
            currentHourSummary.sensor0 = currentHourSummary.sensor0 / currentHourSummary.sensor0count;
            currentHourSummary.sensor1 = currentHourSummary.sensor1 / currentHourSummary.sensor1count;
            currentHourSummary.sensor2 = currentHourSummary.sensor2 / currentHourSummary.sensor2count;
            currentHourSummary.sensor3 = currentHourSummary.sensor3 / currentHourSummary.sensor3count;

            output.push(currentHourSummary);

            currentHour = new Date(currentHour.setHours(currentHour.getHours() + 1));
            
            currentHourSummary = {
                sensor0: 0,
                sensor0count: 0,
                sensor1: 0,
                sensor1count: 0,
                sensor2: 0,
                sensor2count: 0,
                sensor3: 0,
                sensor3count: 0,
                timestamp: currentHour
            }
        }
    });

    return output;
}

type WaterLevel = {
    sensor: number;
    voltage: number;
    timestamp: number;
}

type HourSummary = {
    sensor0: number;
    sensor0count: number;
    sensor1: number;
    sensor1count: number;
    sensor2: number;
    sensor2count: number;
    sensor3: number;
    sensor3count: number;
    timestamp: Date;
}

const WaterLevelChart = () => {
    const [data, setData] = useState<HourSummary[]>();
    useEffect(() => {
        fetch('api/water/week').then(async (response) => {
            if (response.status === 400) {
              return null;
            }
            const resp = await response.json();
            return resp;
          })
          .then((data:WaterLevel[]) => {
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
          <XAxis dataKey="timestamp"/>
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="sensor0" stroke="#0FD65B"  />
          <Line type="monotone" dataKey="sensor1" stroke="#A90FD6"  />
          <Line type="monotone" dataKey="sensor2" stroke="#D60F2A"  />
          <Line type="monotone" dataKey="sensor3" stroke="#E27B1F"  />
        </LineChart>
    );
}

export default WaterLevelChart;
