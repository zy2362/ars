var parsedPoints = []
for(point of points) {
    parsedPoints.push([point[2]*1000,parseInt(point[1])]);
}
for(i = 0; i < parsedPoints.length; i++) {
    min_val = parsedPoints[i][0];
    min_index = i;
    for(j = i; j < parsedPoints.length; j++) {
        if(parsedPoints[j][0]<min_val) {
            min_val = parsedPoints[j][0];
            min_index = j;
        }
    }
    temp = parsedPoints[i];
    parsedPoints[i] = parsedPoints[min_index];
    parsedPoints[min_index] = temp;
    parsedPoints[i][0] = Date(parsedPoints[i][0])
}

Highcharts.chart('container', {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Water Consumption'
    },
    subtitle: {
        text: 'by the BEST project'
    },
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: { // don't display the dummy year
            month: '%e. %b',
            year: '%b'
        },
        title: {
            text: 'Date'
        }
    },
    yAxis: {
        title: {
            text: 'Weight (g)'
        },
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br>',
        pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
    },

    plotOptions: {
        series: {
            marker: {
                enabled: true
            }
        }
    },

    colors: ['#6CF'],

    series: [{
        name: "Water",
        data: parsedPoints
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                plotOptions: {
                    series: {
                        marker: {
                            radius: 2.5
                        }
                    }
                }
            }
        }]
    }
});