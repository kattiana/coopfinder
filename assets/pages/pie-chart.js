let data = [107, 31, 635, 203, 2, 10, 4, 55, 53, 134, 341, 20]

let chart = Highcharts.chart('containerMyChart', {
    chart: {
        type: 'bar',
    },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ],
        min: 0,
        max: 11
    },
    series: [{
        data: data
    }, {
        data: data,
        visible: false,
        showInLegend: false
    }]
});

function filterFunction() {

   
    let input = document.getElementById('myPieChart')

    console.log('filter Function....', input.value)

    let points = chart.series[1].points,
        filteredPoint = points.filter(point => point.category == input.value);

    if (filteredPoint.length) {
        let newData = [];
        for (let i in data) {
            newData.push(null)
        }

        newData[filteredPoint[0].index] = filteredPoint[0].y
            newData.push(null) //--- extra null as a workaround for bug
        
        chart.series[0].update({
            data: newData
        })
    } else {
        chart.series[0].update({
            data: data
        })
    }
}