function bindAction(value = 0, isUpdate = false) {
    let week = moment()
            .add((value || 0) * 7, 'day')
            .startOf('isoweek');
    this.el.style.opacity = 0;

        this.vm.$http.get('/api/hrops', {headers: {'Authorization': 'Token 64a66708548aa75ef2f1bb842c839adf3404c5e9', 'Content-Type': 'application/json'}})
            .then(({data: hrops}) => {
                let weekUnix = week.unix();
                hrops = hrops
                    .map(hr => ({time: moment(hr.time), period: hr.period, intensity: hr.intensity}))
                    .filter(hr => moment(hr.time).startOf('isoweek').unix() == weekUnix);
                let perDays = [];
                for (let i = 0; i < 7; i++) {
                    let d = hrops.filter(hr => moment(hr.time).startOf('day').unix() == (weekUnix + i * 60 * 60 * 24));
                    perDays.push(this.params.modifyDayHropsCallback(d));
                }
                if (!isUpdate) {
                    renderChart.call(this, perDays, week);
                } else if (this.chart) {
                    this.chart.data.datasets[0].data = perDays;
                    this.chart.update();
                }
                this.el.style.opacity = 1;
            });
}

function renderChart(hropsSizePerDay, week) {
    let labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        .map((l, i) => sprintf('%s, %s', l, moment(week).add(i, 'day').format('MMM Do')));
    this.chart = new Chart(this.el, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Per day',
                data: hropsSizePerDay,
                backgroundColor: hropsSizePerDay.map(v => '#e7e7e7'),
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
    params: ['modifyDayHropsCallback'],
    bind() {
        bindAction.call(this);
    },
    update(value) {
        bindAction.call(this, value, true);
    }
};

