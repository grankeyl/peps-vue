import { defineStore } from 'pinia'

export const LoadingStorage = defineStore('LoadingStorage', {
  state: () => ({
    isLoading: true
  }),
  actions: {
    start() {
      this.isLoading = true
    },
    stop() {
      setTimeout(() => {
        this.isLoading = false
      }, 200)
    },
    checkLoading() {
      return this.isLoading // Directly return the isLoading state
    }
  }
})
