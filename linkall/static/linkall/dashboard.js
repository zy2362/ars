var parsedPoints = {
    x:[],
    y:[],
}
for(point of points) {
    parsedPoints.x.push(Date(point[2]*1000));
    parsedPoints.y.push(parseInt(point[1]));
}
console.log(parsedPoints);

var parsedPairsDots = [];
for(i in parsedPoints.x) {
    parsedPairsDots.push([parsedPoints.x[i],parsedPoints.y[i]]);
}

Highcharts.chart('container', {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Snow depth at Vikjafjellet, Norway'
    },
    subtitle: {
        text: 'Irregular time data in Highcharts JS'
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
        min: 0
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
        data: parsedPairsDots
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