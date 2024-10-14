<script lang="ts">
import { UserStorage } from '@/stores/userStore'
import { defineComponent, computed, onMounted, ref, watch } from 'vue'
import { TelegramStorage } from '@/stores/telegramStore'
import { localText } from '@/interface'

export default defineComponent({
  setup() {
    const namePage = 'header'

    const useUserStore = UserStorage()
    const telegramStorage = TelegramStorage()

    const userData = computed(() => useUserStore.user || {})
    const balance = computed(() => userData.value.balance || {})

    const userDataSettings = computed(() => {
      const settings = useUserStore.settings || {}
      return {
        ...settings,
        language: settings.language || telegramStorage.getUserLanguage() || 'en'
      }
    })

    const headerButtonViewsImage = ref<HTMLElement | null>(null)
    const headerButtonViewsP = ref<HTMLElement | null>(null)
    const headerButtonMoneyImage = ref<HTMLElement | null>(null)
    const headerButtonMoneyP = ref<HTMLElement | null>(null)
    const headerButtonTonImage = ref<HTMLElement | null>(null)
    const headerButtonTonP = ref<HTMLElement | null>(null)

    function updateElementStyle(imageElement: HTMLElement | null, textElement: HTMLElement | null) {
      if (!imageElement || !textElement) return
      const textLength = textElement.textContent?.trim().length || 0
      if (textLength >= 8) {
        textElement.style.fontSize = '9px'
        imageElement.style.width = '18px'
        imageElement.style.height = '25px'
        textElement.style.marginLeft = '0px'
      } else if (textLength >= 6) {
        textElement.style.fontSize = '9px'
        imageElement.style.width = '18px'
        imageElement.style.height = '25px'
        textElement.style.marginLeft = '0px'
      } else if (textLength <= 5) {
        textElement.style.fontSize = '11px'
        textElement.style.marginLeft = '-2px'
        imageElement.style.width = '24px'
        imageElement.style.height = '19px'
      }
    }

    function updateElementStyleScript() {
      updateElementStyle(headerButtonViewsImage.value, headerButtonViewsP.value)
      updateElementStyle(headerButtonMoneyImage.value, headerButtonMoneyP.value)
      updateElementStyle(headerButtonTonImage.value, headerButtonTonP.value)
    }

    const formatNumberHeader = (value: number) => {
      const nonNegativeValue = Math.max(0, value)
      const absValue = Math.abs(nonNegativeValue)

      if (absValue >= 1_000_000_000_000) {
        return Math.floor((nonNegativeValue / 1_000_000_000_000) * 10) / 10 + 'T'
      } else if (absValue >= 1_000_000_000) {
        return Math.floor((nonNegativeValue / 1_000_000_000) * 10) / 10 + 'B'
      } else if (absValue >= 1_000_000) {
        return Math.floor((nonNegativeValue / 1_000_000) * 10) / 10 + 'M'
      } else if (absValue >= 1_000) {
        return Math.floor((nonNegativeValue / 1_000) * 10) / 10 + 'k'
      } else {
        return (nonNegativeValue * 1).toFixed(0)
      }
    }

    onMounted(() => {
      updateElementStyleScript()
    })

    watch(balance, () => {
      updateElementStyleScript()
    })

    return {
      balance,
      headerButtonViewsImage,
      headerButtonViewsP,
      headerButtonMoneyImage,
      headerButtonMoneyP,
      headerButtonTonImage,
      headerButtonTonP,
      formatNumberHeader,

      namePage,
      localText,
      userDataSettings
    }
  }
})
</script>

<template>
  <header class="header">
    <div class="header_buttons">
      <RouterLink to="/profile">
        <div id="header_button_views_block" class="header_button">
          <img
            ref="headerButtonViewsImage"
            id="header_button_views_image"
            src="./../assets/img/eye.svg"
            alt="eye"
          />
          <p ref="headerButtonViewsP" id="header_button_views">
            {{ formatNumberHeader(balance.views) }}
          </p>
        </div>
      </RouterLink>

      <RouterLink to="/shop">
        <div id="header_button_money_block" class="header_button">
          <img
            ref="headerButtonMoneyImage"
            id="header_button_money_image"
            src="./../assets/img/money.svg"
            alt="money"
          />
          <p ref="headerButtonMoneyP" id="header_button_money">
            {{ formatNumberHeader(balance.earn) }}
          </p>
          <span>
            <svg
              width="7"
              height="7"
              viewBox="0 0 7 7"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M2.84365 6.46625V0.915275H3.94809V6.46625H2.84365ZM0.622435 4.24093V3.13649H6.17341V4.24093H0.622435Z"
                fill="#1E8723"
              />
            </svg>
          </span>
        </div>
      </RouterLink>

      <RouterLink to="/profile">
        <div id="header_button_ton_block" class="header_button">
          <img
            ref="headerButtonTonImage"
            id="header_button_ton_image"
            src="./../assets/img/diamond.svg"
            alt="diamond"
          />
          <p ref="headerButtonTonP" id="header_button_diamonds">
            {{ (balance.ton * 1).toFixed(2) }}
          </p>
        </div>
      </RouterLink>

      <div class="header_button">
        <img src="./../assets/img/energy.svg" alt="energy" />
        <p>{{ localText[namePage][userDataSettings.language].he_text_1 }}</p>
        <img class="chevrone" src="./../assets/img/chevrone_right.svg" alt="chevrone_right" />
      </div>
    </div>
  </header>
</template>
