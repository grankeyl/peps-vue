import { defineStore } from 'pinia'

export const UserStorage = defineStore('UserStorage', {
  state: () => ({
    user: {},
    settings: {},
    costs: {}
  }),
  actions: {
    setUser(data: Object) {
      this.user = data
    },
    setSettings(data: Object) {
      this.settings = data
    },
    setCosts(data: Object) {
      this.costs = data
    },
    getUser() {
      return this.user
    },
    getSettings() {
      return this.settings
    },
    getCosts() {
      return this.costs
    }
  }
})
