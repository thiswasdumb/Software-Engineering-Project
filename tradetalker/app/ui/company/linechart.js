'use client';
import { useEffect } from 'react';
import { Chart, Title } from 'chart.js/auto';
import dayjs from 'dayjs';

function LineChart(stockLastDays) {
  Chart.register(Title);
  useEffect(() => {
    console.log(stockLastDays);
    var ctx = document.getElementById('myChart').getContext('2d');
    /* eslint-disable @typescript-eslint/no-unused-vars */
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [
          dayjs().subtract(7, 'day').format('DD/MM'),
          dayjs().subtract(6, 'day').format('DD/MM'),
          dayjs().subtract(5, 'day').format('DD/MM'),
          dayjs().subtract(4, 'day').format('DD/MM'),
          dayjs().subtract(3, 'day').format('DD/MM'),
          dayjs().subtract(2, 'day').format('DD/MM'),
          dayjs().subtract(1, 'day').format('DD/MM'),
          'Today',
        ],
        datasets: [
          {
            data: stockLastDays.stockLastDays,
            label: 'Stock price',
            borderColor: '#3e95cd',
            backgroundColor: '#7bb6dd',
            fill: false,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        options: {
          plugins: {
            title: {
              display: true,
              text: 'Last 7 days',
            },
          },
        },
      },
    });
  }, [stockLastDays]);
  /* eslint-enable @typescript-eslint/no-unused-vars */
  return (
    <>
      <div className='flex flex-col justify-items-center'>
        <h1 className='mx-auto mt-1 text-base font-bold'>Last 7 days</h1>
        <div className='relative m-auto flex h-[40vh] w-full grow-0 rounded-lg border border-slate-400 drop-shadow-lg lg:w-full'>
          <canvas id='myChart' />
        </div>
      </div>
    </>
  );
}

export default LineChart;
