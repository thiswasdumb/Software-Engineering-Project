'use client';
import { useEffect } from 'react';
import { Chart, Title } from 'chart.js/auto';
import dayjs from 'dayjs';

/**
 * Creates a line chart of the last 7 days of stock price
 * @param stockLastDays - The last 7 days of stock prices
 * @returns A line chart of the last 7 days of stock prices
 */
function LineChart(stockLastDays) {
  Chart.register(Title);
  useEffect(() => {
    console.log(stockLastDays);
    var ctx = document.getElementById('myChart').getContext('2d');
    /* eslint-disable @typescript-eslint/no-unused-vars */
    var labels = [];
    // Calculate the dates of the last 7 days, excluding weekends
    for (var i = 9; i >= 0; i--) {
      var date = dayjs().subtract(i, 'day');
      if (
        date.subtract(8, 'hour').day() !== 0 &&
        date.subtract(8, 'hour').day() !== 6
      ) {
        labels.push(date.subtract(8, 'hour').format('DD/MM'));
      }
    }
    var data = stockLastDays.stockLastDays;
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            data: data,
            label: 'Share price',
            borderColor: '#3e95cd',
            backgroundColor: '#7bb6dd',
            fill: false,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Last 7 days',
          },
        },
      },
    });
  }, [stockLastDays]);
  /* eslint-enable @typescript-eslint/no-unused-vars */
  return (
    <>
      <div className='mt-2 flex flex-col justify-items-center'>
        <div className='relative m-auto flex h-[40vh] w-full grow-0 rounded-lg border border-slate-400 drop-shadow-lg lg:w-full'>
          <canvas id='myChart' />
        </div>
      </div>
    </>
  );
}

export default LineChart;
