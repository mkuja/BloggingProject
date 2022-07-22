import {mapState} from "vuex";

const state = {
   data() {
      return {
         appSettings: {
            registeredCanComment: null,
            anonymousCanComment: null,
            usersCanRegister: null,
            verifyEmail: null,
            showSocialMediaShares: null,
            dateAndTimeFormat: null,
         }
      }
   },
   computed: mapState({
      registeredCanComment: state => state.appSettings.registeredCanComment,
      anonymousCanComment: state => state.appSettings.anonymousCanComment,
      usersCanRegister: state => state.appSettings.usersCanRegister,
      verifyEmail: state => state.appSettings.verifyEmail,
      showSocialMediaShares: state => state.appSettings.showSocialMediaShares,
      dateAndTimeFormat: state => state.appSettings.dateFormat,
   }),
   mutations: {
      toggleRegisteredCanComment(state) {
         state.appSettings.registeredCanComment = !state.appSettings.registeredCanComment;
      },
      toggleAnonymousCanComment(state) {
         state.appSettings.anonymousCanComment = !state.appSettings.anonymousCanComment;
      },
      toggleUsersCanRegister(state) {
         state.appSettings.usersCanRegister = !state.appSettings.usersCanRegister;
      },
      toggleVerifyEmail(state) {
         state.appSettings.verifyEmail = !state.appSettings.verifyEmail;
      },
      toggleShowSocialMediaShares(state) {
         state.appSettings.showSocialMediaShares = !state.appSettings.showSocialMediaShares;
      },
      setDateFormat(state, format) {
         state.appSettings.dateFormat = format;
      },
      setTimeFormat(state, format) {
         state.appSettings.timeFormat = format;
      }
   }
}

export {state};
