window.$ = window.jQuery = require('jquery');
window._ = require('lodash');
window.moment = require('moment');
window.sprintf = require("sprintf-js").sprintf;
window.Chart = require('chart.js');

import Vue from 'vue';
Vue.use(require('vue-resource'));

import hropgraph from './directives/hropgraph.js';

Vue.directive('hropgraph', hropgraph);

let app = new Vue({
    el: '#antihrop-app',
    data: {
        now: moment(),
        weekShift: 0
    },
    methods: {
        shiftWeek(isNext = true) {
            this.weekShift += isNext ? 1 : -1;
        },
        periodsPerDay(hropsPerDay) {
            return hropsPerDay
                .map(hr => hr.period)
                .reduce((p, c) => p + c, 0);
        },
        intensity(hropsPerDay) {
            return hropsPerDay.length ? Math.max.apply(Math, hropsPerDay.map(hr => hr.intensity)) : 0;
        }
    }
});
