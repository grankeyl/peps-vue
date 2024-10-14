<script lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Rive } from '@rive-app/canvas'

import { getJsonDataTexts } from '@/utils/funcs'
import { TelegramStorage } from '@/stores/telegramStore'
import { UserStorage } from '@/stores/userStore'
import { localText } from '@/interface'

export default {
  setup() {
    const namePage = 'chestdev'

    const useUserStore = UserStorage()
    const telegramStorage = TelegramStorage()

    const userDataSettings = computed(() => {
      const settings = useUserStore.settings || {}
      return {
        ...settings,
        language: settings.language || telegramStorage.getUserLanguage() || 'en'
      }
    })

    let riveInstanceChest: Rive | null = null
    const createGameChest = async () => {
      const GameChestClass = document.getElementById('chestDev_canvas') as HTMLCanvasElement | null
      if (GameChestClass) {
        // Настройка для высококачественной графики
        const dpr = window.devicePixelRatio || 1
        GameChestClass.width = GameChestClass.clientWidth * dpr
        GameChestClass.height = GameChestClass.clientHeight * dpr
        const context = GameChestClass.getContext('2d')
        if (context) {
          riveInstanceChest = new Rive({
            src: `/src/assets/animations/peps_case_icon.riv`,
            canvas: GameChestClass,
            autoplay: false,
            useOffscreenRenderer: true,
            onLoad: () => {
              console.log('Rive loaded successfully')
            },
            onError: (e) => {
              console.error('Rive load error:', e)
            }
          })
          riveInstanceChest.play()
        }
      } else {
        console.error('Canvas element not found')
      }
    }
    onMounted(() => {
      createGameChest()
    })

    return {
      namePage,
      userDataSettings,
      localText
    }
  }
}
</script>

<template>
  <div class="chestDev">
    <div class="chestDev_inner">
      <div class="chestDev_context">
        <div class="chestDev_context_canvas">
          <canvas id="chestDev_canvas" width="880" height="360"></canvas>
        </div>
        <div class="chestDev_context_h">
          <h4>{{ localText[namePage][userDataSettings.language].chestdev_text_1 }}</h4>
        </div>
        <div class="chestDev_context_p">
          <p>{{ localText[namePage][userDataSettings.language].chestdev_text_2 }}</p>
        </div>
      </div>

      <div class="chestDev_buttons">
        <!-- <div class="chestDev_button_p">
                    <p>Следите за обновлениями</p>
                </div> -->
        <div class="chestDev_button_btn">
          <button>{{ localText[namePage][userDataSettings.language].chestdev_text_3 }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '../assets/css/chest.css';
</style>
