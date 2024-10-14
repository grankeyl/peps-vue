<template>
  <div 
    class="preview_skin"
    :class="{ active: status, closing: isClosing }"
  >
    <div class="preview_skin_inner">

      <div @click="triggerClose" class="preview_skin_close">
        <img src="/src/assets/img/close.svg" alt="close" />
      </div>

      <div class="preview_skin_id">
        <div 
          class="upgrades_section_skins_item_left_skin shop_section_skins_item_skin"
          :class="rarity"
        >
          <div class="shop_section_skins_item_skin_inner">
            <img src="/src/assets/img/upgrades_effect.png" alt="upgrades_effect">
            <img :src="'/src/assets/skins/' + skin_id + '.png'" alt="skin">
          </div>
          <p v-if="baffs_object.baffs_type == false">{{ localText['root'][language_user].root_text_6 }}</p>
          <p v-else>{{ baffs }}</p>
        </div>
      </div>

      <div class="preview_skin_title">
        <h4>{{ title }}</h4>
      </div>

      <div class="preview_skin_description">
        <p v-if="language_user == 'ru'">{{ description_ru }}</p>
        <p v-else>{{ description }}</p>
      </div>

    </div>

      <div class="preview_skin_table">
        <div class="preview_skin_cell_left"></div>
          <div class="preview_skin_row">
              <div class="preview_skin_cell preview_skin_cell_title">{{ localText['root'][language_user].root_text_19 }}</div>
              <div v-if="quantity_need > 0" class="preview_skin_cell preview_skin_cell_value">
                <span v-if="quantity_count == 0" class="preview_skin_availability">0</span>
                <span v-if="quantity_count != 0" class="preview_skin_availability">{{ quantity_count }}</span>
                /
                <span v-if="quantity_count != 0" class="preview_skin_tiraj">{{ quantity_need }}</span>
                <span v-if="quantity_count == 0" class="preview_skin_tiraj">{{ quantity_need }}</span>
              </div>
              <div v-else class="preview_skin_cell preview_skin_cell_value">
                <span class="preview_skin_tiraj">∞</span>
              </div>
          </div>
          <div class="preview_skin_row">
              <div class="preview_skin_cell preview_skin_cell_title">{{ localText['root'][language_user].root_text_20 }}</div>
              <div v-if="!formatNumberPreview" class="preview_skin_cell preview_skin_cell_value">
                0
              </div>
              <div v-else class="preview_skin_cell preview_skin_cell_value">
                <img v-if="price_type == 'views'" src="/src/assets/img/eye.svg" alt="buy" />
                <img v-if="price_type == 'money'" src="/src/assets/img/money.svg" alt="buy" />
                <img v-if="price_type == 'ton'" src="/src/assets/img/diamond.svg" alt="buy" />
                <img v-if="price_type == 'stars'" src="/src/assets/img/stars.svg" alt="buy" />
                {{ formatNumberPreview }}
              </div>
          </div>
          <div class="preview_skin_row">
              <div class="preview_skin_cell preview_skin_cell_title">{{ localText['root'][language_user].root_text_21 }}</div>
              <div v-if="rarity == 'very_rare'" class="preview_skin_cell preview_skin_cell_value" style="text-transform: capitalize;">very rare</div>
              <div v-else class="preview_skin_cell preview_skin_cell_value" style="text-transform: capitalize;">{{ rarity }}</div>
          </div>
      </div>

      <div class="preview_skin_button">
          <div
            :id="'previewSkinBuy#' + this.skin_id"
            :class="{
              disabled: !checkBuy,
              actived: checkBuy
            }"
            class="special_btn_qd shop_section_buy_items_item_buy shop_section_buy_items_item_buy shop_section_skins_item_buy upgrades_section_skins_item_right_upgrade_btn actived"
          >
            <button 
              @click="checkBuy ? buySkin() : null"
              id="btn_special_"
            >
              <div class="shop_section_buy_items_item_buy_button_info">
                <img
                  class="button_loading_img"
                  src="/src/assets/img/button_loading.svg"
                  alt="loading"
                />
                <p>{{ localText['root'][language_user].root_text_22 }}</p>
                <img id="special_btnType" v-if="price_type == 'views'" src="/src/assets/img/eye.svg" alt="buy" />
                <img id="special_btnType" v-if="price_type == 'money'" src="/src/assets/img/money.svg" alt="buy" />
                <img id="special_btnType" v-if="price_type == 'ton'" src="/src/assets/img/diamond.svg" alt="buy" />
                <img id="special_btnType" v-if="price_type == 'stars'" src="/src/assets/img/stars.svg" alt="buy" />
                <p>{{ formatNumberPreview }}</p>
              </div>
            </button>
          </div>
      </div>

  </div>
</template>

<script>
import { formatNumber } from '@/utils/funcs'

export default {
  name: "Preview_ShopItem",
  props: {
    status: {
      type: Boolean,
      required: true
    },
    skin_id: {
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
    description_ru: {
      type: String,
      required: true
    },
    rarity: {
      type: String,
      required: true
    },
    price_type: {
      type: String,
      required: true
    },
    price: {
      type: Number,
      required: true
    },
    quantity_count: {
      type: Number,
      required: true
    },
    quantity_need: {
      type: Number,
      required: true
    },
    language_user: {
      type: String,
      required: true
    },
    baffs_object: {
      type: Object,
      required: true
    },
    baffs: {
      type: String,
      required: true
    },
    localText: {
      type: Object,
      required: true
    },
    checkBuy: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      isClosing: false,
    };
  },
  computed: {
    formatNumberPreview() {
      return (
        formatNumber(this.price)
      );
    }
  },
  methods: {
    triggerClose() {
      this.isClosing = true;
      setTimeout(() => {
        this.isClosing = false;
        this.$emit('closeModal');
      }, 300);
    },
    buySkin() {
      const buttonBlock = document.getElementById(`previewSkinBuy#${this.skin_id}`);
      const special_btnType = document.getElementById(`special_btnType`);

      special_btnType.remove()
      buttonBlock.classList.remove('actived');
      buttonBlock.classList.add('disabled');
      buttonBlock.classList.add('button_loading');

      if (this.price_type != 'stars') {
        setTimeout(() => {
          buttonBlock.classList.remove('button_loading');
          buttonBlock.classList.remove('disabled');
          buttonBlock.classList.add('actived');
          this.isClosing = false;
        }, 300);
      }

      this.$emit('buySkin');
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/upgrades.css';
@import '@/assets/css/profile.css';
@import '@/assets/css/shop.css';
</style>