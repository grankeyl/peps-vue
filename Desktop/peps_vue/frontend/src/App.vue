<script setup lang="ts">
import { computed } from 'vue'
import { useTelegramSetup, settingsTelegram } from '@/composables/useTelegramSetup'
import { LoadingStorage } from '@/stores/loadingStorage'
import { UserStorage } from '@/stores/userStore'
import { getDailyGift, afkStamina, sendLogAdmin } from '@/utils/apiRequest'
import { checkDevice } from '@/utils/funcs'
import { PC_CHECK } from '@/config'

import Header from './components/header.vue'
import Menu from './components/menu.vue'
import Loading from './components/loader.vue'

import SettingsTooltip from './components/tooltips/settings.vue'

import { showSettings, toggleSettings } from './components/tooltips/settings.vue'
import { useRouter } from 'vue-router';

const router = useRouter();

const useLoadingStorage = LoadingStorage()
const useUserStorage = UserStorage()

// начало загрузки
useLoadingStorage.start()

// получение данных
useTelegramSetup()

const afkStaminaInterval = setInterval(async () => {
  const response = await afkStamina(useUserStorage.user.user_id)
  if (response.success) {
    clearInterval(afkStaminaInterval)
    useUserStorage.costs.stamina_now = response.new_stamina
  }
}, 2000)

// конец загрузки
useLoadingStorage.stop()

setInterval(() => {
  if (useUserStorage.costs.stamina_now < useUserStorage.costs.stamina_costs) {
    useUserStorage.costs.stamina_now++
  }
}, 2000)

const isLoading = computed(() => useLoadingStorage.isLoading)
const locationApp = location.pathname

// settings click telegram
settingsTelegram(toggleSettings, 'app')

const redirectIfNeeded = async () => {
  if (PC_CHECK && checkDevice() && locationApp !== '/qr') {
    router.push('/qr')
    return
  }

  if (locationApp !== '/tutorial') {
    const response = await getDailyGift(useUserStorage.user.user_id)
    
    if (response.success && response.gift !== null && locationApp !== '/daily') {
      router.push('/daily')
    }
  }
}

redirectIfNeeded()

const showMainContent = async () => {
  return !['/tutorial', '/daily', '/qr'].includes(locationApp);
}

window.onerror = async function (message, source, lineno, colno) {
  await sendLogAdmin('error', {
    error: `${source.split('/').pop()}\n\n${lineno} строка, ${colno} колонка\n\n${message}`,
  });
};

const originalConsoleError = console.error;

console.error = async function (...args) {
  originalConsoleError(...args);

  const message = args.join(' ');
  const errorDetails = new Error().stack.split('\n');
  const source = errorDetails[1];
  
  await sendLogAdmin('error', {
    error: `${source.split('/').pop()}\n\n${message}`,
  });
};
</script>

<template>
  <div v-if="showMainContent">
    <SettingsTooltip :show="showSettings()" :langActive="true" />
    <Header v-if="!isLoading && locationApp !== '/qr' && locationApp !== '/tutorial' && locationApp !== '/daily'" />
    <Menu v-if="!isLoading && locationApp !== '/qr' && locationApp !== '/tutorial' && locationApp !== '/daily'" />
  </div>

  <Loading v-if="isLoading" />

  <div class="content" v-if="!isLoading">
    <RouterView />
  </div>
</template>
