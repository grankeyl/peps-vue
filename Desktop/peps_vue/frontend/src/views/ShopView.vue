<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { LoadingStorage } from '@/stores/loadingStorage'
import {
  getShopItems,
  buySkin,
  changeSkin,
  buy,
  getTask,
  taskNextStep,
  addExperience,
  shopBandles,
  createStarsLink,
  getInvoice,
  existsInvoice,
  updateSpecials,
  sendLogAdmin
} from '@/utils/apiRequest'
import {
  formatNumber,
  generateRandomId,
  getJsonDataSpecial,
  getImage,
  getSkinJson,
  startTimerSpecial
} from '@/utils/funcs'
import { telegramLink } from '@/composables/useTelegramSetup'
import { UserStorage } from '@/stores/userStore'
import { useRoute } from 'vue-router'

import { getRare } from '@/utils/funcs'
import { TelegramStorage } from '@/stores/telegramStore'
import { localText } from '@/interface'

import { __SHOP_STARS_BANDLES__, __SHOP_STARS_FRIENDS__ } from '@/utils/constants'
import { useRouter } from 'vue-router'

import FR_ShopItem from "@/views/improves/FR_ShopItem.vue";
import Preview_ShopItem from "@/views/improves/Preview_ShopItem.vue";

export default defineComponent({
  components: {
    FR_ShopItem,
    Preview_ShopItem
  },
  setup() {
    const route = useRoute()
    const router = useRouter()

    const namePage = 'shop'

    const shopItems = ref([])
    const specialsItems = ref([])
    const useLoadingStore = LoadingStorage()
    const userStorage = UserStorage()
    const useTelegramStore = TelegramStorage()

    const userDataSettings = computed(() => {
      const settings = userStorage.settings || {}
      return {
        ...settings,
        language: settings.language || useTelegramStore.getUserLanguage() || 'en'
      }
    })

    const task = ref(null)

    const loaderStatusPageSpecials = ref(true)
    const loaderStatusPage = ref(true)
    const responseGetTask = ref(false)

    const showToast1 = ref(false)
    const showToast2 = ref(false)
    const showToast3 = ref(false)
    const showToast4 = ref(false)
    const starsBandleValue = ref(0)

    let interval_getTask = ''

    useLoadingStore.start()

    const fetchItems = async () => {
      const response = await getShopItems(userStorage.user.user_id)

      if (response.success) {
        shopItems.value = response.items
        loaderStatusPage.value = false
        clearInterval(interval)
      }
    }

    const interval = setInterval(async () => {
      await fetchItems()
    }, 400)

    useLoadingStore.isLoading = false

    function getImage(skin_id: string) {
      return './src/assets/skins/' + skin_id + '.png'
    }

    async function buySkinShop(item) {
      const buttonBlock = document.getElementById(`shop#${item.skin_id}`)

      if (!buttonBlock) return

      const buttonUnsafe = buttonBlock.querySelector(
        '.upgrades_section_skins_item_right_upgrade_btn'
      )

      if (buttonUnsafe.classList.contains('disabled')) return

      buttonUnsafe.classList.remove('actived')
      buttonUnsafe.classList.add('button_loading')
      buttonUnsafe.classList.add('disabled')

      const response = await buySkin(userStorage.user.user_id, item.skin_id)
      const response_buy = await buy(
        userStorage.user.user_id,
        item.shop_settings['shop_price_type'],
        item.shop_settings['shop_price_cost']
      )

      if (response_buy.success) {
        let profileBandles, baffsPercents, baffsAdding, percentValue

        if (item.shop_settings['shop_price_type'] == 'views') {
          userStorage.user.balance.views -= item.shop_settings['shop_price_cost']
        } else if (item.shop_settings['shop_price_type'] == 'money') {
          userStorage.user.balance.earn -= item.shop_settings['shop_price_cost']
        } else {
          userStorage.user.balance.ton -= item.shop_settings['shop_price_cost']
        }

        if (item.baffs['baffs_type'] == true) {
          if (item.baffs['baffs_buy_type'] == 'views') {
            profileBandles = userStorage.costs.views_costs
            baffsPercents = item.baffs['baffs_buy_percentage']
            baffsAdding = item.baffs['baffs_adding_views']
            percentValue = (profileBandles / 100) * baffsPercents

            item.baffs['baffs_adding_views'] = parseInt(baffsAdding) + parseInt(percentValue)
            userStorage.costs.views_costs =
              parseInt(userStorage.costs.views_costs) + parseInt(percentValue)
          } else if (item.baffs['baffs_buy_type'] == 'money') {
            profileBandles = userStorage.costs.money_costs
            baffsPercents = item.baffs['baffs_buy_percentage']
            baffsAdding = item.baffs['baffs_adding_money']
            percentValue = (profileBandles / 100) * baffsPercents

            item.baffs['baffs_adding_money'] = parseInt(baffsAdding) + parseInt(percentValue)
            userStorage.costs.money_costs =
              parseInt(userStorage.costs.money_costs) + parseInt(percentValue)
          } else if (item.baffs['baffs_buy_type'] == 'stamina') {
            profileBandles = userStorage.costs.stamina_costs
            baffsPercents = item.baffs['baffs_buy_percentage']
            baffsAdding = item.baffs['baffs_adding_stamina']
            percentValue = (profileBandles / 100) * baffsPercents

            item.baffs['baffs_adding_stamina'] = parseInt(baffsAdding) + parseInt(percentValue)
            userStorage.costs.stamina_costs =
              parseInt(userStorage.costs.stamina_costs) + parseInt(percentValue)
          }
        }
        if (response.success) {
          if (item.rare == 'rare') {
            await addExperience(userStorage.user.user_id, 100)
            userStorage.user.experience = userStorage.user.experience + 100
          } else if (item.rare == 'very_rare') {
            await addExperience(userStorage.user.user_id, 150)
            userStorage.user.experience = userStorage.user.experience + 150
          } else if (item.rare == 'epic') {
            await addExperience(userStorage.user.user_id, 350)
            userStorage.user.experience = userStorage.user.experience + 350
          } else if (item.rare == 'legendary') {
            await addExperience(userStorage.user.user_id, 700)
            userStorage.user.experience = userStorage.user.experience + 700
          }

          const response_change = await changeSkin(userStorage.user.user_id, item.skin_id)

          if (response_change.success) {
            buttonUnsafe.classList.remove('button_loading')
            buttonUnsafe.classList.remove('disabled')
            buttonUnsafe.classList.add('actived')

            if (responseGetTask) {
              if (task.value) {
                if (task.value.task_type == 'buy:skin') {
                  const response = await taskNextStep(task.value.id, userStorage.user.user_id)
                  userStorage.user.tasks_progress[task.value.id].current_step =
                    userStorage.user.tasks_progress[task.value.id].current_step + 1
                }
              }
            }

            localStorage.setItem('skin_id', item.skin_id)
            router.push('/')
          }
        }
      }
    }

    const getTaskFunction = async (taskId: string) => {
      try {
        if (taskId) {
          const response = await getTask(taskId, userStorage.user.user_id)

          if (response?.success) {
            task.value = response.task
            responseGetTask.value = true
            clearInterval(interval_getTask)
            return true
          } else {
            responseGetTask.value = false
            return false
          }
        }
      } catch (error) {
        return false
      }
    }

    if (route.query.task) {
      interval_getTask = setInterval(async () => {
        await getTaskFunction(route.query.task as string)
      }, 400)
    }

    const checkBuyButton = (item) => {
      if (item.shop_settings.shop_price_type == 'views') {
        if (item.quantity == -1) {
          return userStorage.user.balance.views >= item.shop_settings.shop_price_cost
        } else if (item.quantity-item.quantity_count == item.quantity) {
          return userStorage.user.balance.views >= item.shop_settings.shop_price_cost
        } else if (item.quantity-item.quantity_count == 0) {
          return false
        } else {
          return userStorage.user.balance.views >= item.shop_settings.shop_price_cost
        }
      } else if (item.shop_settings.shop_price_type == 'money') {
        if (item.quantity == -1) {
          return userStorage.user.balance.earn >= item.shop_settings.shop_price_cost
        } else if (item.quantity-item.quantity_count == item.quantity) {
          return userStorage.user.balance.earn >= item.shop_settings.shop_price_cost
        } else if (item.quantity-item.quantity_count == 0) {
          return false
        } else {
          return userStorage.user.balance.earn >= item.shop_settings.shop_price_cost
        }
      } else if (item.shop_settings.shop_price_type == 'stars') {
        if (item.quantity == -1) {
          return true
        } else if (item.quantity-item.quantity_count == item.quantity) {
          return true
        } else if (item.quantity-item.quantity_count == 0) {
          return false
        } else {
          return true
        }
      } else {
        if (item.quantity == -1) {
          return userStorage.user.balance.ton >= item.shop_settings.shop_price_cost
        } else if (item.quantity-item.quantity_count == item.quantity) {
          return userStorage.user.balance.ton >= item.shop_settings.shop_price_cost
        } else if (item.quantity-item.quantity_count == 0) {
          return false
        } else {
          return userStorage.user.balance.ton >= item.shop_settings.shop_price_cost
        }
      }
    }

    const buyShopSkinStars = async (
      skin_id: string,
      type: string,
      amount: any,
      starsAmount: any
    ) => {
      const blockUpgrade = document.getElementById(`skinButton#${skin_id}`)
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
        invoice: randomId + '@' + 'shopSkin',
        isGift: true,

        giftAmount: type + '|' + amount,

        giftHasSkin: true,
        giftSkin: skin_id
      }

      let stars_data = await createStarsLink(
        userStorage.user.user_id,
        `Skin`,
        'Purchase for @PepsGameBot',
        parseInt(starsAmount),
        getImage(skin_id),
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

              showToast3.value = true
              setInterval(() => {
                showToast3.value = false
              }, 3650)

              await sendLogAdmin('donate', {
                user_id: userStorage.user.user_id,
                prize: `Покупка скина ${skin_id}`,
                amount: parseInt(starsAmount)
              })

              localStorage.setItem('skin_id', skin_id)

              setTimeout(() => {
                blockUpgrade.classList.remove('button_loading')
                blockUpgrade.classList.remove('disabled')
                blockUpgrade.classList.add('actived')
              }, 300)

              router.push('/')
            }
          }
        }, 1000)
      }
    }

    const buyShopSpecial = async (
      special_id: string,
      skin_id: string,
      type: string,
      amount: any,
      starsAmount: any
    ) => {
      const blockUpgrade = document.getElementById(`specialButton_${special_id}`)
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
        invoice: randomId + '@' + 'special',
        isGift: true,

        giftAmount: type + '|' + amount,

        giftHasSkin: true,
        giftSkin: skin_id[0]
      }

      let stars_data = await createStarsLink(
        userStorage.user.user_id,
        `Skin + ${formatNumber(amount)} ${type === 'money' ? '$PEPS' : type.charAt(0).toUpperCase() + type.slice(1)}`,
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
              starsBandleValue.value = amount

              if (type == 'views') userStorage.user.balance.views += amount
              if (type == 'money') userStorage.user.balance.earn += amount
              if (type == 'ton') userStorage.user.balance.ton += amount

              if (type == 'earn') {
                type = 'money'
              }

              let element = document.getElementById(`header_button_${type}_block`)
              element.classList.add('animate_add_money')
              setTimeout(() => element.classList.remove('animate_add_money'), 600)

              clearInterval(checkInvoiceInterval)

              showToast2.value = true
              setInterval(() => {
                showToast2.value = false
              }, 3650)

              await sendLogAdmin('donate', {
                user_id: userStorage.user.user_id,
                prize: `Специальная акция #${special_id}`,
                amount: parseInt(starsAmount)
              })

              await updateSpecials(
                userStorage.user.user_id, 
                special_id
              )

              userStorage.user.special_completed.push(special_id)

              const blockSpecial = document.getElementById('specialBlock_' + special_id)
              if (blockSpecial) blockSpecial.remove()

              localStorage.setItem('skin_id', skin_id)

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

    const buyShopBandle = async (type: string, amount: any, starsAmount: any) => {
      // const response = await shopBandles(userStorage.user.user_id, type, amount)

      const blockUpgrade = document.getElementById(`bandleButton#${amount}`)
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
        invoice: randomId + '@' + 'bandle',
        isGift: true,

        giftAmount: type + '|' + amount,

        giftHasSkin: false,
        giftSkin: 'none'
      }

      let stars_data

      const stars_config = [
        { maxAmount: 6000, label: '6,000 $PEPS', image: 'https://i.ibb.co/dK5gscs/1-4.png' },
        { maxAmount: 40000, label: '40,000 $PEPS', image: 'https://i.ibb.co/54J88wr/2-3.png' },
        { maxAmount: 80000, label: '80,000 $PEPS', image: 'https://i.ibb.co/dbmfzTK/3-3.png' },
        { maxAmount: 500000, label: '500,000 $PEPS', image: 'https://i.ibb.co/M9vf6S6/4-2.png' }
      ]

      const selectedConfig = stars_config.find((config) => amount <= config.maxAmount)

      if (selectedConfig) {
        stars_data = await createStarsLink(
          userStorage.user.user_id,
          selectedConfig.label,
          'Purchase for @PepsGameBot',
          parseInt(starsAmount),
          selectedConfig.image,
          JSON.stringify(stars_data_json)
        )
        console.log(stars_data)
      }

      if (stars_data.success) {
        telegramLink(stars_data.data['invoice_link'])

        // цикл проверки оплаты
        const checkInvoiceInterval = setInterval(async () => {
          const checkInvoice = await getInvoice(randomId)

          if (checkInvoice.success) {
            if (checkInvoice.invoice.invoice_status === 'paid') {
              starsBandleValue.value = amount
              userStorage.user.balance.earn += amount

              if (type == 'earn') {
                type = 'money'
              }

              let element = document.getElementById(`header_button_${type}_block`)
              element.classList.add('animate_add_money')
              setTimeout(() => element.classList.remove('animate_add_money'), 600)
              clearInterval(checkInvoiceInterval)

              showToast1.value = true
              setInterval(() => {
                showToast1.value = false
              }, 3650)

              await sendLogAdmin('donate', {
                user_id: userStorage.user.user_id,
                prize: `${amount} монет`,
                amount: parseInt(starsAmount)
              })

              setTimeout(() => {
                blockUpgrade.classList.remove('button_loading')
                blockUpgrade.classList.remove('disabled')
                blockUpgrade.classList.add('actived')
              }, 300)
            }
          }
        }, 2100)
      }
    }

    const getSpecials = async () => {
      const data = await getJsonDataSpecial()
      const specialsArray = Object.values(data)

      const currentTime = new Date()

      specialsItems.value = specialsArray.filter((item) => {
        const [startDate, startTime] = item.special_start_time.split(' ')
        const [dayStart, monthStart, yearStart] = startDate.split('-')
        const specialStart = new Date(`${'20' + yearStart}-${monthStart}-${dayStart}T${startTime}`)

        const [endDate, endTime] = item.special_end_time.split(' ')
        const [dayEnd, monthEnd, yearEnd] = endDate.split('-')
        const specialEnd = new Date(`${'20' + yearEnd}-${monthEnd}-${dayEnd}T${endTime}`)

        if (userStorage.user.special_completed.includes(item.special_id)) {
          return false
        } else {
          return currentTime >= specialStart && currentTime <= specialEnd
        }
      })

      if (userStorage.user.special_completed !== undefined) {
        return true
      } else {
        return false
      }
    }

    const specialsInterval = setInterval(async () => {
      const specials = await getSpecials()
      if (specials) {
        loaderStatusPageSpecials.value = false
        clearInterval(specialsInterval)
      }
    }, 400)

    const previewSkin = ref({
      status: false,
      item: null,
      skin_id: null,
      title: null,
      description: null,
      description_ru: null,
      rarity: null,
      price_type: null,
      price: null,
      quantity_count: null,
      quantity_need: null,
      language_user: null,
      baffs: null
    })

    const previewSkinOpen = (skin) => {
      const previewSkinBlock = document.getElementById(`previewSkin#${skin.skin_id}`)

      if (previewSkinBlock.classList.contains('clicked')) {
        return
      } else {
        previewSkinBlock.classList.add('clicked')
      }

      setTimeout(() => {
        previewSkinBlock.classList.remove('clicked')
      }, 210)

      previewSkin.value.item = skin
      previewSkin.value.skin_id = skin.skin_id
      previewSkin.value.title = skin.name
      previewSkin.value.description = skin.description
      previewSkin.value.description_ru = skin.description_ru
      previewSkin.value.rarity = skin.rare
      previewSkin.value.price_type = skin.shop_settings.shop_price_type
      previewSkin.value.price = skin.shop_settings.shop_price_cost
      previewSkin.value.quantity_count = skin.quantity-skin.quantity_count
      previewSkin.value.quantity_need = skin.quantity
      previewSkin.value.language_user = userDataSettings.value.language
      previewSkin.value.baffs = skin.baffs
      previewSkin.value.status = true
    }

    return {
      shopItems,
      getImage,
      getRare,
      formatNumber,
      buySkinShop,
      userStorage,
      loaderStatusPageSpecials,
      loaderStatusPage,
      checkBuyButton,
      buyShopBandle,
      showToast1,
      showToast2,
      showToast3,
      showToast4,
      starsBandleValue,
      buyShopSkinStars,
      buyShopSpecial,
      getSpecials,
      specialsItems,
      getImage,
      getSkinJson,
      startTimerSpecial,

      namePage,
      userDataSettings,
      localText,

      previewSkin,
      previewSkinOpen,

      __SHOP_STARS_BANDLES__,
      __SHOP_STARS_FRIENDS__
    }
  }
})
</script>

<template>
  <div id="toast_1" :class="showToast1 ? 'show' : ''" class="toast purchase">
    {{ localText['root'][userDataSettings.language].root_text_10 }}
    {{ formatNumber(starsBandleValue) }} $PEPS.
  </div>

  <div id="toast_2" :class="showToast2 ? 'show' : ''" class="toast purchase">
    {{ localText['root'][userDataSettings.language].root_text_11 }}
  </div>

  <div id="toast_3" :class="showToast3 ? 'show' : ''" class="toast purchase">
    {{ localText['root'][userDataSettings.language].root_text_12 }}
  </div>

  <div id="toast_4" :class="showToast4 ? 'show' : ''" class="toast purchase">
    {{ localText['root'][userDataSettings.language].root_text_17 }}
  </div>
  
  <Preview_ShopItem
    v-if="previewSkin.status == true"
    :status="previewSkin.status"
    :skin_id="previewSkin.skin_id"
    :title="previewSkin.title"
    :description="previewSkin.description"
    :description_ru="previewSkin.description_ru"
    :rarity="previewSkin.rarity"
    :price_type="previewSkin.price_type"
    :price="previewSkin.price"
    :quantity_count="previewSkin.quantity_count"
    :quantity_need="previewSkin.quantity_need"
    :language_user="previewSkin.language_user"
    :baffs_object="previewSkin.baffs"
    :baffs="getRare(previewSkin.language_user, previewSkin.baffs.baffs_buy_type, previewSkin.baffs.baffs_buy_percentage)"
    :localText="localText"
    :checkBuy="checkBuyButton(previewSkin.item)"
    @closeModal="previewSkin.status = false"
    @buySkin="
      previewSkin.item.shop_settings.shop_price_type === 'stars'
      ? buyShopSkinStars(
          previewSkin.item.skin_id,
          previewSkin.item.shop_settings.shop_price_type,
          0,
          previewSkin.item.shop_settings.shop_price_cost
        ) 
      : buySkinShop(previewSkin.item)
    "
  />

  <div class="shop">
    <div class="shop_inner">

      <div v-if="specialsItems.length !== 0" class="shop_section" id="grid_special_cd">
        <div class="shop_section_title skeleton text special_sp">
          <h4>{{ localText[namePage][userDataSettings.language].sh_text_1 }}</h4>
        </div>

        <div
          v-if="loaderStatusPageSpecials"
          style="margin: auto; text-align: center; align-items: center; padding: 60px 0px"
        >
          <div class="jumping-dots-loader"><span></span> <span></span> <span></span></div>
        </div>

        <div
          v-for="special in specialsItems"
          :key="special.special_id"
          :id="'specialBlock_' + special.special_id"
          class="shop_special skeleton block"
        >
          <div class="special_spanner upgrades_section_skins_item_left_info_title">
            <span :id="'special_time_' + special.special_id">{{
              startTimerSpecial('special_time_' + special.special_id, special.special_end_time)
            }}</span>
          </div>

          <div class="shop_special_head">
            <div
              :class="getSkinJson(special.special_skins[0]).rare"
              class="upgrades_section_skins_item_left_skin rare shop_section_skins_item_skin"
            >
              <div class="shop_section_skins_item_skin_inner">
                <img src="./../assets/img/upgrades_effect.png" alt="upgrades_effect" />
                <img :src="getImage(special.special_skins[0])" alt="skin" />
              </div>
              <p
                v-if="
                  getSkinJson(special.special_skins[0]).baffs.baffs_type == true &&
                  getSkinJson(special.special_skins[0]).baffs.baffs_buy_type == 'views'
                "
              >
                {{ localText['root'][userDataSettings.language].root_text_1 }} +{{
                  getSkinJson(special.special_skins[0]).baffs.baffs_buy_percentage
                }}%
              </p>
              <p
                v-if="
                  getSkinJson(special.special_skins[0]).baffs.baffs_type == true &&
                  getSkinJson(special.special_skins[0]).baffs.baffs_buy_type == 'money'
                "
              >
                {{ localText['root'][userDataSettings.language].root_text_2 }} +{{
                  getSkinJson(special.special_skins[0]).baffs.baffs_buy_percentage
                }}%
              </p>
              <p
                v-if="
                  getSkinJson(special.special_skins[0]).baffs.baffs_type == true &&
                  getSkinJson(special.special_skins[0]).baffs.baffs_buy_type == 'ton'
                "
              >
                {{ localText['root'][userDataSettings.language].root_text_4 }} +{{
                  getSkinJson(special.special_skins[0]).baffs.baffs_buy_percentage
                }}%
              </p>
            </div>

            <div class="shop_special_plus">
              <svg
                width="15"
                height="15"
                viewBox="0 0 15 15"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M7.5 1.375V13.625M1.375 7.5H13.625"
                  stroke="white"
                  stroke-width="1.75"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>

            <div class="shop_special_prize">
              <div class="upgrades_section_skins_item_right_upgrade_summary">
                <img
                  v-if="special.special_type_prize == 'views'"
                  src="./../assets/img/eye.svg"
                  alt="eye"
                />
                <img
                  v-if="special.special_type_prize == 'money'"
                  src="./../assets/img/money.svg"
                  alt="money"
                />
                <img
                  v-if="special.special_type_prize == 'ton'"
                  src="./../assets/img/diamond.svg"
                  alt="diamond"
                />
                <p>{{ special.special_prize }}</p>
              </div>
            </div>
          </div>

          <div
            @click="
              buyShopSpecial(
                special.special_id,
                special.special_skins,
                special.special_type_prize,
                special.special_prize,
                special.special_stars_amount
              )
            "
            :id="'specialButton_' + special.special_id"
            class="special_btn_qd shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
          >
            <button id="btn_special_">
              <div class="shop_section_buy_items_item_buy_button_info">
                <img
                  class="button_loading_img"
                  src="./../assets/img/button_loading.svg"
                  alt="loading"
                />
                <img src="./../assets/img/stars.svg" alt="buy" />
                <p>{{ special.special_stars_amount }}</p>
              </div>
            </button>
          </div>
        </div>
      </div>

      <div class="shop_section">
        <div class="shop_section_title skeleton text">
          <h4>{{ localText[namePage][userDataSettings.language].sh_text_2 }}</h4>
        </div>

        <div class="shop_section_buy_items">
          <div class="shop_section_buy_items_item skeleton block">
            <div class="shop_section_buy_items_item_inner">
              <div class="shop_section_buy_items_item_image">
                <img src="./../assets/img/upgrades_effect.png" alt="money" />
                <img src="./../assets/img/money.svg" alt="money" />
              </div>

              <div class="shop_section_buy_items_item_block_into">
                <div class="shop_section_buy_items_item_block">
                  <div class="shop_section_buy_items_item_sum">
                    <img src="./../assets/img/money.svg" alt="money" />
                    <p>{{ formatNumber(__SHOP_STARS_BANDLES__['1'].prizeAmount) }}</p>
                  </div>

                  <div
                    @click="
                      buyShopBandle(
                        'money',
                        __SHOP_STARS_BANDLES__['1'].prizeAmount,
                        __SHOP_STARS_BANDLES__['1'].starsAmount
                      )
                    "
                    :id="'bandleButton#' + __SHOP_STARS_BANDLES__['1'].prizeAmount"
                    class="shop_section_buy_items_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
                  >
                    <button id="bandle_1">
                      <div class="shop_section_buy_items_item_buy_button_info">
                        <img
                          class="button_loading_img"
                          src="./../assets/img/button_loading.svg"
                          alt="loading"
                        />
                        <img src="./../assets/img/stars.svg" alt="buy" />
                        <p>{{ __SHOP_STARS_BANDLES__['1'].starsAmount }}</p>
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="shop_section_buy_items_item skeleton block">
            <div class="shop_section_buy_items_item_inner">
              <div class="shop_section_buy_items_item_image">
                <img src="./../assets/img/upgrades_effect.png" alt="money" />
                <img src="./../assets/img/money_three.svg" alt="money" />
              </div>

              <div class="shop_section_buy_items_item_block_into">
                <div class="shop_section_buy_items_item_block">
                  <div class="shop_section_buy_items_item_sum">
                    <img src="./../assets/img/money.svg" alt="money" />
                    <p>{{ formatNumber(__SHOP_STARS_BANDLES__['2'].prizeAmount) }}</p>
                  </div>

                  <div
                    @click="
                      buyShopBandle(
                        'money',
                        __SHOP_STARS_BANDLES__['2'].prizeAmount,
                        __SHOP_STARS_BANDLES__['2'].starsAmount
                      )
                    "
                    :id="'bandleButton#' + __SHOP_STARS_BANDLES__['2'].prizeAmount"
                    class="shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
                  >
                    <button id="bandle_2">
                      <div class="shop_section_buy_items_item_buy_button_info">
                        <img
                          class="button_loading_img"
                          src="./../assets/img/button_loading.svg"
                          alt="loading"
                        />
                        <img src="./../assets/img/stars.svg" alt="buy" />
                        <p>{{ __SHOP_STARS_BANDLES__['2'].starsAmount }}</p>
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="shop_section_buy_items_item skeleton block">
            <div class="shop_section_buy_items_item_inner">
              <div class="shop_section_buy_items_item_image">
                <img src="./../assets/img/upgrades_effect.png" alt="money" />
                <img src="./../assets/img/money_center.svg" alt="money" />
              </div>

              <div class="shop_section_buy_items_item_block_into">
                <div class="shop_section_buy_items_item_block">
                  <div class="shop_section_buy_items_item_sum">
                    <img src="./../assets/img/money.svg" alt="money" />
                    <p>{{ formatNumber(__SHOP_STARS_BANDLES__['3'].prizeAmount) }}</p>
                  </div>

                  <div
                    @click="
                      buyShopBandle(
                        'money',
                        __SHOP_STARS_BANDLES__['3'].prizeAmount,
                        __SHOP_STARS_BANDLES__['3'].starsAmount
                      )
                    "
                    :id="'bandleButton#' + __SHOP_STARS_BANDLES__['3'].prizeAmount"
                    class="shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
                  >
                    <button id="bandle_3">
                      <div class="shop_section_buy_items_item_buy_button_info">
                        <img
                          class="button_loading_img"
                          src="./../assets/img/button_loading.svg"
                          alt="loading"
                        />
                        <img src="./../assets/img/stars.svg" alt="buy" />
                        <p>{{ __SHOP_STARS_BANDLES__['3'].starsAmount }}</p>
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="shop_section_buy_items_item skeleton block">
            <div class="shop_section_buy_items_item_inner">
              <div class="shop_section_buy_items_item_image">
                <img src="./../assets/img/upgrades_effect.png" alt="money" />
                <img src="./../assets/img/money_four.svg" alt="money" />
              </div>

              <div class="shop_section_buy_items_item_block_into">
                <div class="shop_section_buy_items_item_block">
                  <div class="shop_section_buy_items_item_sum">
                    <img src="./../assets/img/money.svg" alt="money" />
                    <p>{{ formatNumber(__SHOP_STARS_BANDLES__['4'].prizeAmount) }}</p>
                  </div>

                  <div
                    @click="
                      buyShopBandle(
                        'money',
                        __SHOP_STARS_BANDLES__['4'].prizeAmount,
                        __SHOP_STARS_BANDLES__['4'].starsAmount
                      )
                    "
                    :id="'bandleButton#' + __SHOP_STARS_BANDLES__['4'].prizeAmount"
                    class="shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
                  >
                    <button id="bandle_4">
                      <div class="shop_section_buy_items_item_buy_button_info">
                        <img
                          class="button_loading_img"
                          src="./../assets/img/button_loading.svg"
                          alt="loading"
                        />
                        <img src="./../assets/img/stars.svg" alt="buy" />
                        <p>{{ __SHOP_STARS_BANDLES__['4'].starsAmount }}</p>
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="shop_section">
        <div class="shop_section_title skeleton text">
          <h4>{{ localText[namePage][userDataSettings.language].sh_text_10 }}</h4>
        </div>

        <div class="shop_section_friends">
          <FR_ShopItem 
            :id="1"
            :photo="'/src/assets/img/shop_friend_1.png'"
            :title="localText[namePage][userDataSettings.language].sh_text_12"
            :description="localText[namePage][userDataSettings.language].sh_text_11"
            :prizeAmount="__SHOP_STARS_FRIENDS__['1'].prizeAmount"
            :starsPrice="__SHOP_STARS_FRIENDS__['1'].starsAmount"
            :userStorage="userStorage"
            :toast="showToast4"
            @update-toast="showToast4 = $event"
          />
          <FR_ShopItem 
            :id="2"
            :photo="'/src/assets/img/shop_friend_2.png'"
            :title="localText[namePage][userDataSettings.language].sh_text_14"
            :description="localText[namePage][userDataSettings.language].sh_text_13"
            :prizeAmount="__SHOP_STARS_FRIENDS__['2'].prizeAmount"
            :starsPrice="__SHOP_STARS_FRIENDS__['2'].starsAmount"
            :userStorage="userStorage"
            :toast="showToast4"
            @update-toast="showToast4 = $event"
          />
        </div>

      </div>

      <div class="shop_section">
        <div class="shop_section_title skeleton text">
          <h4>{{ localText[namePage][userDataSettings.language].sh_text_3 }}</h4>
        </div>

        <div
          v-if="loaderStatusPage"
          style="margin: auto; text-align: center; align-items: center; padding: 60px 0px"
        >
          <div class="jumping-dots-loader"><span></span> <span></span> <span></span></div>
        </div>

        <div class="shop_section_skins">
          <div
            v-for="item in shopItems"
            :id="['shop#' + item.skin_id]"
            class="shop_section_skins_item skeleton block"
          >
            <div
              @click="previewSkinOpen(item)"
              :id="['previewSkin#' + item.skin_id]"
              :class="[
                'upgrades_section_skins_item_left_skin',
                item.rare,
                'shop_section_skins_item_skin'
              ]"
            >
              <div class="shop_section_skins_item_skin_inner">
                <img src="./../assets/img/upgrades_effect.png" alt="upgrades_effect" />
                <img :src="getImage(item.skin_id)" alt="skin" />
              </div>
              <p v-if="item.baffs.baffs_type == false">
                {{ localText['root'][userDataSettings.language].root_text_6 }}
              </p>
              <p v-else>
                {{
                  getRare(
                    userDataSettings.language,
                    item.baffs.baffs_buy_type,
                    item.baffs.baffs_buy_percentage
                  )
                }}
              </p>
            </div>

            <div class="shop_skin_quantity">
              <div v-if="item.quantity > 0" class="shop_skin_quantity_inner">
                <p v-if="item.quantity-item.quantity_count == 0" style="text-transform: capitalize">{{ localText["root"][userDataSettings.language].root_text_16 }}</p>
                <p v-if="item.quantity-item.quantity_count != 0">{{ formatNumber(item.quantity-item.quantity_count) }}</p>
                <p v-if="item.quantity-item.quantity_count != 0">/</p>
                <p v-if="item.quantity-item.quantity_count != 0">{{ formatNumber(item.quantity) }}</p>
              </div>
              <div v-else class="shop_skin_quantity_inner_none">
                <p>∞</p>
              </div>
            </div>

            <div class="shop_section_skins_item_left_info">
              <div class="shop_section_skins_item_title">
                <h4>{{ item.name }}</h4>
              </div>
              <div
                style="max-width: 94%"
                class="shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn"
                :class="{
                  disabled: !checkBuyButton(item),
                  actived: checkBuyButton(item)
                }"
                :id="'skinButton#' + item.skin_id"
              >
                <button
                  @click="
                    item.shop_settings.shop_price_type === 'stars'
                      ? buyShopSkinStars(
                          item.skin_id,
                          item.shop_settings.shop_price_type,
                          0,
                          item.shop_settings.shop_price_cost
                        )
                      : buySkinShop(item)
                  "
                >
                  <div class="shop_section_buy_items_item_buy_button_info">
                    <img
                      class="button_loading_img"
                      src="./../assets/img/button_loading.svg"
                      alt="loading"
                    />
                    <img
                      v-if="item.shop_settings.shop_price_type == 'views'"
                      src="./../assets/img/eye.svg"
                      alt="buy"
                    />
                    <img
                      v-if="item.shop_settings.shop_price_type == 'money'"
                      src="./../assets/img/money.svg"
                      alt="buy"
                    />
                    <img
                      v-if="item.shop_settings.shop_price_type == 'stars'"
                      src="./../assets/img/stars.svg"
                      alt="buy"
                    />
                    <p>{{ formatNumber(item.shop_settings.shop_price_cost) }}</p>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '../assets/css/upgrades.css';
@import '../assets/css/profile.css';
@import '../assets/css/shop.css';
</style>
