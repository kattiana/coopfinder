'use strict';
    $(document).ready(function() {
dashboard();

    /*Counter Js Starts*/
    $('.counter').counterUp({
        delay: 10,
        time: 400
    });
    /*Counter Js Ends*/

//  Resource bar
    $(".resource-barchart").sparkline([5, 6, 2, 4, 9, 1, 2, 8, 3, 6, 4,2,1,5], {
        type: 'bar',
        barWidth: '15px',
        height: '80px',
        barColor: '#fff',
        tooltipClassname:'abc'
    });

        function setHeight() {
            var $window = $(window);
            var windowHeight = $(window).height();
            if ($window.width() >= 320) {
                $('.user-list').parent().parent().css('min-height', windowHeight);
                $('.chat-window-inner-content').css('max-height', windowHeight);
                $('.user-list').parent().parent().css('right', -300);
            }
        };
        setHeight();

        $(window).on('load',function() {
            setHeight();
        });
    });

    $(window).resize(function() {
        dashboard();
        //  Resource bar
        $(".resource-barchart").sparkline([5, 6, 2, 4, 9, 1, 2, 8, 3, 6, 4,2,1,5], {
                type: 'bar',
                barWidth: '15px',
                height: '80px',
                barColor: '#fff',
                tooltipClassname:'abc'
            });
    });

    function dashboard(){
    };

    
    Highcharts.getJSON('./../../model/dataChart.json',function (dataset) {
        Highcharts.chart('barchart', {

        chart: {
            zoomType: 'xy'//,
            //height: 300
        },
        title: {
            text: '' // baseado nas estratégias
        },
        xAxis: {
            categories: dataset[0],
            max: 2,
            scrollbar: {
                enabled: true
            }
        },
        yAxis: {
            min: 0,
            max: 15, // atualizar o valor baseando-se em uma média
            scrollbar: {
                enabled: true
            }
        },
        labels: {
            items: [{
                html: 'Total activities in files',
                style: {
                    left: '130px',
                    top: '8px',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
                }
            }]
        },
        credits: {
            enabled: false
        },
        series: [{
            type: 'column',
            name: [dataset[1][0]],
            data: dataset[2],
            color:'#ff884d'
        }, {
            type: 'column',
            name: [dataset[1][1]],
            data: dataset[3],
            color:'#66b3ff'
        }, //{
        //    type: 'column',
        //    name: 'Joe',
        //    data: [3, 4, 2, 9, 5],
        //    color:'#39444e'
        //}, {
        {
            type: 'spline',
            name: 'Average',
            data: dataset[4],
            marker: {
                lineWidth: 2,
                lineColor: Highcharts.getOptions().colors[2],
                fillColor: 'white'
            }
        }, {
            type: 'pie',
            name: 'Total consumption',
            data: [{
                name: [dataset[1][0]],
                y: 13,                  //atualizar esse valores
                color: '#ff884d'
            }, {
                name: [dataset[1][1]],
                y: 23,                  //atualizar esse valores
                color:'#66b3ff'
            }//, {
            //    name: 'Joe',
            //    y: 19,
            //   color:'#39444e'
            //}
            ],
            center: [40, 20],
            size: 100,
            showInLegend: false,
            dataLabels: {
                enabled: false
            }
        }]
        })
    })




    Highcharts.getJSON('./../../model/dataChart.json',function (dataset) {

        let fork_rec_developer = window.localStorage.getItem('fork_rec_developer')
        
        Highcharts.chart('piechart', {
            chart: {
                type: 'pie',
                options3d: {
                    enabled: true,
                    alpha: 45,
                    beta: 0
                }
                //  backgroundColor:'#fff'
            },
            title: {
                text: 'Expertise of ' + fork_rec_developer
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            credits: {
                enabled: false
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    depth: 35,
                    dataLabels: {
                        enabled: true,
                        format: '{point.name}'
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'Browser share',
                data: [
                    {
                        name: 'Firefox',
                        y: 40.0,
                        sliced: true,
                        selected: true,
                        color:'#2BBBAD'
                    },
                    {
                        name: 'IE',
                        y: 26.8,
                        color:'#39444e'
                    },
                    {
                        name: 'Chrome',
                        y: 12.8,
                        color:'#2196F3'
                    },
                    {
                        name: 'Safari',
                        y: 8.5,
                        color:'#3F729B'
                    },
                    {
                        name: 'Opera',
                        y: 6.2,
                        color:'#f57c00'
                    },
                    {
                        name: 'Others',
                        y: 5.7,
                        color:'#aa66cc'
                    }
                ]
            }]
            
        });
    });
        
    //updatePieChart(fork_rec_developer){

    //        console.log("updatePieChart------ " , recDevName) 
        
            // pieChart = document.querySelector("#piechart");    
        
    //        pieChart.chart.title.update( 'novo titulo' + recDevName);
        
    //};


    Highcharts.chart('container', {

        title: {
            text: 'Highcharts Sankey Diagram'
        },
        accessibility: {
            point: {
                valueDescriptionFormat: '{index}. {point.from} to {point.to}, {point.weight}.'
            }
        },
        series: [{
            keys: ['from', 'to', 'weight'],
            data: [
                ['Brazil', 'Portugal', 5],
                ['Brazil', 'France', 1],
                ['Brazil', 'Spain', 1],
                ['Brazil', 'England', 1],
                ['Canada', 'Portugal', 1],
                ['Canada', 'France', 5],
                ['Canada', 'England', 1],
                ['Mexico', 'Portugal', 1],
                ['Mexico', 'France', 1],
                ['Mexico', 'Spain', 5],
                ['Mexico', 'England', 1],
                ['USA', 'Portugal', 1],
                ['USA', 'France', 1],
                ['USA', 'Spain', 1],
                ['USA', 'England', 5],
                ['Portugal', 'Angola', 2],
                ['Portugal', 'Senegal', 1],
                ['Portugal', 'Morocco', 1],
                ['Portugal', 'South Africa', 3],
                ['France', 'Angola', 1],
                ['France', 'Senegal', 3],
                ['France', 'Mali', 3],
                ['France', 'Morocco', 3],
                ['France', 'South Africa', 1],
                ['Spain', 'Senegal', 1],
                ['Spain', 'Morocco', 3],
                ['Spain', 'South Africa', 1],
                ['England', 'Angola', 1],
                ['England', 'Senegal', 1],
                ['England', 'Morocco', 2],
                ['England', 'South Africa', 7],
                ['South Africa', 'China', 5],
                ['South Africa', 'India', 1],
                ['South Africa', 'Japan', 3],
                ['Angola', 'China', 5],
                ['Angola', 'India', 1],
                ['Angola', 'Japan', 3],
                ['Senegal', 'China', 5],
                ['Senegal', 'India', 1],
                ['Senegal', 'Japan', 3],
                ['Mali', 'China', 5],
                ['Mali', 'India', 1],
                ['Mali', 'Japan', 3],
                ['Morocco', 'China', 5],
                ['Morocco', 'India', 1],
                ['Morocco', 'Japan', 3]
            ],
            type: 'sankey',
            name: 'Sankey demo series'
        }]

        });
