<script lang="ts">
import { defineComponent, ref } from 'vue'
import { TELEGRAM_BOT } from '@/config'
import { UserStorage } from '@/stores/userStore';

const name = 'QrView'

export default defineComponent({
  setup() {
    const userStorage = UserStorage()

    const createQr = () => {
      // API для создания QR-кода
      const qrApi = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="

      // Добавление рефералльной ссылки
      const qrLink = qrApi + `https://t.me/${TELEGRAM_BOT}/app?startapp=${userStorage.referal_key}`

      return qrLink
    }

    return {
      createQr
    }
  }
})
</script>

<template>
  <div class="pc_screen" id="pc_screen">
      <div class="pc_screen_inner">

          <div class="pc_screen_top">
              <img src="./../assets/img/pc_screen.png" alt="pc_screen">
          </div>

          <div class="pc_screen_h">
              <h4>Play on mobile 🐸</h4>
          </div>

          <div class="pc_screen_bottom" id="pc_screen_bottom">
              <img id="qr-code" :src="createQr()" alt="">
          </div>

      </div>
  </div>
</template>

<style scoped>
@import '../assets/css/qr.css';
</style>
