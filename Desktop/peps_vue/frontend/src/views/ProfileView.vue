<script lang="ts">
import { UserStorage } from '@/stores/userStore'
import { defineComponent, computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { TelegramStorage } from '@/stores/telegramStore'
import { buy, updateChances, setSettings, getSkins } from '@/utils/apiRequest'
import { formatNumber, getImage, getRare } from '@/utils/funcs'

import SettingsTooltip from '@/components/tooltips/settings.vue'
export default defineComponent({
  components: {
    SettingsTooltip
  },
  setup() {
    const telegramStorage = TelegramStorage()
    const useUserStore = UserStorage()

    const isShowSettings = ref(false)

    const userData = computed(() => useUserStore.user || {})
    const userCosts = computed(() => useUserStore.costs || {})
    const userSettings = computed(() => useUserStore.settings || {})
    const userSkins = ref([])
    const categories = ref([])
    const isTooltipActive = ref(false)
    const isButtonDisabled = ref(false)
    const isButtonLoading = ref(false)
    const settingsButton = ref<HTMLButtonElement | null>(null)
    const settingsTooltip = ref<HTMLElement | null>(null)

    const oldTapAnimation = ref(false)
    const oldLanguage = ref('en')

    const categorySkins = ref([])
    const activeCategory = ref('Wear')

    const toggleTooltipSettings = (event: MouseEvent) => {
      document.querySelector('.settings_tooltip')?.classList.toggle('active')
      event.stopPropagation()
    }

    const profilePostChanceSummary = () => {
      const summary =
        parseInt(userCosts.value.views_chance) + parseInt(userCosts.value.money_chance)
      return summary
    }

    const profileAfkPostChanceSummary = () => {
      const summary =
        parseInt(userCosts.value.auto_views_chance) + parseInt(userCosts.value.auto_money_chance)
      return summary
    }

    const UpgradePost = async (type: 'Default' | 'Afk') => {
      let chance_views
      let chance_money
      let profile_post_cost

      if (type === 'Default') {
        chance_views = userCosts.value.views_chance
        chance_money = userCosts.value.money_chance
        profile_post_cost = userCosts.value.profile_post_cost
      } else if (type === 'Afk') {
        chance_views = userCosts.value.auto_views_chance
        chance_money = userCosts.value.auto_money_chance
        profile_post_cost = userCosts.value.profile_afk_cost
      }

      if (userData.value.balance.views < profile_post_cost) {
        return
      }

      if (isButtonDisabled.value) return

      isButtonDisabled.value = true
      isButtonLoading.value = true

      const views_chance_costs = parseInt(chance_views)
      const money_chance_costs = parseInt(chance_money)

      if (type === 'Default') {
        if (views_chance_costs + 5 >= 50) {
          chance_views = 50
        } else {
          chance_views = chance_views + 5
        }

        if (money_chance_costs + 5 >= 50) {
          chance_money = 50
        } else {
          chance_money = chance_money + 5
        }
      } else if (type === 'Afk') {
        if (views_chance_costs + money_chance_costs >= 100) {
          chance_views = 50
          chance_money = 50
        } else {
          chance_views = chance_views + 5
          chance_money = chance_money + 5
        }
      }

      const buyResult = await buyItem('views', profile_post_cost)
      profile_post_cost = (profile_post_cost * 1.3 + Math.random() * 0.7).toFixed(0)

      const result = await updateChances(
        userData.value.user_id,
        chance_views,
        chance_money,
        profile_post_cost,
        type
      )

      if (result.success) {
        if (type === 'Default') {
          userCosts.value.views_chance = result.views_chance
          userCosts.value.money_chance = result.money_chance
          userCosts.value.profile_post_cost = profile_post_cost
        } else if (type === 'Afk') {
          userCosts.value.auto_views_chance = result.views_chance
          userCosts.value.auto_money_chance = result.money_chance
          userCosts.value.profile_afk_cost = profile_post_cost
        }
      }

      if (chance_views + chance_money >= 100) {
        location.reload()
      }

      if (money_chance_costs + views_chance_costs == 100) {
        // забудь нахуй
      } else {
        const lineUpgradePost = document.querySelector(
          `#post_chance_upgrade_profile_line_${type}`
        ) as HTMLElement
        const totalCost = views_chance_costs + money_chance_costs + 10
        lineUpgradePost.style.width = totalCost + '%'
      }

      if (!isMax(type)) {
        setTimeout(() => {
          if (!isEnough(profile_post_cost)) {
            isButtonLoading.value = false
            isButtonDisabled.value = true
          } else {
            isButtonLoading.value = false
            isButtonDisabled.value = false
          }
        }, 300)
      }
    }

    const isEnough = (amount: number) => {
      if (
        userData.value &&
        userData.value.balance &&
        typeof userData.value.balance.views !== 'undefined'
      ) {
        return userData.value.balance.views >= amount
      } else {
        return false
      }
    }

    const buyItem = async (type: string, amount: number) => {
      if (isEnough(amount)) {
        const response = await buy(userData.value.user_id, type, amount)

        if (response.success) {
          if (type === 'views') {
            userData.value.balance.views = response.balance
          } else if (type === 'money') {
            userData.value.balance.earn = response.balance
          } else {
            userData.value.balance.ton = response.balance
          }
          return true
        } else {
          return false
        }
      }
    }

    const isMax = (type: 'Default' | 'Afk') => {
      let views_chance
      let money_chance

      if (type === 'Default') {
        views_chance = userCosts.value.views_chance
        money_chance = userCosts.value.money_chance
      } else if (type === 'Afk') {
        views_chance = userCosts.value.auto_views_chance
        money_chance = userCosts.value.auto_money_chance
      }

      return views_chance + money_chance === 100
    }

    const showSettings = () => {
      return isShowSettings.value
    }

    const toggleSettings = async () => {
      isShowSettings.value = !isShowSettings.value
    }

    const fetchSkins = async () => {
      const response = await getSkins(userData.value.user_id)
      if (response.success) {
        if (response.skins.length !== 0) {
          userSkins.value = response.skins
          categories.value = response.categories
          setActiveCategory('Wear')
          clearInterval(interval)
          return true
        } else {
          return false
        }
      } else {
        return false
      }
    }

    const interval = setInterval(async () => {
      await fetchSkins()
    }, 400)

    const setActiveCategory = (category: string) => {
      categorySkins.value = []
      filterSkins(category)
      activeCategory.value = category
    }

    const filterSkins = (category) => {
      userSkins.value.forEach((element) => {
        if (element.skin_category === category.toLowerCase() && element.profile_show) {
          categorySkins.value.push(element)
        }
      })
    }

    return {
      userData,
      userCosts,
      profilePostChanceSummary,
      profileAfkPostChanceSummary,
      UpgradePost,
      isEnough,
      isMax,
      formatNumber,
      toggleTooltipSettings,
      settingsTooltip,
      toggleTooltipSettings,
      isShowSettings,
      showSettings,
      toggleSettings,
      categories,
      activeCategory,
      setActiveCategory,
      userSkins,
      getImage,
      getRare,
      categorySkins
    }
  }
})
</script>

<template>
  <div class="profile">
    <div class="profile_inner">
      <SettingsTooltip :show="showSettings()" :langActive="true" />

      <div class="profile_user" style="position: relative">
        <div class="profile_user_head">
          <div class="profile_user_head_avatar skeleton rounded">
            <img src="./../assets/img/default_avatar.png" alt="" />
          </div>
          <div @click="toggleSettings" class="profile_user_head_settings skeleton rounded">
            <svg
              width="18"
              height="18"
              viewBox="0 0 18 18"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g clip-path="url(#clip0_585_705)">
                <path
                  d="M6.72401 2.89307L7.27687 1.46592C7.3701 1.22429 7.53414 1.01645 7.7475 0.869625C7.96086 0.722799 8.21358 0.643831 8.47258 0.643066H9.52687C9.78586 0.643831 10.0386 0.722799 10.2519 0.869625C10.4653 1.01645 10.6293 1.22429 10.7226 1.46592L11.2754 2.89307L13.1526 3.97307L14.6697 3.74164C14.9223 3.70735 15.1795 3.74893 15.4084 3.86111C15.6373 3.97329 15.8277 4.15099 15.9554 4.37164L16.4697 5.27164C16.6015 5.4958 16.6622 5.75465 16.6439 6.01404C16.6255 6.27342 16.5289 6.52113 16.3669 6.72449L15.4283 7.92021V10.0802L16.3926 11.2759C16.5546 11.4793 16.6512 11.727 16.6696 11.9864C16.6879 12.2458 16.6272 12.5046 16.4954 12.7288L15.9812 13.6288C15.8535 13.8494 15.663 14.0271 15.4341 14.1393C15.2052 14.2515 14.9481 14.2931 14.6954 14.2588L13.1783 14.0274L11.3012 15.1074L10.7483 16.5345C10.6551 16.7761 10.491 16.984 10.2777 17.1308C10.0643 17.2776 9.81158 17.3566 9.55258 17.3574H8.47258C8.21358 17.3566 7.96086 17.2776 7.7475 17.1308C7.53414 16.984 7.3701 16.7761 7.27687 16.5345L6.72401 15.1074L4.84687 14.0274L3.32972 14.2588C3.0771 14.2931 2.81999 14.2515 2.59106 14.1393C2.36213 14.0271 2.17171 13.8494 2.04401 13.6288L1.52972 12.7288C1.39794 12.5046 1.33722 12.2458 1.35559 11.9864C1.37395 11.727 1.47053 11.4793 1.63258 11.2759L2.57115 10.0802V7.92021L1.60687 6.72449C1.44481 6.52113 1.34823 6.27342 1.32987 6.01404C1.31151 5.75465 1.37222 5.4958 1.50401 5.27164L2.01829 4.37164C2.146 4.15099 2.33641 3.97329 2.56534 3.86111C2.79427 3.74893 3.05139 3.70735 3.30401 3.74164L4.82115 3.97307L6.72401 2.89307ZM6.42829 9.00021C6.42829 9.50879 6.57911 10.0059 6.86166 10.4288C7.14421 10.8517 7.54581 11.1813 8.01568 11.3759C8.48555 11.5705 9.00258 11.6214 9.50138 11.5222C10.0002 11.423 10.4584 11.1781 10.818 10.8185C11.1776 10.4589 11.4225 10.0007 11.5217 9.50187C11.621 9.00306 11.57 8.48603 11.3754 8.01617C11.1808 7.5463 10.8512 7.1447 10.4283 6.86214C10.0055 6.57959 9.5083 6.42878 8.99972 6.42878C8.31774 6.42878 7.66368 6.6997 7.18145 7.18193C6.69921 7.66417 6.42829 8.31822 6.42829 9.00021V9.00021Z"
                  stroke="white"
                  stroke-width="1.63636"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </g>
              <defs>
                <clipPath id="clip0_585_705">
                  <rect width="18" height="18" fill="white" />
                </clipPath>
              </defs>
            </svg>
          </div>
        </div>

        <div class="profile_user_name">
          <p class="profile_user_name_grip">{{ userData.full_name }}</p>
          <span>{{ userData.level }} lvl</span>
        </div>
      </div>

      <div class="profile_bands">
        <div class="profile_band">
          <img style="object-fit: contain;" src="./../assets/img/eye.svg" alt="" />
          <p>{{ userCosts.views_costs }}</p>
        </div>
        <div class="profile_band">
          <img style="object-fit: contain;" src="./../assets/img/money.svg" alt="" />
          <p>{{ userCosts.money_costs }}</p>
        </div>
        <div class="profile_band" style="display: none">
          <h4>Rank</h4>
          <p><b>#</b><small>100</small></p>
        </div>
        <div class="profile_band">
          <img style="object-fit: contain;" src="./../assets/img/energy.svg" alt="" />
          <p>{{ userCosts.stamina_costs }}</p>
        </div>
      </div>

      <div class="profile_connect_wallet">
        <div class="profile_connect_wallet_button">
          <button class="profile_connect_wallet_button_button" onclick="showToast_1()">
            <div class="profile_connect_wallet_button_button_center">
              <img src="./../assets/img/diamond_connect_wallet.svg" alt="" />
              <p>Connect wallet</p>
            </div>
          </button>
        </div>
      </div>

      <div class="profile_autoting">
        <div class="earn_limited_task upgrades_section_skins_item profile_section_skins_item">
          <div class="upgrades_section_skins_item_left">
            <div class="upgrades_section_skins_item_left_info">
              <div class="upgrades_section_skins_item_left_info_title">
                <h4 style="max-width: 147px">Post chance</h4>
                <div class="upgrades_section_skins_item_left_info_post_chance">
                  <span>+10%</span>
                </div>
              </div>
              <div class="upgrades_section_skins_item_left_border_text_bottom_abs">
                <div class="upgrades_section_skins_item_left_border_text">
                  <p id="post_chance_upgrade_profile_percents">{{ profilePostChanceSummary() }}%</p>
                </div>
                <div class="upgrades_section_skins_item_left_border">
                  <div
                    id="post_chance_upgrade_profile_line_Default"
                    :style="{ width: profilePostChanceSummary() + '%' }"
                    class="upgrades_section_skins_item_left_border_line"
                  ></div>
                </div>
              </div>
            </div>

            <div class="upgrades_section_skins_item_right_upgrade">
              <div
                @click="UpgradePost('Default')"
                id="UpgradePostDefault"
                class="upgrades_section_skins_item_right_upgrade_btn upgrades_section_skins_item_right_upgrade_btn_profile_post_chance"
                :class="{
                  actived: isEnough(userCosts.profile_post_cost),
                  disabled: !isEnough(userCosts.profile_post_cost) || isMax('Default')
                }"
              >
                <button style="width: 85px" id="post_chance_upgrade_profile">
                  <div class="shop_section_buy_items_item_buy_button_info">
                    <img
                      class="button_loading_img"
                      src="./../assets/img/button_loading.svg"
                      alt="loading"
                    />
                    <p v-if="!isMax('Default')">Upgrade</p>
                    <p v-else>Max level</p>
                  </div>
                </button>
              </div>

              <div
                id="post_chance_upgrade_profile_text_summary"
                class="upgrades_section_skins_item_right_upgrade_summary upgrades_section_skins_item_right_upgrade_summary_profile"
              >
                <img v-if="!isMax('Default')" src="./../assets/img/eye.svg" alt="eye" />
                <p v-if="!isMax('Default')" id="post_chance_upgrade_profile_text">
                  {{ formatNumber(userCosts.profile_post_cost) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="earn_limited_task upgrades_section_skins_item profile_section_skins_item">
          <div class="upgrades_section_skins_item_left">
            <div class="upgrades_section_skins_item_left_info">
              <div class="upgrades_section_skins_item_left_info_title">
                <h4 style="max-width: 147px">AFK post chance</h4>
                <div class="upgrades_section_skins_item_left_info_post_chance">
                  <span>+10%</span>
                </div>
              </div>
              <div class="upgrades_section_skins_item_left_border_text_bottom_abs">
                <div class="upgrades_section_skins_item_left_border_text">
                  <p id="afk_post_chance_upgrade_profile_percents">
                    {{ profileAfkPostChanceSummary() }}%
                  </p>
                </div>
                <div class="upgrades_section_skins_item_left_border">
                  <div
                    id="post_chance_upgrade_profile_line_Afk"
                    :style="{ width: profileAfkPostChanceSummary() + '%' }"
                    class="upgrades_section_skins_item_left_border_line"
                  ></div>
                </div>
              </div>
            </div>

            <div class="upgrades_section_skins_item_right_upgrade">
              <div
                @click="UpgradePost('Afk')"
                id="UpgradePostAfk"
                class="upgrades_section_skins_item_right_upgrade_btn upgrades_section_skins_item_right_upgrade_btn_profile_post_chance"
                :class="{
                  actived: isEnough(userCosts.profile_afk_cost),
                  disabled: !isEnough(userCosts.profile_afk_cost) || isMax('Afk')
                }"
              >
                <button style="width: 85px" id="afk_post_chance_upgrade_profile">
                  <div class="shop_section_buy_items_item_buy_button_info">
                    <img
                      class="button_loading_img"
                      src="./../assets/img/button_loading.svg"
                      alt="loading"
                    />
                    <p v-if="!isMax('Afk')">Upgrade</p>
                    <p v-else>Max level</p>
                  </div>
                </button>
              </div>
              <div
                id="afk_post_chance_upgrade_profile_text_summary"
                class="upgrades_section_skins_item_right_upgrade_summary upgrades_section_skins_item_right_upgrade_summary_profile"
              >
                <img v-if="!isMax('Afk')" src="./../assets/img/eye.svg" alt="eye" />
                <p v-if="!isMax('Afk')" id="post_chance_upgrade_profile_text">
                  {{ formatNumber(userCosts.profile_afk_cost) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="profile_c">
        <div class="upgrades_section_title">
          <h4>Skins</h4>
        </div>

        <div class="profile_categories">
          <div
            v-for="category in categories"
            @click="setActiveCategory(category)"
            :class="['profile_category', category === activeCategory ? 'active' : '']"
          >
            <p>{{ category }}</p>
          </div>
        </div>

        <div class="shop_section_skins">
          <div class="shop_section_category active">
            <div v-for="skin in categorySkins" :key="skin.id" class="shop_section_skins_item">
              <div
                :class="[
                  'upgrades_section_skins_item_left_skin',
                  skin.skin_rare,
                  'shop_section_skins_item_skin'
                ]"
              >
                <div class="shop_section_skins_item_skin_inner">
                  <img src="./../assets/img/upgrades_effect.png" alt="upgrades_effect" />
                  <img :src="getImage(skin.skin_id)" alt="skin" />
                </div>
                <p v-if="skin.skin_baffs.baffs_type == false">Basic</p>
                <p v-else>
                  {{
                    getRare(skin.skin_baffs.baffs_buy_type, skin.skin_baffs.baffs_buy_percentage)
                  }}
                </p>
              </div>
              <div class="shop_section_skins_item_left_info">
                <div class="shop_section_skins_item_title">
                  <h4>{{ skin.name }}</h4>
                </div>

                <div
                  v-if="skin.skin_status == false"
                  class="shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
                >
                  <button style="width: 95%; margin-bottom: 0; height: 37px" id="profile_putting|">
                    <div class="shop_section_buy_items_item_buy_button_info">
                      <img
                        class="button_loading_img"
                        src="./../assets/img/button_loading.svg"
                        alt="loading"
                      />
                      <p>Put on</p>
                    </div>
                  </button>
                </div>

                <div
                  v-if="skin.skin_status == true"
                  class="shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn disabled"
                >
                  <button style="width: 95%; margin-bottom: 0; height: 37px" id="profile_putting|">
                    <div class="shop_section_buy_items_item_buy_button_info">
                      <img
                        class="button_loading_img"
                        src="./../assets/img/button_loading.svg"
                        alt="loading"
                      />
                      <p>Enabled</p>
                    </div>
                  </button>
                </div>
              </div>
            </div>

            <div v-if="categorySkins == null || categorySkins.length === 0">
              <div class="no_items_message">
                <div class="shop_section_buy_items_item_buy shop_section_skins_item_buy disabled">
                  <button>
                    <div class="shop_section_buy_items_item_buy_button_info">
                      <p>Skins not found!</p>
                    </div>
                  </button>
                </div>
                <div class="shop_section_buy_items_item_buy shop_section_skins_item_buy actived">
                  <button id="go_to_shop">
                    <div class="shop_section_buy_items_item_buy_button_info">
                      <p>Go to shop</p>
                    </div>
                  </button>
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
@import '../assets/css/profile.css';
@import '../assets/css/upgrades.css';
@import '../assets/css/shop.css';
</style>
