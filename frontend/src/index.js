import { createApp, h } from 'vue'
import { createInertiaApp, InertiaLink } from '@inertiajs/inertia-vue3'
import { InertiaProgress } from '@inertiajs/progress/src'
import axios from "axios";
import '../../static/css/app.postcss'

let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
axios.defaults.csrfmiddlewaretoken = csrftoken;

import Pages from "./Pages/pages.js";

const pages = {
  ...Pages
};

let customRoute = (...args) => {
  let route =  window.reverseUrl(...args);
  return route;
}

InertiaProgress.init();

createInertiaApp({
  page: JSON.parse(document.getElementById("page").textContent),
  resolve: name => import(`./Pages/${pages[name]}`),
  setup({ el, app, props, plugin }) {
    const appVue = createApp({ render: () => h(app, props) })
      .use(plugin)
      .mixin({ methods: { route: customRoute }})
      .component('inertia-link', InertiaLink)

    // Translation Settings
    appVue.config.globalProperties.$_ = window.gettext ? window.gettext : value => value;
    appVue.config.globalProperties.$i_ = window.interpolate ? window.interpolate : value => value;
    appVue.config.globalProperties.$setlang = window.setlang ? window.setlang : value => value;

    appVue.mount(el);
  },
})
