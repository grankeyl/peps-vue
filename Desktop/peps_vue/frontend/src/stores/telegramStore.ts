import { defineStore } from 'pinia'

export const TelegramStorage = defineStore('TelegramStorage', {
  state: () => ({
    UserId: '',
    UserFirstName: '',
    UserLastName: '',
    UserFullName: '',
    UserUsername: '',
    UserPhoto: '',
    UserLanguage: '',
    UserStartParam: '',
    UserIsLanguage: '',
  }),
  actions: {
    // setters
    setUserId(data: any) {
      this.UserId = data
    },
    setUserFirstName(data: any) {
      this.UserFirstName = data
    },
    setUserLastName(data: any) {
      this.UserLastName = data
    },
    setUserFullName(data: any) {
      this.UserFullName = data
    },
    setUserUsername(data: any) {
      this.UserUsername = data
    },
    setUserPhoto(data: any) {
      this.UserPhoto = data
    },
    setUserLanguage(data: any) {
      this.UserLanguage = data
    },
    setUserStartParam(data: any) {
      this.UserStartParam = data
    },
    setUserIsPremium(data: any) {
      this.UserIsLanguage = data
    },

    // getters
    getUserId() {
      return this.UserId
    },
    getUserFirstName() {
      return this.UserFirstName
    },
    getUserLastName() {
      return this.UserLastName
    },
    getUserFullName() {
      return this.UserFullName
    },
    getUserUsername() {
      return this.UserUsername
    },
    getUserPhoto() {
      return this.UserPhoto
    },
    getUserLanguage() {
      return this.UserLanguage
    },
    getUserStartParam() {
      return this.UserStartParam
    },
    getUserIsPremium() {
      return this.UserIsLanguage
    }
  }
})
