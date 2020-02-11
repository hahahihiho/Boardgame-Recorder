function drawHBarChart(ctx,data) {
    var chart_overall = new Chart(ctx,{
        type: 'horizontalBar',
        data: {
            labels:data.keys,
            datasets: [{
                label: data.label,
                data: data.values,
                backgroundColor : [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ]

            }]
        },
        options: {
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            scales: {
                xAxes: [{
                    time: {
                    unit: 'month'
                    },
                    ticks: {
                        min: 0,
                        stepsize:1,
                        maxTicksLimit: 10
                    },
                    maxBarThickness: 25,
                    gridLines: {
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                }],
                yAxes: [{
                    ticks: {
                        padding: 10
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                }],
            },
        }
    });
}
