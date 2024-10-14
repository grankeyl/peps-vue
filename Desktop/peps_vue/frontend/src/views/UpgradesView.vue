<script setup lang="ts">
import { ref, computed } from 'vue'
import { UserStorage } from '@/stores/userStore'
import { SkinsStorage } from '@/stores/skinsStore'
import {
  getFullStamina,
  updateFullStamina,
  getSkins,
  getTask,
  taskNextStep
} from '@/utils/apiRequest'
import { telegramLink } from '@/composables/useTelegramSetup'
import { getImage, formatNumber, getSkinInfo, generateRandomId } from '@/utils/funcs'
import {
  upgradeSkin,
  buy,
  buySkin,
  changeSkin,
  existsInvoice,
  createStarsLink,
  getInvoice,
  sendLogAdmin
} from '@/utils/apiRequest'
import { __FULLSTAMINA_SPEEDUP__ } from '@/utils/constants'
import { useRoute, useRouter } from 'vue-router'
import { TelegramStorage } from '@/stores/telegramStore'

import { localText } from '@/interface'
import { TELEGRAM_BOT } from '@/config'

import moment from 'moment'

import { reactive } from 'vue';
import EQ_UpgradeItem from "@/views/improves/EQ_UpgradeItem.vue";

const namePage = 'upgrades'
const userStorage = reactive(UserStorage())
const skinsStorage = SkinsStorage()
const telegramStorage = TelegramStorage()

const userDataSettings = computed(() => {
  const settings = userStorage.settings || {}
  return {
    ...settings,
    language: settings.language || telegramStorage.getUserLanguage() || 'en'
  }
})

const route = useRoute()
const router = useRouter()
const task = ref(null)
const responseGetTask = ref(false)

const showToast1 = ref(false)
const showToast2 = ref(false)

const upgradesSkins = ref([])
const upgradesEquipment = ref([])
const userSkins = ref([])
const loaderStatusPage = ref(true)

let interval_getTask = ''

function startTimer(targetDate: string) {
  const dateFormat = 'DD-MM-YY HH:mm:ss'
  const startDate = moment(targetDate, dateFormat).toDate()
  const endDate = new Date(startDate.getTime() + 24 * 60 * 60 * 1000)

  async function updateTimer() {
    const now = new Date()
    const timeRemaining = endDate.getTime() - now.getTime()

    if (timeRemaining <= 0) {
      clearInterval(timerInterval)
      const response = await updateFullStamina(userStorage.user.user_id)
      if (response.success) {
        userStorage.user.full_stamina = response.data
        userStorage.user.full_stamina_last_date = 'None'
      }
    } else {
      const hours = Math.floor((timeRemaining / (1000 * 60 * 60)) % 24)
        .toString()
        .padStart(2, '0')
      const minutes = Math.floor((timeRemaining / (1000 * 60)) % 60)
        .toString()
        .padStart(2, '0')
      const seconds = Math.floor((timeRemaining / 1000) % 60)
        .toString()
        .padStart(2, '0')
      document.getElementById('staminaTimer').textContent = `${hours}:${minutes}:${seconds}`
    }
  }

  const timerInterval = setInterval(updateTimer, 1000)
}

async function fullStamina() {
  if (!isTimer()) {
    const response = await getFullStamina(userStorage.user.user_id)

    let full_stamina_id_class = document.getElementById('full_stamina_id')
    full_stamina_id_class.classList.add('active')
    setTimeout(() => full_stamina_id_class.classList.remove('active'), 200)

    if (response.success) {
      userStorage.user.full_stamina--
      userStorage.costs.stamina_now = response.data
      router.push('/')
    }
  }
}

const fetchSkins = async () => {
  const response = await getSkins(userStorage.user.user_id)

  if (response.success) {
    if (response.skins.length !== 0) {
      clearInterval(interval)
      userSkins.value = response.skins

      response.skins.forEach((element) => {
        if (element.skin_upgrade.upgrades_show === true) {
          if (element.skin_upgrade.upgrades_category == 'equipment') {
            const isDuplicate = upgradesEquipment.value.some(
              (upgrade) => upgrade.skin_id === element.skin_id
            )
            if (!isDuplicate) upgradesEquipment.value.push(element)
          } else {
            if (element.skin_status === true) {
              const isDuplicate = upgradesSkins.value.some(
                (upgrade) => upgrade.skin_id === element.skin_id
              )
              if (!isDuplicate) upgradesSkins.value.push(element)
            }
          }
        }
      })
    }
  }
}

const interval = setInterval(async () => {
  await fetchSkins()
}, 400)

const sortList = (list) => {
  return list.sort((a, b) => a.skin_upgrade.upgrades_place - b.skin_upgrade.upgrades_place)
}

const getUpgradeLine = (value: string) => {
  loaderStatusPage.value = false
  return `width: ${value}%`
}

async function upgrade(skin: any) {
  const skinUpgradesCost = parseInt(skin.skin_upgrade.upgrades_cost)

  let redirectNewSkin = false
  let balance = 0

  if (skin.skin_upgrade.upgrades_cost_type == 'views') {
    balance = userStorage.user.balance.views
  } else if (skin.skin_upgrade.upgrades_cost_type == 'money') {
    balance = userStorage.user.balance.earn
  } else if (skin.skin_upgrade.upgrades_cost_type == 'ton') {
    balance = userStorage.user.balance.ton
  }

  if (skin.skin_upgrade.upgrades_cost_type !== 'stars') {
    if (balance < skin.skin_upgrade.upgrades_cost) {
      return
    }
  }
  
  const blockUpgrade = document.getElementById(`skin#${skin.skin_id}`)
  const blockUpgradeButtonSkinBlock = blockUpgrade.querySelector(
    '.upgrades_section_skins_item_right_upgrade_btn'
  )

  if (skin.skin_upgrade.upgrades_cost_type !== 'stars') {
    if (!blockUpgrade) return
  }

  if (skin.skin_upgrade.upgrades_cost_type !== 'stars') {
    if (blockUpgradeButtonSkinBlock.classList.contains('disabled')) return
  }

  if (skin.skin_upgrade.upgrades_level_step + 1 >= 10) {
    skin.skin_upgrade.upgrades_level_step = 1
    skin.skin_upgrade.upgrades_level = skin.skin_upgrade.upgrades_level + 1

    if (
      skin.skin_upgrade.upgrades_current_index + 1 <=
      skin.skin_upgrade.upgrades_paths.length - 1
    ) {
      skin.skin_upgrade.upgrades_current_index = skin.skin_upgrade.upgrades_current_index + 1
      skin.skin_upgrade.upgrades_active_path =
        skin.skin_upgrade.upgrades_paths[skin.skin_upgrade.upgrades_current_index]

      const response = await buySkin(
        userStorage.user.user_id,
        skin.skin_upgrade.upgrades_active_path
      )

      if (response.success) {
        const response_change_skin = await changeSkin(
          userStorage.user.user_id,
          skin.skin_upgrade.upgrades_active_path
        )
        redirectNewSkin = true
      }
    }

    const blockUpgradeLevelSkinBlock = blockUpgrade.querySelector(
      '.upgrades_section_skins_item_left_skin'
    )

    if (blockUpgradeLevelSkinBlock) {
      blockUpgradeLevelSkinBlock.classList.add('level_animation')
      setTimeout(() => {
        blockUpgradeLevelSkinBlock.classList.remove('level_animation')
      }, 300)
    }
  } else {
    skin.skin_upgrade.upgrades_level_step = skin.skin_upgrade.upgrades_level_step + 1
  }

  blockUpgradeButtonSkinBlock.classList.remove('actived')
  blockUpgradeButtonSkinBlock.classList.add('button_loading')
  blockUpgradeButtonSkinBlock.classList.add('disabled')

  const buyResponse = await buy(
    userStorage.user.user_id,
    skin.skin_upgrade.upgrades_cost_type,
    parseInt(skin.skin_upgrade.upgrades_cost)
  )

  if (buyResponse.success) {
    let profileBandles, baffsPercents, baffsAdding, percentValue

    if (skin.skin_upgrade.upgrades_cost_type == 'views') {
      userStorage.user.balance.views -= skinUpgradesCost
    } else if (skin.skin_upgrade.upgrades_cost_type == 'money') {
      userStorage.user.balance.earn -= skinUpgradesCost
    } else if (skin.skin_upgrade.upgrades_cost_type == 'ton') {
      userStorage.user.balance.ton -= skinUpgradesCost
    }

    if (skin.skin_baffs.baffs_buy_type == 'views') {
      profileBandles = userStorage.costs.views_costs
      baffsPercents = skin.skin_baffs.baffs_buy_percentage
      baffsAdding = skin.skin_baffs.baffs_adding_views
      percentValue = (profileBandles / 100) * baffsPercents

      skin.skin_baffs.baffs_adding_views = parseInt(baffsAdding) + parseInt(percentValue)
      userStorage.costs.views_costs =
        parseInt(userStorage.costs.views_costs) + parseInt(percentValue)
    } else if (skin.skin_baffs.baffs_buy_type == 'money') {
      profileBandles = userStorage.costs.money_costs
      baffsPercents = skin.skin_baffs.baffs_buy_percentage
      baffsAdding = skin.skin_baffs.baffs_adding_money
      percentValue = (profileBandles / 100) * baffsPercents

      skin.skin_baffs.baffs_adding_money = parseInt(baffsAdding) + parseInt(percentValue)
      userStorage.costs.money_costs =
        parseInt(userStorage.costs.money_costs) + parseInt(percentValue)
    } else if (skin.skin_baffs.baffs_buy_type == 'stamina') {
      profileBandles = userStorage.costs.stamina_costs
      baffsPercents = skin.skin_baffs.baffs_buy_percentage
      baffsAdding = skin.skin_baffs.baffs_adding_stamina
      percentValue = (profileBandles / 100) * baffsPercents

      skin.skin_baffs.baffs_adding_stamina = parseInt(baffsAdding) + parseInt(percentValue)
      userStorage.costs.stamina_costs =
        parseInt(userStorage.costs.stamina_costs) + parseInt(percentValue)
    }

    const response = await upgradeSkin(
      userStorage.user.user_id,
      skin.skin_id,
      JSON.stringify(skin.skin_upgrade),
      JSON.stringify(skin.skin_baffs)
    )

    if (response.success) {
      skin.skin_upgrade = response.upgrade

      blockUpgradeButtonSkinBlock.classList.remove('button_loading')
      blockUpgradeButtonSkinBlock.classList.remove('disabled')
      blockUpgradeButtonSkinBlock.classList.add('actived')
    }

    skin.skin_upgrade.upgrades_cost = skin.skin_upgrade.upgrades_cost * 1.21 + Math.random() * 0.42

    const upgradeSkinChecker = document.getElementById(`upgradeSkinChecker#${skin.skin_id}`)
    
    if (skin.skin_upgrade.upgrades_cost_type == 'views') {
      if (userStorage.user.balance.views < skin.skin_upgrade.upgrades_cost) {
        upgradeSkinChecker.classList.add('disabled')
      }
    } else if (skin.skin_upgrade.upgrades_cost_type == 'money') {
      if (userStorage.user.balance.earn < skin.skin_upgrade.upgrades_cost) {
        upgradeSkinChecker.classList.add('disabled')
      }
    } else if (skin.skin_upgrade.upgrades_cost_type == 'ton') {
      if (userStorage.user.balance.ton < skin.skin_upgrade.upgrades_cost) {
        upgradeSkinChecker.classList.add('disabled')
      }
    }

    if (redirectNewSkin) {
      if (responseGetTask) {
        if (task.value) {
          if (task.value.task_type == 'upgrade:skin') {
            await taskNextStep(task.value.id, userStorage.user.user_id)
            userStorage.user.tasks_progress[task.value.id].current_step =
              userStorage.user.tasks_progress[task.value.id].current_step + 1
          }
        }
      }

      localStorage.setItem('skin_id', skin.skin_upgrade.upgrades_active_path)
      router.push('/')
    }
  }
}

const upgradeSkinStars = async (skin: any, skin_id: string, starsAmount: any) => {
  const blockUpgrade = document.getElementById(`upgradeSkinButton#${skin_id}`)
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
    invoice: randomId + '@' + 'upgradeSkin',
    isGift: true,

    giftAmount: 'None' + '|' + 0,

    giftHasSkin: false,
    giftSkin: 'None'
  }

  let stars_data = await createStarsLink(
    userStorage.user.user_id,
    `Upgrade skin`,
    'Purchase for @PepsGameBot',
    parseInt(starsAmount),
    `http://${location.hostname}:${location.port}` + getImage(skin_id),
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
          await upgrade(skin)

          showToast2.value = true
          setInterval(() => {
            showToast2.value = false
          }, 3650)

          await sendLogAdmin('donate', {
            user_id: userStorage.user.user_id,
            prize: `Апгрейд скина ${skin_id}`,
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

const isTimer = () => {
  if (userStorage.user.full_stamina == 0) {
    return true
  } else {
    return false
  }
}

const isEnoughUpgrades = (type: string, amount: string) => {
  const parsedAmount = parseInt(amount);
  if (type == 'views') {
    return parsedAmount <= parseInt(userStorage.user.balance.views);
  } else if (type == 'money') {
    return parsedAmount <= parseInt(userStorage.user.balance.earn);
  } else if (type == 'ton') {
    return parsedAmount <= parseInt(userStorage.user.balance.ton);
  } else {
    return false;
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

function repostGame() {
  let text_lg = ''

  if (userStorage.settings.language === 'ru') {
    text_lg =
      '🐸 Лягушонок Пепе стал игрой! Прокачивай оборудование чтобы получить новые предметы и $PEPS. 🎁 Бери свою приветственную награду 2,500 $PEPS и лимитированный скин!'
  } else {
    text_lg =
      '🐸 Pepe the frog becomes a game! Upgrade your setup to get new items and $PEPS. 🎁 Claim your welcome gift, 2,500 $PEPS and limited skin'
  }

  const baseUrl = 'https://t.me/share/url?url='
  const appUrl = `https://t.me/${TELEGRAM_BOT}/app?startapp=${userStorage.user.referal_key}`
  const fullUrl = `${baseUrl}${encodeURIComponent(appUrl)}&text=${encodeURIComponent(text_lg)}`

  telegramLink(fullUrl)
}

const speedupStamina = async (type: string, amount: any, starsAmount: any) => {
  let randomId = generateRandomId()
  const checkInvoiceId = await existsInvoice(randomId)

  if (checkInvoiceId.exists) randomId = generateRandomId()

  const stars_data_json = {
    invoice: `${randomId}@speedupStamina`,
    isGift: true,
    giftAmount: `none`,
    giftHasSkin: false,
    giftSkin: 'none'
  }

  const selectedConfig = 'speedupStamina'

  if (selectedConfig) {
    const stars_data = await createStarsLink(
      userStorage.user.user_id,
      '3 Full Stamina',
      'Purchase for @PepsGameBot',
      parseInt(starsAmount),
      location.pathname.replace(/[^\/]+$/, '') + '../assets/img/energy.svg',
      JSON.stringify(stars_data_json)
    )

    if (stars_data.success) {
      telegramLink(stars_data.data['invoice_link'])

      const checkInvoiceInterval = setInterval(async () => {
        const checkInvoice = await getInvoice(randomId)

        if (checkInvoice.success && checkInvoice.invoice.invoice_status === 'paid') {
          userStorage.user.full_stamina = 3
          clearInterval(checkInvoiceInterval)
          showToast1.value = true
          setTimeout(() => (showToast1.value = false), 3650)

          await sendLogAdmin('donate', {
            user_id: userStorage.user.user_id,
            prize: `Ускорение стамины`,
            amount: parseInt(starsAmount)
          })
        }
      }, 2100)
    }
  }
}
</script>

<template>
  <div id="toast_1" :class="showToast1 ? 'show' : ''" class="toast purchase">
    {{ localText['root'][userDataSettings.language].root_text_8 }}
  </div>

  <div id="toast_2" :class="showToast2 ? 'show' : ''" class="toast purchase">
    {{ localText['root'][userDataSettings.language].root_text_9 }}
  </div>

  <div class="upgrades">
    <div class="upgrades_inner">
      <div class="upgrades_section">
        <div class="upgrades_section_title skeleton text">
          <h4>{{ localText[namePage][userDataSettings.language].up_text_1 }}</h4>
        </div>

        <div class="upgrades_section_content">
          <div class="upgrades_section_item skeleton block">
            <div class="upgrades_section_item_left">
              <h4>{{ localText[namePage][userDataSettings.language].up_text_2 }}</h4>
              <p>{{ localText[namePage][userDataSettings.language].up_text_3 }}</p>
            </div>
            <div class="upgrades_section_item_right">
              <img src="./../assets/img/diamond_white.svg" alt="diamond" />
            </div>
          </div>

          <div class="upgrades_section_item_fullstamina_content_block">
            <div
              v-if="userStorage.user.referals >= 0"
              @click="fullStamina"
              class="upgrades_section_item upgrades_section_item_fullstamina_content"
              id="full_stamina_id"
              :class="{ no_remaing: isTimer() == true }"
            >
              <div class="upgrades_section_item_left">
                <h4>{{ localText[namePage][userDataSettings.language].up_text_4 }}</h4>
                <p v-if="isTimer()" id="staminaTimer">
                  {{ startTimer(userStorage.user.full_stamina_last_date) }}
                  {{ localText[namePage][userDataSettings.language].up_text_16 }}
                </p>
                <p v-else>
                  {{ userStorage.user.full_stamina }}
                  {{ localText[namePage][userDataSettings.language].up_text_5 }}
                </p>
              </div>
              <div class="upgrades_section_item_right">
                <img src="./../assets/img/energy_big.svg" alt="diamond" />
              </div>
            </div>

            <div
              v-else
              @click="repostGame"
              class="upgrades_section_item upgrades_section_item_fullstamina_content"
              id="full_stamina_id"
              style="background: #1d2955 !important"
            >
              <div class="upgrades_section_item_left">
                <h4>{{ localText[namePage][userDataSettings.language].up_text_4 }}</h4>
                <p>{{ localText[namePage][userDataSettings.language].up_text_15 }}</p>
              </div>
              <div class="upgrades_section_item_right">
                <img src="./../assets/img/chevrone_earn.svg" alt="diamond" />
              </div>
            </div>

            <div
              v-if="isTimer() && userStorage.user.referals >= 0"
              @click="speedupStamina('earn', 0, __FULLSTAMINA_SPEEDUP__.starsAmount)"
              class="upgrades_section_item_fullstamina_speedup"
            >
              <p>{{ localText[namePage][userDataSettings.language].up_text_17 }}</p>
              <img src="./../assets/img/stars.svg" alt="stars" />
              <p>{{ __FULLSTAMINA_SPEEDUP__.starsAmount }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="upgradesEquipment.value !== 0" class="upgrades_section">
        <div class="upgrades_section_title skeleton text">
          <h4>{{ localText[namePage][userDataSettings.language].up_text_6 }}</h4>
        </div>

        <div
          v-if="loaderStatusPage"
          style="margin: auto; text-align: center; align-items: center; padding: 60px 0px"
        >
          <div class="jumping-dots-loader"><span></span> <span></span> <span></span></div>
        </div>

        <div class="upgrades_section_skins">
          <EQ_UpgradeItem
            v-for="skin in upgradesEquipment"
            :key="skin.skin_id"
            :skin="skin"
            :localText="localText"
            :userDataSettings="userDataSettings"
            :userStorage="userStorage"
            :namePage="namePage"
            :isEnoughUpgrades="isEnoughUpgrades"
            :repostGame="repostGame"
            :upgrade="upgrade"
            :getImage="getImage"
            :getSkinInfo="getSkinInfo"
            :formatNumber="formatNumber"
            :getUpgradeLine="getUpgradeLine"
          />
        </div>
      </div>

      <div v-if="upgradesSkins.value !== 0" class="upgrades_section">
        <div class="upgrades_section_title skeleton text">
          <h4>{{ localText[namePage][userDataSettings.language].up_text_14 }}</h4>
        </div>

        <div
          v-if="loaderStatusPage"
          style="margin: auto; text-align: center; align-items: center; padding: 60px 0px"
        >
          <div class="jumping-dots-loader"><span></span> <span></span> <span></span></div>
        </div>

        <div class="upgrades_section_skins">
          <div
            v-for="skin in upgradesSkins"
            :id="['skin#' + skin.skin_id]"
            class="upgrades_section_skins_item skeleton block"
          >
            <div class="upgrades_section_skins_item_left">
              <div :class="['upgrades_section_skins_item_left_skin', skin.skin_rare]">
                <img src="./../assets/img/upgrades_effect.png" alt="upgrades_effect" />
                <img :src="getImage(skin.skin_upgrade.upgrades_active_path)" alt="skin" />
                <p>
                  {{ skin.skin_upgrade.upgrades_level }}
                  {{ localText[namePage][userDataSettings.language].up_text_7 }}
                </p>
              </div>
              <div class="upgrades_section_skins_item_left_info">
                <div class="upgrades_section_skins_item_left_info_title">
                  <h4>{{ getSkinInfo(skin.skin_upgrade.upgrades_active_path).name }}</h4>
                </div>
                <div class="upgrades_section_skins_item_left_info_post_chance">
                  <p v-if="skin.skin_baffs.baffs_buy_type == 'views'">
                    {{ localText['root'][userDataSettings.language].root_text_1 }}
                  </p>
                  <p v-if="skin.skin_baffs.baffs_buy_type == 'money'">
                    {{ localText['root'][userDataSettings.language].root_text_2 }}
                  </p>
                  <p v-if="skin.skin_baffs.baffs_buy_type == 'stamina'">
                    {{ localText['root'][userDataSettings.language].root_text_3 }}
                  </p>
                  <p v-if="skin.skin_baffs.baffs_buy_type == 'ton'">
                    {{ localText['root'][userDataSettings.language].root_text_4 }}
                  </p>
                  <span>+{{ skin.skin_baffs.baffs_buy_percentage }}%</span>
                </div>
                <div class="upgrades_section_skins_item_left_border">
                  <div
                    class="upgrades_section_skins_item_left_border_line"
                    :style="getUpgradeLine(skin.skin_upgrade.upgrades_level_step * 10)"
                  ></div>
                </div>
              </div>
              <p class="upgrades_section_skins_item_left_border_gift_icon">🎁</p>
              <div class="upgrades_section_skins_item_right_upgrade">
                <div
                  @click="
                    skin.skin_upgrade.upgrades_cost_type === 'stars'
                      ? upgradeSkinStars(skin, skin.skin_id, skin.skin_upgrade.upgrades_cost)
                      : upgrade(skin)
                  "
                  class="upgrades_section_skins_item_right_upgrade_btn actived"
                  :class="{
                    disabled:
                      skin.skin_upgrade.upgrades_cost_type != 'stars' &&
                      !isEnoughUpgrades(
                        skin.skin_upgrade.upgrades_cost_type,
                        skin.skin_upgrade.upgrades_cost
                      ),
                    actived: isEnoughUpgrades(
                      skin.skin_upgrade.upgrades_cost_type,
                      skin.skin_upgrade.upgrades_cost
                    )
                  }"
                  :id="'upgradeSkinButton#' + skin.skin_id"
                >
                  <button
                    :class="{
                      upgrades_section_skins_item_right_upgrade_btn_stars:
                        skin.skin_upgrade.upgrades_cost_type == 'stars'
                    }"
                  >
                    <img
                      class="button_loading_img"
                      src="./../assets/img/button_loading.svg"
                      alt="loading"
                    />
                    <p>{{ localText[namePage][userDataSettings.language].up_text_12 }}</p>
                  </button>
                </div>
                <div class="upgrades_section_skins_item_right_upgrade_summary">
                  <img
                    v-if="skin.skin_upgrade.upgrades_cost_type == 'views'"
                    src="./../assets/img/eye.svg"
                    alt="views"
                  />
                  <img
                    v-if="skin.skin_upgrade.upgrades_cost_type == 'money'"
                    src="./../assets/img/money.svg"
                    alt="money"
                  />
                  <img
                    v-if="skin.skin_upgrade.upgrades_cost_type == 'ton'"
                    src="./../assets/img/ton.svg"
                    alt="ton"
                  />
                  <img
                    v-if="skin.skin_upgrade.upgrades_cost_type == 'stars'"
                    src="./../assets/img/stars.svg"
                    alt="stars"
                  />
                  <p>{{ formatNumber(skin.skin_upgrade.upgrades_cost) }}</p>
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
@import '../assets/css/upgrades.css';
@import '../assets/css/profile.css';
</style>

<style>
#full_stamina_id.no_remaing {
  background: #1d2955 !important;
}
</style>
