<script lang="ts">
import { defineComponent, ref } from 'vue'
import { LoadingStorage } from '@/stores/loadingStorage'
import { getShopItems, buySkin } from '@/utils/apiRequest'
import { formatNumber } from '@/utils/funcs'
import { UserStorage } from '@/stores/userStore'

export default defineComponent({
  setup() {
    const shopItems = ref([])
    const useLoadingStore = LoadingStorage()
    const userStorage = UserStorage()

    useLoadingStore.start()

    const fetchItems = async () => {
      const response = await getShopItems()

      if (response.success) {
        shopItems.value = response.items
      }
    }

    fetchItems()
    useLoadingStore.isLoading = false

    function getImage(skin_id: string) {
      return './src/assets/skins/' + skin_id + '.png'
    }

    function getRare(type: string, amount: string) {
      if (type == 'views') {
        return 'Views +' + amount + '%'
      } else if (type == 'money') {
        return 'Earn +' + amount + '%'
      } else if (type == 'ton') {
        return 'TON Earn +' + amount + '%'
      } else if (type == 'stamina') {
        return 'Stamina +' + amount + '%'
      }
    }

    async function buySkinShop(item) {
      const buttonBlock = document.getElementById(`shop#${item.skin_id}`)

      if (!buttonBlock) return

      const buttonUnsafe = buttonBlock.querySelector('.upgrades_section_skins_item_right_upgrade_btn')
      
      if (buttonUnsafe.classList.contains('disabled')) return

      buttonUnsafe.classList.remove('actived')
      buttonUnsafe.classList.add('button_loading')
      buttonUnsafe.classList.add('disabled')

      const response = await buySkin(userStorage.user.user_id, item.skin_id)

      if (response.success) {
        buttonUnsafe.classList.remove('button_loading')
        buttonUnsafe.classList.remove('disabled')
        buttonUnsafe.classList.add('actived')

        location.href = '/'
      }
    }

    return {
      shopItems,
      getImage,
      getRare,
      formatNumber,
      buySkinShop,
      userStorage
    }
  }
})
</script>

<template>
  <div class="shop">
    <div class="shop_inner">
      <div class="shop_section" id="grid_special_cd">
        <div class="shop_section_title skeleton text special_sp">
          <h4>Special</h4>
          <div class="special_spanner upgrades_section_skins_item_left_info_title">
            <span id="special_time">6d 2h</span>
          </div>
        </div>

        <div class="shop_special skeleton block">
          <div class="shop_special_head">
            <div class="upgrades_section_skins_item_left_skin rare shop_section_skins_item_skin">
              <div class="shop_section_skins_item_skin_inner">
                <img src="./../assets/img/upgrades_effect.png" alt="upgrades_effect" />
                <img src="./../assets/skins/cap_5.png" alt="skin" />
              </div>
              <p>Views +5%</p>
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
                <img src="./../assets/img/eye.svg" alt="eye" />
                <p>5000</p>
              </div>
            </div>
          </div>

          <div
            class="shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
          >
            <button id="btn_special_">
              <div class="shop_section_buy_items_item_buy_button_info">
                <img
                  class="button_loading_img"
                  src="./../assets/img/button_loading.svg"
                  alt="loading"
                />
                <img src="./../assets/img/stars.svg" alt="buy" />
                <p>500</p>
              </div>
            </button>
          </div>
        </div>
      </div>

      <div class="shop_section">
        <div class="shop_section_title skeleton text">
          <h4>$PEPS</h4>
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
                    <p>5000</p>
                  </div>

                  <div
                    class="shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
                  >
                    <button id="bandle_1">
                      <div class="shop_section_buy_items_item_buy_button_info">
                        <img
                          class="button_loading_img"
                          src="./../assets/img/button_loading.svg"
                          alt="loading"
                        />
                        <img src="./../assets/img/stars.svg" alt="buy" />
                        <p>100</p>
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
                <img src="./../assets/img/money.svg" alt="money" />
              </div>

              <div class="shop_section_buy_items_item_block_into">
                <div class="shop_section_buy_items_item_block">
                  <div class="shop_section_buy_items_item_sum">
                    <img src="./../assets/img/money.svg" alt="money" />
                    <p>5000</p>
                  </div>

                  <div
                    class="shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
                  >
                    <button id="bandle_1">
                      <div class="shop_section_buy_items_item_buy_button_info">
                        <img
                          class="button_loading_img"
                          src="./../assets/img/button_loading.svg"
                          alt="loading"
                        />
                        <img src="./../assets/img/stars.svg" alt="buy" />
                        <p>100</p>
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
                <img src="./../assets/img/money.svg" alt="money" />
              </div>

              <div class="shop_section_buy_items_item_block_into">
                <div class="shop_section_buy_items_item_block">
                  <div class="shop_section_buy_items_item_sum">
                    <img src="./../assets/img/money.svg" alt="money" />
                    <p>5000</p>
                  </div>

                  <div
                    class="shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
                  >
                    <button id="bandle_1">
                      <div class="shop_section_buy_items_item_buy_button_info">
                        <img
                          class="button_loading_img"
                          src="./../assets/img/button_loading.svg"
                          alt="loading"
                        />
                        <img src="./../assets/img/stars.svg" alt="buy" />
                        <p>100</p>
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
                <img src="./../assets/img/money.svg" alt="money" />
              </div>

              <div class="shop_section_buy_items_item_block_into">
                <div class="shop_section_buy_items_item_block">
                  <div class="shop_section_buy_items_item_sum">
                    <img src="./../assets/img/money.svg" alt="money" />
                    <p>5000</p>
                  </div>

                  <div
                    class="shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
                  >
                    <button id="bandle_1">
                      <div class="shop_section_buy_items_item_buy_button_info">
                        <img
                          class="button_loading_img"
                          src="./../assets/img/button_loading.svg"
                          alt="loading"
                        />
                        <img src="./../assets/img/stars.svg" alt="buy" />
                        <p>100</p>
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
          <h4>Skins</h4>
        </div>

        <div class="shop_section_skins">
          <div 
          v-for="item in shopItems" 
          :id="['shop#' + item.skin_id]"
          class="shop_section_skins_item skeleton block">
            <div
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
              <p v-if="item.baffs.baffs_type == false">Basic</p>
              <p v-else>
                {{ getRare(item.baffs.baffs_buy_type, item.baffs.baffs_buy_percentage) }}
              </p>
            </div>

            <div class="shop_section_skins_item_left_info">
              <div class="shop_section_skins_item_title">
                <h4>{{ item.name }}</h4>
              </div>
              <div
                style="max-width: 94%"
                class="shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn"
                :class="{ 
                  disabled: item.shop_settings.shop_price_cost > userStorage.user.balance.earn,
                  actived: item.shop_settings.shop_price_cost <= userStorage.user.balance.earn
                }"
              >
                <button 
                @click="buySkinShop(item)">
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
