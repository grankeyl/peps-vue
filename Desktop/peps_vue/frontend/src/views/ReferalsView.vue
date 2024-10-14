<script lang="ts">
import { ref, onMounted, computed } from 'vue'
import { UserStorage } from '@/stores/userStore'
import { getReferals, getAvatar } from '@/utils/apiRequest'
import { formatDate } from '@/utils/funcs'
import { telegramLink } from '@/composables/useTelegramSetup'
import { TelegramStorage } from '@/stores/telegramStore'
import { localText } from '@/interface'
import { TELEGRAM_BOT } from '@/config'

export default {
  setup() {
    const namePage = 'referals'

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

    const referalsList = ref('')
    const avatars = ref<Record<number, string>>({}) // Store avatars here
    const loaderStatusPage = ref(true)
    const showToast1 = ref(false)

    // Fetch avatar image for a user and store it in avatars
    const getAvatarImage = async (user_id: number) => {
      const response = await getAvatar(user_id)
      avatars.value[user_id] = response.avatar || './../assets/img/default_avatar.png'
    }

    // Fetch referals and avatars
    const fetchReferals = async () => {
      const interval = setInterval(async () => {
        if (userData.value.referals > 0) {
          const response = await getReferals(userData.value.user_id)
          if (response.success) {
            referalsList.value = response.referals
            loaderStatusPage.value = false
            clearInterval(interval)

            referalsList.value.forEach((referal: any) => {
              if (referal.username != 'Anonymous') {
                getAvatarImage(referal.user_id)
              }
            })
          }
        }
      }, 300)
    }

    fetchReferals()

    function repostGame() {
      let text_lg = ''

      if (userDataSettings.value.language === 'ru') {
        text_lg =
          '🐸 Лягушонок Пепе стал игрой! Прокачивай оборудование чтобы получить новые предметы и $PEPS. 🎁 Бери свою приветственную награду 2,500 $PEPS и лимитированный скин!'
      } else {
        text_lg =
          '🐸 Pepe the frog becomes a game! Upgrade your setup to get new items and $PEPS. 🎁 Claim your welcome gift, 2,500 $PEPS and limited skin'
      }

      const baseUrl = 'https://t.me/share/url?url='
      const appUrl = `https://t.me/${TELEGRAM_BOT}/app?startapp=${userData.value.referal_key}`
      const fullUrl = `${baseUrl}${encodeURIComponent(appUrl)}&text=${encodeURIComponent(text_lg)}`

      telegramLink(fullUrl)
    }

    function copyRepostGame() {
      let text_lg = ''

      if (userDataSettings.value.language === 'ru') {
        text_lg =
          '🐸 Лягушонок Пепе стал игрой! Прокачивай оборудование чтобы получить новые предметы и $PEPS. 🎁 Бери свою приветственную награду 2,500 $PEPS и лимитированный скин!'
      } else {
        text_lg =
          '🐸 Pepe the frog becomes a game! Upgrade your setup to get new items and $PEPS. 🎁 Claim your welcome gift, 2,500 $PEPS and limited skin'
      }

      const appUrl = `https://t.me/${TELEGRAM_BOT}/app?startapp=${userData.value.referal_key}`
      const fullUrl = `${appUrl}\n\n${text_lg}`

      const tempInput = document.createElement('input')
      tempInput.value = fullUrl
      document.body.appendChild(tempInput)
      tempInput.select()
      document.execCommand('copy')
      document.body.removeChild(tempInput)

      showToast1.value = true
      setTimeout(() => {
        showToast1.value = false
      }, 2000)
    }

    return {
      userData,
      referalsList,
      avatars,
      loaderStatusPage,
      formatDate,
      repostGame,
      copyRepostGame,
      showToast1,
      TELEGRAM_BOT,
      getAvatarImage,
      namePage,
      userDataSettings,
      localText
    }
  }
}
</script>

<template>
  <div class="referals">
    <div id="toast_1" :class="showToast1 ? 'show' : ''" class="toast">
      {{ localText['root'][userDataSettings.language].root_text_14 }}
    </div>

    <div class="referals_inner">
      <div class="referals_block">
        <div class="referals_block_title">
          <h4>{{ localText[namePage][userDataSettings.language].referals_text_1 }}</h4>
        </div>
        <div class="referals_block_link">
          <p>https://t.me/{{ TELEGRAM_BOT }}/app?startapp={{ userData.referal_key }}</p>
          <span @click="copyRepostGame">
            <img src="./../assets/img/copy.svg" alt="copy" />
          </span>
        </div>
        <div @click="repostGame" class="referals_block_button">
          <button>{{ localText[namePage][userDataSettings.language].referals_text_2 }}</button>
        </div>
      </div>
      <div class="referals_block">
        <div class="referals_block_title">
          <h4>{{ localText[namePage][userDataSettings.language].referals_text_3 }}</h4>
        </div>
        <div class="referals_block_users">
          <div v-if="userData.referals > 0" class="referals_block_users_title">
            <h4>
              <span>{{ userData.referals }}</span>
              {{ localText[namePage][userDataSettings.language].referals_text_4 }}
            </h4>
          </div>
          <div v-else style="margin-bottom: 0px" class="referals_block_users_title">
            <h4>
              <span>{{ userData.referals }}</span>
              {{ localText[namePage][userDataSettings.language].referals_text_4 }}
            </h4>
          </div>

          <div
            v-if="loaderStatusPage && userData.referals > 0"
            style="
              margin: auto;
              text-align: center;
              align-items: center;
              padding: 21px 0px;
              margin-bottom: -80px;
            "
          >
            <div class="jumping-dots-loader"><span></span> <span></span> <span></span></div>
          </div>

          <div v-if="userData.referals > 0" class="referals_block_users_items">
            <div v-for="referal in referalsList" class="referals_block_users_items_item">

              <div v-if="referal.username == 'Anonymous'" class="referals_block_users_items_item_avatar">
                <img :src="'/src/assets/img/shop_friend_1_circle.png'" alt="" />
              </div>

              <div v-else class="referals_block_users_items_item_avatar">
                <img v-if="avatars[referal.user_id] != 'None'" :src="avatars[referal.user_id] ? avatars[referal.user_id] : '/src/assets/img/default_avatar.png'" alt="" />
                <img v-else :src="'/src/assets/img/default_avatar.png'" alt="" />
              </div>

              <div class="referals_block_users_items_item_context">
                <div class="referals_block_users_items_item_context_name">
                  <h4 v-if="referal.username == 'Anonymous'">
                    Pepe frien
                    <img src="/src/assets/img/stars.svg" alt="">
                  </h4>
                  <h4 v-else>{{ referal.full_name }}</h4>
                </div>
                <div class="referals_block_users_items_item_context_date">
                  <p>
                    {{ localText[namePage][userDataSettings.language].referals_text_5 }}
                    {{ formatDate(referal.join_first) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '../assets/css/referals.css';
</style>
