import { defineStore } from 'pinia'

export const SkinsStorage = defineStore('SkinsStorage', {
  state: () => ({
    storageSkins: {}
  }),
  actions: {
    setStorageSkins(data: Object) {
      this.storageSkins = data
    },
    getStorageSkins() {
      return this.storageSkins
    }
  }
})
