<script lang="ts">
import { UserStorage } from '@/stores/userStore'
import { defineComponent, computed, onMounted, ref, watch } from 'vue'
import { formatNumber } from '@/utils/funcs'

export default defineComponent({
  setup() {
    const useUserStore = UserStorage()

    const userData = computed(() => useUserStore.user || {})
    const balance = computed(() => userData.value.balance || {})

    const headerButtonViewsImage = ref<HTMLElement | null>(null)
    const headerButtonViewsP = ref<HTMLElement | null>(null)
    const headerButtonMoneyImage = ref<HTMLElement | null>(null)
    const headerButtonMoneyP = ref<HTMLElement | null>(null)
    const headerButtonTonImage = ref<HTMLElement | null>(null)
    const headerButtonTonP = ref<HTMLElement | null>(null)

    function updateElementStyle(imageElement: HTMLElement | null, textElement: HTMLElement | null) {
      if (!imageElement || !textElement) return
      const textLength = textElement.textContent?.trim().length || 0
      if (textLength === 8) {
        textElement.style.fontSize = '9px'
        imageElement.style.width = '18px'
        imageElement.style.height = '25px'
        textElement.style.marginLeft = '0px'
      } else if (textLength === 6) {
        textElement.style.fontSize = '9px'
        imageElement.style.width = '18px'
        imageElement.style.height = '25px'
        textElement.style.marginLeft = '0px'
      } else if (textLength === 5) {
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

    onMounted(() => {
      updateElementStyleScript()
    })

    watch(balance, () => {
      updateElementStyleScript()
    })

    return {
      balance,
      formatNumber,
      headerButtonViewsImage,
      headerButtonViewsP,
      headerButtonMoneyImage,
      headerButtonMoneyP,
      headerButtonTonImage,
      headerButtonTonP,
    }
  }
})
</script>

<template>
  <header class="header">
    <div class="header_buttons">
      <div id="header_button_views_block" class="header_button">
        <img ref="headerButtonViewsImage" id="header_button_views_image" src="./../assets/img/eye.svg" alt="eye" />
        <p ref="headerButtonViewsP" id="header_button_views">{{ formatNumber(balance.views) }}</p>
      </div>
      <div id="header_button_money_block" class="header_button">
        <img ref="headerButtonMoneyImage" id="header_button_money_image" src="./../assets/img/money.svg" alt="money" />
        <p ref="headerButtonMoneyP" id="header_button_money">{{ formatNumber(balance.earn) }}</p>
      </div>
      <div id="header_button_ton_block" class="header_button">
        <img ref="headerButtonTonImage" id="header_button_ton_image" src="./../assets/img/diamond.svg" alt="diamond" />
        <p ref="headerButtonTonP" id="header_button_diamonds">{{ ((balance.ton * 1)).toFixed(1) }}</p>
      </div>
      <div class="header_button">
        <img src="./../assets/img/energy.svg" alt="energy" />
        <p>Soon</p>
        <img class="chevrone" src="./../assets/img/chevrone_right.svg" alt="chevrone_right" />
      </div>
    </div>
  </header>
</template>