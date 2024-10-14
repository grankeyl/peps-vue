<template>
  <div class="shop_section_friends_item">
    <div class="shop_section_friends_item_left">
      <img :src="photo" alt="upgrade_friends" />
    </div>
    <div class="shop_section_friends_item_right">
      <div class="shop_section_friends_item_right_title">
        <h4>{{ title }}</h4>
      </div>
      <div class="shop_section_friends_item_right_descr">
        <p>{{ description }}</p>
      </div>
        <div
          @click="_buyFriends"
          :id="'buyFriends#' + id"
          class="shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
        >
          <button id="buy_friend">
            <div class="shop_section_buy_items_item_buy_button_info">
              <img
                class="button_loading_img"
                src="./../../assets/img/button_loading.svg"
                alt="loading"
              />
              <img src="./../../assets/img/stars.svg" alt="buy" />
              <p>{{ starsPrice }}</p>
            </div>
          </button>
        </div>

    </div>
  </div>
</template>

<script>
import { generateRandomId } from '@/utils/funcs'
import { 
  createStarsLink, 
  getInvoice, 
  existsInvoice, 
  updateReferals,
  sendLogAdmin
} from '@/utils/apiRequest'
import { telegramLink } from '@/composables/useTelegramSetup'

export default {
  name: "FR_ShopItem",
  props: {
    id: {
      type: Number,
      required: true
    },
    photo: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    prizeAmount: {
      type: Number,
      required: true
    },
    starsPrice: {
      type: Number,
      required: true
    },
    userStorage: {
      type: Object,
      required: true,
    },
    toast: {
      type: Boolean,
      required: true,
    }
  },
  computed: {},
  methods: {
    async _buyFriends() {
      const buttonBlock = document.getElementById(`buyFriends#${this.id}`)
      if (buttonBlock.classList.contains('disabled')) return
      buttonBlock.classList.remove('actived')
      buttonBlock.classList.add('button_loading')
      buttonBlock.classList.add('disabled')

      let randomId = generateRandomId()

      const checkInvoiceId = await existsInvoice(randomId)
      if (checkInvoiceId.exists) {
        randomId = generateRandomId()
      }

      const stars_data_json = {
        invoice: `${randomId}@buyFriends`,
        isGift: true,
        giftAmount: `none`,
        giftHasSkin: false,
        giftSkin: 'none'
      }

      const selectedConfig = 'buyFriends'

      if (selectedConfig) {
        const stars_data = await createStarsLink(
          this.userStorage.user.user_id,
          `${this.prizeAmount} friends`,
          'Purchase for @PepsGameBot',
          parseInt(this.starsPrice),
          location.pathname.replace(/[^\/]+$/, '') + '../assets/img/energy.svg',
          JSON.stringify(stars_data_json)
        )

        if (stars_data.success) {
          telegramLink(stars_data.data['invoice_link'])

          const checkInvoiceInterval = setInterval(async () => {
            const checkInvoice = await getInvoice(randomId)

            if (checkInvoice.success && checkInvoice.invoice.invoice_status === 'paid') {
              const updateReferalsData = await updateReferals(
                this.userStorage.user.user_id,
                this.prizeAmount,
                this.userStorage.user.referal_key
              )
              
              if (updateReferalsData.success) {
                this.userStorage.user.referals = parseInt(this.userStorage.user.referals) + parseInt(this.prizeAmount)
              } else {
                await updateReferals(
                  this.userStorage.user.user_id,
                  this.prizeAmount,
                  this.userStorage.user.referal_key
                )
                this.userStorage.user.referals = parseInt(this.userStorage.user.referals) + parseInt(this.prizeAmount)
              }

              clearInterval(checkInvoiceInterval)
              this.$emit('update-toast', true);
              setTimeout(() => this.$emit('update-toast', false), 3650);

              await sendLogAdmin('donate', {
                user_id: this.userStorage.user.user_id,
                prize: `Покупка ${this.prizeAmount} друзей`,
                amount: parseInt(this.starsPrice)
              })

              setTimeout(() => {
                buttonBlock.classList.remove('button_loading')
                buttonBlock.classList.remove('disabled')
                buttonBlock.classList.add('actived')
              }, 300)
            }
          }, 2100)
        }
        
    }
  }
  }
}
</script>

<style scoped>
@import '@/assets/css/upgrades.css';
@import '@/assets/css/profile.css';
@import '@/assets/css/shop.css';
</style>