// initPieChart, initLineMonthChart 

function initPieChart(ctx) {
    var chart = new Chart(ctx,{
        type: 'pie',
        data: {
            labels:'',
            datasets: [{
                label: [],
                data: [],
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
            maintainAspectRatio: false
        }
    });
    return chart;
}

function initLineMonthChart(ctx){
    let chart = new Chart(ctx, {
        type: 'line',
        // The data for our dataset
        data: {
            // labels: ['January', 'February', 'March', 'April','May','June','July','August','September','October','November','December'],
            labels: ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
            datasets: []
        },
        options:{
            maintainAspectRatio: false,
            responsive: true,
            scales: {
				yAxes: [{
					ticks: {
                        min: 0,
                        stepSize: 1,
                        maxTicksLimit: 10
					}
				}]
            },
            legend: {
                display: true,
                position: 'top'
            }
        }
    });
    return chart;
}