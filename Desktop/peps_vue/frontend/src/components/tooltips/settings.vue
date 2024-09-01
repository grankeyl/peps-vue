<script lang="ts">
import { ref, defineComponent, watch, computed } from 'vue'
import { UserStorage } from '@/stores/userStore'

import { setSettings } from '@/utils/apiRequest'

export default defineComponent({
  props: {
    show: {
      type: Boolean,
      required: true
    }
  },
  setup(props) {
    const userStorage = UserStorage()

    const settingsTooltipVisible = ref(props.show)
    const languagesActive = ref(false)

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
      if (!settingsTooltipVisible) settingsTooltipVisible.value = !settingsTooltipVisible.value
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
      if (userStorage.settings.language == 'ru') {
        userStorage.settings.language = 'en'
      } else {
        userStorage.settings.language = 'ru'
      }
      const result = await setSettings(
        userStorage.user.user_id,
        userStorage.settings.language,
        userStorage.settings.tap_animation
      )

      languagesActive.value = false
      settingsTooltipVisible.value = false
    }

    const changeTapAnimation = async () => {
      userStorage.settings.tap_animation = !userStorage.settings.tap_animation

      const result = await setSettings(
        userStorage.user.user_id,
        userStorage.settings.language,
        userStorage.settings.tap_animation
      )
      
      languagesActive.value = false
    }

    return {
      settingsTooltipVisible,
      languagesActive,
      toggleSettingsTooltip,
      changeLanguage,
      changeTapAnimation,
      statusLanguage,
      statusTapAnimation,
      toggleLang
    }
  }
})
</script>

<template>
  <div v-if="settingsTooltipVisible">
    <div class="settings_tooltip active">
      <div class="settings_tooltip_item">
        <p>Settings</p>
      </div>
      <div class="settings_tooltip_item_lead">
        <div class="settings_tooltip_item_lead_title">
          <p>Language</p>
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
        <p>Tap Animations</p>
        <label class="switch">
          <input
            v-if="statusTapAnimation"
            checked
            type="checkbox"
            id="tapAnimationsToggle"
            @change="changeTapAnimation"
          />
          <input 
          v-else 
          type="checkbox" 
          id="tapAnimationsToggle" @change="changeTapAnimation" />
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
