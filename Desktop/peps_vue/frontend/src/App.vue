<script setup lang="ts">
import { computed, defineComponent, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useTelegramSetup } from '@/composables/useTelegramSetup'
import { useUserSetup } from '@/composables/useUserSetup'
import { LoadingStorage } from '@/stores/loadingStorage'
import { UserStorage } from '@/stores/userStore'

import Header from './components/header.vue'
import Menu from './components/menu.vue'
import Loading from './components/loader.vue'

const useLoadingStorage = LoadingStorage()
const useUserStorage = UserStorage()

// начало загрузки
useLoadingStorage.start()

// получение данных
useTelegramSetup()

// конец загрузки
useLoadingStorage.stop()

setInterval(() => {
  if (useUserStorage.costs.stamina_now < useUserStorage.costs.stamina_costs) {
    useUserStorage.costs.stamina_now++
  }
}, 2000)

const isLoading = computed(() => useLoadingStorage.isLoading)
</script>

<template>
  <Loading v-if="isLoading" />
  <Header v-if="!isLoading" />

  <div class="content" v-if="!isLoading">
    <RouterView />
  </div>

  <Menu v-if="!isLoading" />
</template>
