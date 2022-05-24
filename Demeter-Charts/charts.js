const ctx = document.getElementById('predictChart').getContext('2d');

// const footer = (tooltipItems) => {
//     let sum = 0;

//     tooltipItems.forEach(function (tooltipItem) {
//         sum += tooltipItem.parsed.y;
//     });
//     return 'Sum: ' + sum;
// };

const footer = function (tooltipItems) {
    tooltipItems.parsed.y
    return 'Temperature: ' + sum + '\n';
};

const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1', '2', '3', '4', '5', '6'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            // backgroundColor: [
            // 'rgba(255, 99, 132, 0.2)'
            //     'rgba(54, 162, 235, 0.2)',
            //     'rgba(255, 206, 86, 0.2)',
            //     'rgba(75, 192, 192, 0.2)',
            //     'rgba(153, 102, 255, 0.2)',
            //     'rgba(255, 159, 64, 0.2)'
            // ],
            borderColor: [
                //     'rgba(255, 99, 132, 1)',
                //     'rgba(54, 162, 235, 1)',
                //     'rgba(255, 206, 86, 1)',
                //     'rgba(75, 192, 192, 1)',
                //     'rgba(153, 102, 255, 1)',
                'rgba(25, 25, 25, 1)'
            ]
            // borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        interaction: {
            intersect: false,
            mode: 'index',
        },
        plugins: {
            tooltip: {
                callbacks: {
                    footer: footer,
                }
            }
        }
    }
});