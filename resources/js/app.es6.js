window.$ = window.jQuery = require('jquery');
window._ = require('lodash');
window.moment = require('moment');
window.sprintf = require("sprintf-js").sprintf;
window.Chart = require('chart.js');

import Vue from 'vue';
Vue.use(require('vue-resource'));

let token = localStorage.getItem('token');
if (token) {
    Vue.http.headers.common['Authorization'] = sprintf('Token %s', token);
}

import hropgraph from './directives/hropgraph.js';

Vue.directive('hropgraph', hropgraph);

let app = new Vue({
    el: '#antihrop-app',
    data: {
        now: moment(),
        timeShift: 0,
        timeType: 0,
        user: {login: '', password: ''}
    },
    methods: {
        login() {
            this.$http.post('/api/token-auth/', {username: this.user.login, password: this.user.password}, {headers: {'Content-Type': 'application/json'}})
                .then(({data: {token}}) => {
                    localStorage.setItem('token', token);
                    window.location = '/';
                })
        },
        setTimeType(type) {
            this.timeType = type;
        },
        shiftTime(isNext = true) {
            this.timeShift += isNext ? 1 : -1;
        },
        periodsPerDay(hropsPerDay) {
            return hropsPerDay
                .map(hr => hr.period)
                .reduce((p, c) => p + c, 0);
        },
        maxIntensity(hropsPerDay) {
            return hropsPerDay.length ? Math.max.apply(Math, hropsPerDay.map(hr => hr.intensity)) : 0;
        },
        avgIntensity(hropsPerDay) {
            return hropsPerDay.length
                ? (hropsPerDay.map(ht => ht.intensity).reduce((i, carry) => (carry + i), 0) / hropsPerDay.length)
                : 0;
        },
        counts(hropsPerDay) {
            return hropsPerDay.length
        }
    }
});
