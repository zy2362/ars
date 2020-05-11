var parsedPoints = []
for(point of points) {
    parsedPoints.push([point[0]*1000,parseInt(point[1])]);
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
    //parsedPoints[i][0] = timestampToDate(parsedPoints[i][0])
}
console.log(parsedPoints);

function timestampToDate(timestamp) {
    date = new Date(timestamp);
    y = date.getFullYear();
    m = date.getMonth();
    d = date.getDay();
    h = date.getHours();
    return Date.UTC(y,m,d,h-4);
}

options= {
    chart: {
        type: 'spline',
        backgroundColor: 'transparent',
    },
    title: {text: ''},
    subtitle: {text: ''},
    credits: {text: ''},
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: { // don't display the dummy year
            month: '%e. %b',
            year: '%b'
        },
    },
    yAxis: {title: {text: ''}},
    tooltip: {
        pointFormat: '{point.y:.0f}g'
    },

    plotOptions: {series: {marker: {enabled: true}}},

    colors: ['#6CF'],

    series: [
        {name: "Water",data: parsedPoints},
    ],

    legend: {enabled: false},

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
};

Highcharts.chart('container',options);
Highcharts.chart('container2',options);