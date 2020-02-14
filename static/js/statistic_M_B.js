
var which_year;
var checkbox = document.getElementsByName('checkbox')

function chooseYear(e){
    let temp_year = e.target.attributes.value.value;
    if(which_year == temp_year){}
    else{
        which_year = temp_year;
        //체크 해제
        checkbox.forEach((_) => {
            _.checked = false;
        })
        chart.data.datasets = [];
        chart.update();
    }
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

function data_to_chart_dataset(data){
    let dataset = {
        type:'line',
        label: data.label,
        fill : false,         // 채우기 없음
        lineTension : 0.2,  // 0이면 꺾은선 그래프, 숫자가 높을수록 둥글해짐
        pointRadius : 0,    // 각 지점에 포인트 주지 않음
        borderColor: gencolor(),
        data: data.value
    };
    return dataset;
}

function gencolor(){
    let r = Math.floor(Math.random()*255);
    let g = Math.floor(Math.random()*255);
    let b = Math.floor(Math.random()*255);
    return 'rgba('+r+','+g+','+b+','+0.4+')';
}