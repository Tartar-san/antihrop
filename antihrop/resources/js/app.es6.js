window._ = require('lodash');
window.moment = require('moment');
window.sprintf = require("sprintf-js").sprintf;

import Vue from 'vue';
Vue.use(require('vue-resource'));

let app = new Vue({
    el: '#antihrop-app',
    data: {}
});