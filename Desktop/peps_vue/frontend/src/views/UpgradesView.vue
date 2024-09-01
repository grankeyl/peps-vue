<script setup lang="ts">
import { ref } from 'vue'
import { UserStorage } from '@/stores/userStore'
import { getFullStamina, updateFullStamina, getSkins } from '@/utils/apiRequest'
import { getImage } from '@/utils/funcs'
import { formatNumber } from '@/utils/funcs'
import { upgradeSkin, buy } from '@/utils/apiRequest'
import moment from 'moment'

const name = 'UpgradesView'
const userStorage = UserStorage()

const upgradesSkins = ref([])
const upgradesEquipment = ref([])
const userSkins = ref([])

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
      location.href = '/'
    }
  }
}

const fetchSkins = async () => {
  const response = await getSkins(userStorage.user.user_id)
  console.log(response)

  if (response.success) {
    if (response.skins.length !== 0) {
      clearInterval(interval)
      userSkins.value = response.skins

      response.skins.forEach((element) => {
        if (element.skin_upgrade.upgrades_show === true) {
          if (element.skin_upgrade.upgrades_category == 'equipment') {
            upgradesEquipment.value.push(element)
          } else {
            upgradesSkins.value.push(element)
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
  return `width: ${value}%`
}

async function upgrade(skin: any) {
  let balance = 0
  if (skin.skin_upgrade.upgrades_cost_type == 'views') {
    balance = userStorage.user.balance.views
  } else if (skin.skin_upgrade.upgrades_cost_type == 'money') {
    balance = userStorage.user.balance.earn
  } else if (skin.skin_upgrade.upgrades_cost_type == 'ton') {
    balance = userStorage.user.balance.ton
  }
  console.log(balance, skin.skin_upgrade.upgrades_cost)
  if (balance < skin.skin_upgrade.upgrades_cost) {
    return
  }

  const blockUpgrade = document.getElementById(`skin#${skin.skin_id}`)
  const blockUpgradeButtonSkinBlock = blockUpgrade.querySelector(
    '.upgrades_section_skins_item_right_upgrade_btn'
  )

  if (!blockUpgrade) return

  if (blockUpgradeButtonSkinBlock.classList.contains('disabled')) return

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

  skin.skin_upgrade.upgrades_cost = skin.skin_upgrade.upgrades_cost * 1.15 + Math.random() * 0.42

  blockUpgradeButtonSkinBlock.classList.remove('actived')
  blockUpgradeButtonSkinBlock.classList.add('button_loading')
  blockUpgradeButtonSkinBlock.classList.add('disabled')

  const buyResponse = await buy(
    userStorage.user.user_id,
    skin.skin_upgrade.upgrades_cost_type,
    parseInt(skin.skin_upgrade.upgrades_cost)
  )

  if (buyResponse.success) {
    const response = await upgradeSkin(
      userStorage.user.user_id,
      skin.skin_id,
      JSON.stringify(skin.skin_upgrade)
    )

    if (skin.skin_upgrade.upgrades_cost_type == 'views') {
      userStorage.user.balance.views = buyResponse.balance
    } else if (skin.skin_upgrade.upgrades_cost_type == 'money') {
      userStorage.user.balance.earn = buyResponse.balance
    } else if (skin.skin_upgrade.upgrades_cost_type == 'ton') {
      userStorage.user.balance.ton = buyResponse.balance
    }

    if (response.success) {
      skin.skin_upgrade = response.upgrade

      blockUpgradeButtonSkinBlock.classList.remove('button_loading')
      blockUpgradeButtonSkinBlock.classList.remove('disabled')
      blockUpgradeButtonSkinBlock.classList.add('actived')
    }
  }
}

const isTimer = () => {
  if (userStorage.user.full_stamina == 0) {
    return true
  } else {
    return false
  }
}
</script>

<template>
  <div class="upgrades">
    <div class="upgrades_inner">
      <div class="upgrades_section">
        <div class="upgrades_section_title skeleton text">
          <h4>Daily stuff</h4>
        </div>

        <div class="upgrades_section_content">
          <div class="upgrades_section_item skeleton block">
            <div class="upgrades_section_item_left">
              <h4>Booost!</h4>
              <p>Soon..</p>
            </div>
            <div class="upgrades_section_item_right">
              <img src="./../assets/img/diamond_white.svg" alt="diamond" />
            </div>
          </div>

          <div
            @click="fullStamina"
            class="upgrades_section_item"
            id="full_stamina_id"
            :class="{ no_remaing: isTimer() == true }"
          >
            <div class="upgrades_section_item_left">
              <h4>Full Stamina</h4>
              <p v-if="isTimer()" id="staminaTimer">
                {{ startTimer(userStorage.user.full_stamina_last_date) }}
                Loading..
              </p>
              <p v-else>{{ userStorage.user.full_stamina }} available</p>
            </div>
            <div class="upgrades_section_item_right">
              <img src="./../assets/img/energy_big.svg" alt="diamond" />
            </div>
          </div>
        </div>
      </div>

      <div v-if="upgradesEquipment.value !== 0" class="upgrades_section">
        <div class="upgrades_section_title skeleton text">
          <h4>Upgrades</h4>
        </div>

        <div class="upgrades_section_skins">
          <div
            v-for="skin in sortList(upgradesEquipment)"
            :id="['skin#' + skin.skin_id]"
            class="upgrades_section_skins_item skeleton block"
          >
            <div class="upgrades_section_skins_item_left">
              <div :class="['upgrades_section_skins_item_left_skin', skin.skin_rare]">
                <img src="./../assets/img/upgrades_effect.png" alt="upgrades_effect" />
                <img :src="getImage(skin.skin_upgrade.upgrades_active_path)" alt="skin" />
                <p>{{ skin.skin_upgrade.upgrades_level }} lvl</p>
              </div>
              <div class="upgrades_section_skins_item_left_info">
                <div class="upgrades_section_skins_item_left_info_title">
                  <h4>{{ skin.name }}</h4>
                </div>
                <div class="upgrades_section_skins_item_left_info_post_chance">
                  <p v-if="skin.skin_baffs.baffs_buy_type == 'views'">Views</p>
                  <p v-if="skin.skin_baffs.baffs_buy_type == 'money'">Earn</p>
                  <p v-if="skin.skin_baffs.baffs_buy_type == 'stamina'">Stamina</p>
                  <p v-if="skin.skin_baffs.baffs_buy_type == 'ton'">TON Earn</p>
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
                class="upgrades_section_skins_item_right_upgrade_btn"
                :class="{ 
                  disabled: skin.skin_upgrade.upgrades_cost > userStorage.user.balance.earn,
                  actived: skin.skin_upgrade.upgrades_cost <= userStorage.user.balance.earn
                }">
                  <button @click="upgrade(skin)">
                    <img
                      class="button_loading_img"
                      src="./../assets/img/button_loading.svg"
                      alt="loading"
                    />
                    <p>Upgrade</p>
                  </button>
                </div>
                <div class="upgrades_section_skins_item_right_upgrade_summary">
                  <img
                    v-if="skin.skin_upgrade.upgrades_cost_type == 'money'"
                    src="./../assets/img/money.svg"
                    alt="money"
                  />
                  <img
                    v-if="skin.skin_upgrade.upgrades_cost_type == 'views'"
                    src="./../assets/img/views.svg"
                    alt="money"
                  />
                  <p>{{ formatNumber(skin.skin_upgrade.upgrades_cost) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- <div v-if="upgradesSkins.value !== 0" class="upgrades_section">
        <div class="upgrades_section_title skeleton text">
          <h4>Skins</h4>
        </div>

        <div class="upgrades_section_skins">
          <div v-for="skin in upgradesSkins" class="upgrades_section_skins_item skeleton block">
            <div class="upgrades_section_skins_item_left">
              <div class="upgrades_section_skins_item_left_skin rare">
                <img src="./../assets/img/upgrades_effect.png" alt="upgrades_effect" />
                <img :src="getImage(skin.skin_id)" alt="skin" />
                <p>{{ skin.skin_upgrade.upgrades_level }} lvl</p>
              </div>
              <div class="upgrades_section_skins_item_left_info">
                <div class="upgrades_section_skins_item_left_info_title">
                  <h4>{{ skin.name }}</h4>
                </div>
                <div class="upgrades_section_skins_item_left_info_post_chance">
                  <p>Earn</p>
                  <span>+1%</span>
                </div>
                <div class="upgrades_section_skins_item_left_border">
                  <div
                    class="upgrades_section_skins_item_left_border_line"
                    style="width: 30%"
                  ></div>
                </div>
              </div>
              <p class="upgrades_section_skins_item_left_border_gift_icon">🎁</p>
              <div class="upgrades_section_skins_item_right_upgrade">
                <div class="upgrades_section_skins_item_right_upgrade_btn actived">
                  <button id="upgrade|">
                    <img
                      class="button_loading_img"
                      src="./../assets/img/button_loading.svg"
                      alt="loading"
                    />
                    <p>Upgrade</p>
                  </button>
                </div>
                <div class="upgrades_section_skins_item_right_upgrade_summary">
                  <img
                    v-if="skin.skin_upgrade.upgrades_cost_type == 'money'"
                    src="./../assets/img/money.svg"
                    alt="money"
                  />
                  <img
                    v-if="skin.skin_upgrade.upgrades_cost_type == 'views'"
                    src="./../assets/img/views.svg"
                    alt="money"
                  />
                  <p>{{ skin.skin_upgrade.upgrades_cost }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div> -->
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
