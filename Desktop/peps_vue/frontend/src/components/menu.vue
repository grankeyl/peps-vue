<script lang="ts">
import { onMounted, computed } from 'vue'
import { UserStorage } from '@/stores/userStore'
import { localText } from '@/interface'
import { TelegramStorage } from '@/stores/telegramStore'

export default {
  setup() {
    const namePage = 'menu'

    const useUserStore = UserStorage()
    const telegramStorage = TelegramStorage()

    const userData = computed(() => useUserStore.user || {})

    const userDataSettings = computed(() => {
      const settings = useUserStore.settings || {}
      return {
        ...settings,
        language: settings.language || telegramStorage.getUserLanguage() || 'en'
      }
    })

    return {
      namePage,
      userData,
      userDataSettings,
      localText
    }
  }
}
</script>

<template>
  <div class="menu">
    <div class="menu_buttons">
      <RouterLink to="/">
        <div class="menu_button">
          <img style="object-fit: contain" src="./../assets/img/diamond.svg" alt="diamond" />
          <p>{{ localText[namePage][userDataSettings.language].me_text_1 }}</p>
        </div>
      </RouterLink>

      <RouterLink to="/earn">
        <div class="menu_button">
          <img style="object-fit: contain" src="./../assets/img/money.svg" alt="money" />
          <p>{{ localText[namePage][userDataSettings.language].me_text_2 }}</p>
        </div>
      </RouterLink>

      <RouterLink to="/upgrades">
        <div class="menu_button">
          <img style="object-fit: contain" src="./../assets/img/energy.svg" alt="energy" />
          <p>{{ localText[namePage][userDataSettings.language].me_text_3 }}</p>
        </div>
      </RouterLink>

      <RouterLink to="/shop">
        <div class="menu_button">
          <img style="object-fit: contain" src="./../assets/img/shop.svg" alt="shop" />
          <p>{{ localText[namePage][userDataSettings.language].me_text_4 }}</p>
        </div>
      </RouterLink>

      <RouterLink to="/profile">
        <div class="menu_button">
          <img style="object-fit: contain" src="./../assets/img/profile.svg" alt="profile" />
          <p>{{ localText[namePage][userDataSettings.language].me_text_5 }}</p>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped></style>
