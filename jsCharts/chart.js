const colors = Highcharts.getOptions().colors;

// Create the chart
Highcharts.chart('container', {
    chart: {
        type: 'arearange',
        zooming: {
            type: 'x'
        }
    },
    title: {
        text: 'Tesla Stock '
    },
    subtitle: {
        text: 'Forecast, Summer 2024</a>'
    },
    xAxis: {
        type: 'category',
        accessibility: {
            rangeDescription: 'Range: 2024-05-15 to 2024-05-28.'
        },
        min: 1,
        max: 8,
        endOnTick: false,
        plotBands: [{
            color: 'rgba(255, 75, 66, 0.07)',
            from: 180,
            to: 205,
            label: {
                text: 'Forecast'
            }
        }],
        plotLines: [{
            dashStyle: 'dash',
            color: colors[1],
            width: 2,
            value: 5.5
        }]
    },
    yAxis: {
        opposite: true,
        title: {
            text: 'Price'
        },
        labels: {
            format: '{value}'
        },
        max: 190,
        min: 170
    },
    tooltip: {
        crosshairs: true,
        shared: true,
        valueSuffix: '$',
    },
    responsive: {
        rules: [{
            chartOptions: {
                xAxis: {
                    labels: {
                        staggerLines: 2
                    }
                }
            },
            condition: {
                minWidth: 540
            }
        }]
    },
    plotOptions: {
        series: {
            marker: {
                enabled: false
            }
        },
        arearange: {
            enableMouseTracking: false,
            states: {
                inactive: {
                    enabled: false
                }
            },
            color: colors[1],
            fillOpacity: 1 / 3,
            lineWidth: 0
        }
    },
    legend: {
        enabled: false
    },
    series: [{
        name: 'Tsla price',
        type: 'line',
        data: [
            ['2024-05-13', 171.89],
            ['2024-05-14', 174.55],
            ['2024-05-15', 173.99],
            ['2024-05-16', 174.84],
            ['2024-05-17', 177.46],
            ['2024-05-20', 174.95],
            ['2024-05-21', 186.60],
            ['2024-05-22', 180.11],
            ['2024-05-23', 173.74],
            ['2024-05-24', 179.24],
            ['2024-05-28', 176.75]
        ],
        zIndex: 2,
        color: colors[2],
        lineWidth: 4
    },{
        name: 'Tsla predict price',
        type: 'line',
        data: [
            ['2024-05-20', 174.95],
            ['2024-05-21', 177.04],
            ['2024-05-22', 176.87],
            ['2024-05-23', 176.02],
            ['2024-05-24', 177.32],
            ['2024-05-28', 177]
        ],
        zIndex: 2,
        color: colors[1],
        lineWidth: 4
    },
     {
        name: '1σ',
        data: [
            ['2024-05-20', 174.95, 174.95],
            ['2024-05-21', 175.395, 178.685 ],
            ['2024-05-22', 175.225, 178.515],
            ['2024-05-23', 174.375, 177.665],
            ['2024-05-24', 175.675, 178.965],
            ['2024-05-28', 175.655, 176.645],
        ]
    }, {
        name: '2σ',
        data: [
            ['2024-05-20', 174.95, 174.95],
            ['2024-05-21', 177.04 - 1.96, 177.04 + 1.96],
            ['2024-05-22', 176.87 - 1.96, 176.87 + 1.96],
            ['2024-05-23', 176.02 - 1.96, 176.02 + 1.96],
            ['2024-05-24', 177.32 - 1.96, 177.32 + 1.96],
            ['2024-05-28', 177 - 1.96, 177 + 1.96]
        ]
    }, {
        name: '3σ',
        data: [
            ['2024-05-20', 174.95, 174.95],
            ['2024-05-21', 177.04 - 2.576, 177.04 + 2.576],
            ['2024-05-22', 176.87 - 2.576, 176.87 + 2.576],
            ['2024-05-23', 176.02 - 2.576, 176.02 + 2.576],
            ['2024-05-24', 177.32 - 2.576, 177.32 + 2.576],
            ['2024-05-28', 177 - 2.576, 177 + 2.576]
        ]
    }]
});
