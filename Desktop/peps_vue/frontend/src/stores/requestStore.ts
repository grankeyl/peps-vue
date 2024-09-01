import { defineStore } from 'pinia'

export const RequestStorage = defineStore('RequestStorage', {
  state: () => ({
    response: {}
  }),
  actions: {
    setResponse(response: Object) {
      this.response = response
    },
    getResponse() {
      return this.response
    }
  }
})
