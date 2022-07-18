import {createApp} from 'vue';
import App from './App.vue';
import {createStore} from "vuex";

import {state} from "@/vuex/state";
import {mutations} from "@/vuex/mutations";
import {actions} from "@/vuex/actions";

const store = createStore({
   ...state,
   ...mutations,
   ...actions,
});
const app = createApp(App);
app.use(store);
app.mount('#app');
