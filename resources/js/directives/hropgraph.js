function bindAction(value = 0, isUpdate = false) {
    let timeType = this.params.timeType;
    let timeTypeStartOf = timeType == 0 ? 'isoweek' : timeType == 1 ? 'month' : 'isoweek';
    let startTime = moment()
            .add((value || 0) * 7, 'day')
            .startOf(timeTypeStartOf);
    this.el.style.opacity = 0;

        this.vm.$http.get('/api/hrops', {headers: {
                'Authorization': 'Token 64a66708548aa75ef2f1bb842c839adf3404c5e9',
                'Content-Type': 'application/json'}
            })
            .then(({data: hrops}) => {
                let startTimeUnix = startTime.unix();
                hrops = hrops
                    .map(hr => ({time: moment(hr.time), period: hr.period, intensity: hr.intensity}))
                    .filter(hr => moment(hr.time).startOf(timeTypeStartOf).unix() == startTimeUnix);
                let perDays = [];

                for (let i = 0; i < (timeType == 0 ? 7 : timeType == 1 ? startTime.daysInMonth() : 7); i++) {
                    let d = hrops.filter(hr => moment(hr.time).startOf('day').unix() == (startTimeUnix + i * 60 * 60 * 24));
                    perDays.push(this.params.modifyDayHropsCallback(d));
                }
                if (!isUpdate) {
                    renderChart.call(this, perDays, startTime);
                } else if (this.chart) {
                    let labels = [];
                    if (timeType == 0) {
                        labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
                            .map((l, i) => sprintf('%s%s', l, moment(startTime).add(i, 'day').format('MMM Do')));
                    } else if (timeType == 1) {
                        for (let i = 0; i < startTime.daysInMonth(); i++) {
                            labels.push(moment(startTime).add(i, 'day').format('MMM Do'));
                        }
                    }
                    this.chart.data.labels = labels;
                    this.chart.data.datasets[0].data = perDays;
                    this.chart.update();
                }
                this.el.style.opacity = 1;
            });
}

function renderChart(hropsSizePerDay, startTime) {
    let labels = [];
    if (this.params.timeType == 0) {
        labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            .map((l, i) => sprintf('%s%s', l, moment(startTime).add(i, 'day').format('MMM Do')));
    } else if (this.params.timeType == 1) {
        for (let i = 0; i < startTime.daysInMonth(); i++) {
            labels.push(moment(startTime).add(i, 'day').format('MMM Do'));
        }
    }
    this.chart = new Chart(this.el, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Per day',
                data: hropsSizePerDay,
                backgroundColor: hropsSizePerDay.map(v => 'rgba(32, 77, 116, 0.3)'),
                borderColor: hropsSizePerDay.map(v => '#e7e7e7'),
                borderWidth: 1
            }]
        },
        options: {
            animation: {duration: 0},
            scales: {
                yAxes: [{ticks: {beginAtZero: true}}]
            }
        }
    });
}

export default {
    params: ['modifyDayHropsCallback', 'timeType'],
    paramWatchers: {
        timeType() {
            bindAction.call(this, this.value, true);
        }
    },
    bind() {
        bindAction.call(this);
    },
    update(value) {
        this.value = value;
        bindAction.call(this, value, true);
    }
};

