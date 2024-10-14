import { defineStore } from 'pinia'

export const LocalizationStorage = defineStore('LocalizationStorage', {
  state: () => ({
    localization: {}
  }),
  actions: {
    setLocalization(data: Object) {
      this.localization = data
    },
    getLocalization() {
      return this.localization
    }
  }
})
