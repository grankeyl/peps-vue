<script lang="ts">
import { ref, defineComponent, onMounted, onUnmounted, watch, computed } from 'vue'
import { UserStorage } from '@/stores/userStore'
import { setSettings } from '@/utils/apiRequest'

import { TelegramStorage } from '@/stores/telegramStore'
import { localText } from '@/interface'

const isShowSettings = ref(false)

export function showSettings() {
  return isShowSettings.value
}

export async function toggleSettings() {
  isShowSettings.value = !isShowSettings.value
}

export default defineComponent({
  props: {
    show: {
      type: Boolean,
      required: true
    },
    langActive: {
      type: Boolean,
      required: true
    }
  },
  setup(props) {
    const namePage = 'settings'

    const userStorage = UserStorage()
    const telegramStorage = TelegramStorage()

    const userDataSettings = computed(() => {
      const settings = userStorage.settings || {};
      return {
        ...settings,
        language: settings.language || telegramStorage.getUserLanguage() || 'en'
      };
    });

    const settingsTooltipVisible = ref(props.show)
    const languagesActive = ref(false)
    const tooltipRef = ref<HTMLElement | null>(null)

    watch(
      () => props.show,
      (newVal) => {
        settingsTooltipVisible.value = newVal
      }
    )

    watch(
      () => props.langActive,
      (newVal) => {
        languagesActive.value = newVal
      }
    )

    const toggleSettingsTooltip = async () => {
      settingsTooltipVisible.value = !settingsTooltipVisible.value
    }

    const toggleLang = () => {
      settingsTooltipVisible.value = false
      languagesActive.value = !languagesActive.value
    }

    const statusLanguage = computed(() => {
      return userStorage.settings.language
    })

    const statusTapAnimation = computed(() => {
      return userStorage.settings.tap_animation
    })

    const changeLanguage = async (language: string) => {
      userStorage.settings.language = language
      await setSettings(
        userStorage.user.user_id,
        userStorage.settings.language,
        userStorage.settings.tap_animation
      )
      languagesActive.value = false
      settingsTooltipVisible.value = false
      isShowSettings.value = !isShowSettings.value
      localStorage.setItem('languageUser', language)
    }

    const changeTapAnimation = async () => {
      userStorage.settings.tap_animation = !userStorage.settings.tap_animation
      await setSettings(
        userStorage.user.user_id,
        userStorage.settings.language,
        userStorage.settings.tap_animation
      )
      languagesActive.value = false
    }

    const handleClickOutside = (event: MouseEvent | TouchEvent) => {
      if (tooltipRef.value && !tooltipRef.value.contains(event.target as Node)) {
        settingsTooltipVisible.value = false
        isShowSettings.value = false
      }
    }

    onMounted(() => {
      document.addEventListener('mousedown', handleClickOutside)
      document.addEventListener('touchstart', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('mousedown', handleClickOutside)
      document.removeEventListener('touchstart', handleClickOutside)
    })

    return {
      settingsTooltipVisible,
      languagesActive,
      toggleSettingsTooltip,
      changeLanguage,
      changeTapAnimation,
      statusLanguage,
      statusTapAnimation,
      toggleLang,
      tooltipRef,

      namePage,
      userDataSettings,
      localText
    }
  }
})
</script>

<template>
  <div v-if="settingsTooltipVisible" ref="tooltipRef">
    <div class="settings_tooltip active">
      <div class="settings_tooltip_item">
        <p>{{ localText[namePage][userDataSettings.language].se_text_1 }}</p>
      </div>
      <div class="settings_tooltip_item_lead">
        <div class="settings_tooltip_item_lead_title">
          <p>{{ localText[namePage][userDataSettings.language].se_text_4 }}</p>
        </div>
        <div @click="toggleLang()" class="settings_tooltip_item_lead_flag">
          <img v-if="statusLanguage == 'ru'" src="../../assets/img/russian.png" alt="ru" />
          <img v-else src="../../assets/img/english.png" alt="en" />
          <span v-if="statusLanguage == 'ru'">Русский</span>
          <span v-else>English</span>
          <img src="../../assets/img/chevron_down.svg" alt="chevron_down" />
        </div>
      </div>
      <div class="settings_tooltip_item">
        <p>{{ localText[namePage][userDataSettings.language].se_text_3 }}</p>
        <label class="switch">
          <input
            v-if="statusTapAnimation"
            checked
            type="checkbox"
            id="tapAnimationsToggle"
            @change="changeTapAnimation"
          />
          <input v-else type="checkbox" id="tapAnimationsToggle" @change="changeTapAnimation" />
          <span class="switch_slider"></span>
        </label>
      </div>
    </div>
  </div>

  <div v-if="languagesActive" class="settings_tooltip_languages active">
    <div class="settings_tooltip_item" @click="() => changeLanguage('ru')">
      <div>
        <img src="../../assets/img/russian.png" alt="ru" />
        <p>Русский</p>
      </div>
    </div>
    <div class="settings_tooltip_item" @click="() => changeLanguage('en')">
      <div>
        <img src="../../assets/img/english.png" alt="en" />
        <p>English</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.settings_tooltip {
  /* Your tooltip styles */
  display: none;
}

.settings_tooltip.active {
  display: block;
}
</style>
