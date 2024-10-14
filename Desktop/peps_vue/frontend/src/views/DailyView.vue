<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import {
  getDailyAll,
  getDailyGift,
  updateBalance,
  existsInvoice,
  createStarsLink,
  getInvoice,
  sendLogAdmin,
  getGiftsStars
} from '@/utils/apiRequest'
import { getImage, getRare, generateRandomId } from '@/utils/funcs'
import { UserStorage } from '@/stores/userStore'
import { useRouter } from 'vue-router'
import { __DAILY_REWARD__ } from '@/utils/constants'
import { telegramLink } from '@/composables/useTelegramSetup'

import { TelegramStorage } from '@/stores/telegramStore'
import { localText } from '@/interface'

export default defineComponent({
  setup() {
    const router = useRouter()
    const namePage = 'daily'

    const daily = ref([])
    const existingGifts = ref([])

    const userStorage = UserStorage()
    const telegramStorage = TelegramStorage()

    const userDataSettings = computed(() => {
      const settings = userStorage.settings || {}
      return {
        ...settings,
        language: settings.language || telegramStorage.getUserLanguage() || 'en'
      }
    })

    const loaderStatusPage = ref(true)

    const showToast1 = ref(false)

    const fetchDaily = async () => {
      const interval = setInterval(async () => {
        const response = await getDailyAll()
        if (response.success) {
          daily.value = response.daily
          console.log(daily.value)
          loaderStatusPage.value = false
          clearInterval(interval)
        }
      }, 1000)
    }

    fetchDaily()

    const getGift = async () => {
      const interval = setInterval(async () => {
        const response = await getDailyGift(userStorage.user.user_id)
        if (response.success) {
          if (response.gift !== null) {
            existingGifts.value = response.gifts
            await getPrizeGift(response.gift)
            clearInterval(interval)
          } else {
            existingGifts.value = response.gifts
            console.log(existingGifts.value)
            clearInterval(interval)
          }
        }
      }, 1000)
    }

    getGift()

    const getPrizeGift = async (dl: any) => {
      if (dl.gift_skin == 'None') {
        if (dl.gift_type == 'views') {
          userStorage.user.balance.earn += parseInt(dl.gift_amount)

          await updateBalance(userStorage.user.user_id, 'views', '+' + dl.gift_amount)
        } else if (dl.gift_type == 'money') {
          userStorage.user.balance.earn += parseInt(dl.gift_amount)

          await updateBalance(userStorage.user.user_id, 'money', '+' + dl.gift_amount)
        } else if (dl.gift_type == 'ton') {
          userStorage.user.balance.ton += parseInt(dl.gift_amount)

          await updateBalance(userStorage.user.user_id, 'ton', '+' + dl.gift_amount)
        }
      } else {
      }
    }

    const clickGame = () => {
      const click_game_button = document.querySelector('.daily_get_button')
      click_game_button.classList.add('active')

      setTimeout(() => {
        click_game_button.classList.remove('active')
        location.href = `/`
      }, 1200)
    }

    const dailyBuyAllStars = async (starsAmount: any) => {
      const blockUpgrade = document.getElementById(`donate_daily_all`)
      if (blockUpgrade.classList.contains('disabled')) return
      blockUpgrade.classList.remove('actived')
      blockUpgrade.classList.add('button_loading')
      blockUpgrade.classList.add('disabled')

      let randomId = generateRandomId()

      const checkInvoiceId = await existsInvoice(randomId)
      if (checkInvoiceId.exists) {
        randomId = generateRandomId()
      }

      const stars_data_json = {
        invoice: randomId + '@' + 'dailyAll',
        isGift: true,

        giftAmount: 'None' + '|' + 0,

        giftHasSkin: false,
        giftSkin: 'None'
      }

      let stars_data = await createStarsLink(
        userStorage.user.user_id,
        `All daily rewards`,
        'Purchase for @PepsGameBot',
        parseInt(starsAmount),
        'https://i.ibb.co/dK5gscs/1-4.png',
        JSON.stringify(stars_data_json)
      )

      if (stars_data.success) {
        telegramLink(stars_data.data['invoice_link'])

        // цикл проверки оплаты
        const checkInvoiceInterval = setInterval(async () => {
          const checkInvoice = await getInvoice(randomId)

          if (checkInvoice.success) {
            if (checkInvoice.invoice.invoice_status === 'paid') {
              clearInterval(checkInvoiceInterval)
              await getGiftsStars(userStorage.user.user_id)

              document.querySelectorAll('.daily_rewards_item_grided').forEach((item) => {
                item.classList.add('active')
              })

              showToast1.value = true
              setInterval(() => {
                showToast1.value = false
              }, 3650)

              await sendLogAdmin('donate', {
                user_id: userStorage.user.user_id,
                prize: `Все призы дневного бонуса`,
                amount: parseInt(starsAmount)
              })

              setTimeout(() => {
                blockUpgrade.classList.remove('button_loading')
                blockUpgrade.classList.remove('disabled')
                blockUpgrade.classList.add('actived')
              }, 300)
            }
          }
        }, 1000)
      }
    }

    return {
      daily,
      getImage,
      getRare,
      existingGifts,
      loaderStatusPage,
      clickGame,
      dailyBuyAllStars,
      showToast1,

      namePage,
      userDataSettings,
      localText,

      __DAILY_REWARD__
    }
  }
})
</script>

<template>
  <div id="toast_1" :class="showToast1 ? 'show' : ''" class="toast purchase">
    {{ localText['root'][userDataSettings.language].root_text_13 }}
  </div>

  <div class="daily">
    <div class="daily_inner">
      <div class="daily_context">
        <div class="daily_image">
          <img src="/src/assets/img/money_four.svg" alt="money_four" />
        </div>

        <div class="daily_title">
          <h4>{{ localText[namePage][userDataSettings.language].da_text_1 }}</h4>
        </div>

        <div class="daily_description">
          <p>{{ localText[namePage][userDataSettings.language].da_text_2 }}</p>
        </div>

        <div
          v-if="loaderStatusPage"
          style="margin: auto; text-align: center; align-items: center; padding: 140px 0px"
        >
          <div class="jumping-dots-loader"><span></span> <span></span> <span></span></div>
        </div>

        <div class="daily_rewards">
          <div v-for="dl in daily" class="foreachBlock">
            <div
              class="daily_rewards_item_grided"
              :class="{ active: existingGifts[dl.gift_uuid - 1] }"
            >
              <div class="daily_rewards_item">
                <div class="daily_rewards_item_day">
                  <p>
                    {{ dl.gift_uuid }}
                    {{ localText[namePage][userDataSettings.language].da_text_3 }}
                  </p>
                </div>

                <div v-if="dl.gift_skin == 'None'" class="daily_rewards_item_context">
                  <div class="daily_rewards_item_context_image">
                    <img v-if="dl.gift_type == 'views'" src="/src/assets/img/eye.svg" alt="views" />
                    <img
                      v-if="dl.gift_type == 'money' && dl.gift_amount >= 1000"
                      src="/src/assets/img/money_three.svg"
                      alt="money_three"
                    />
                    <img
                      v-if="dl.gift_type == 'money' && dl.gift_amount < 1000"
                      src="/src/assets/img/money.svg"
                      alt="money_three"
                    />
                    <img v-if="dl.gift_type == 'ton'" src="/src/assets/img/diamond.svg" alt="ton" />
                  </div>
                  <div class="daily_rewards_item_context_prize">
                    <p>{{ dl.gift_amount }}</p>
                  </div>
                </div>

                <div v-else class="upgrades_section_skins_item_left_skin" :class="dl.rare">
                  <img src="/src/assets/img/upgrades_effect.png" alt="upgrades_effect" />
                  <img :src="getImage(dl.gift_skin)" alt="skin" />
                  <p v-if="dl.baffs_type == false">
                    {{ localText['root'][userDataSettings.language].root_text_1 }}
                  </p>
                  <p v-else>
                    {{ getRare(userDataSettings.language, dl.baffs_buy_type, dl.baffs_percentage) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="daily_buttons">
        <div
          @click="dailyBuyAllStars(__DAILY_REWARD__.starsAmount)"
          class="daily_donate_button"
          id="donate_daily_all"
        >
          <p>{{ localText[namePage][userDataSettings.language].da_text_4 }}</p>
          <span>
            <img src="/src/assets/img/stars.svg" alt="money" />
            {{ __DAILY_REWARD__.starsAmount }}
          </span>
        </div>
        <div @click="clickGame" class="daily_get_button" id="play_game">
          <img class="button_loading_img" src="./../assets/img/button_loading.svg" alt="loading" />
          <p>{{ localText[namePage][userDataSettings.language].da_text_5 }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '../assets/css/daily.css';
@import '../assets/css/upgrades.css';
</style>
