<template>
  <div :id="['skin#' + skin.skin_id]" class="upgrades_section_skins_item skeleton block">
    <div class="upgrades_section_skins_item_left">
      <div :class="['upgrades_section_skins_item_left_skin', skin.skin_rare]">
        <img src="./../../assets/img/upgrades_effect.png" alt="upgrades_effect" />
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

      <p class="upgrades_section_skins_item_left_border_gift_icon">
        {{
          skin.skin_upgrade.upgrades_level == 1 &&
          skin.skin_upgrade.upgrades_level_step == 9 &&
          userStorage.user.referals < 1
            ? ''
            : '🎁'
        }}
      </p>

      <div class="upgrades_section_skins_item_right_upgrade">
        <div
          @click="handleUpgrade"
          class="upgrades_section_skins_item_right_upgrade_btn"
          :class="buttonClass"
          :id="'upgradeSkinChecker#' + skin.skin_id"
        >
          <button>
            <img
              class="button_loading_img"
              src="./../../assets/img/button_loading.svg"
              alt="loading"
            />
            <p v-if="isMaxLevel">{{ localText[namePage][userDataSettings.language].up_text_13 }}</p>
            <p v-if="isReferralNeeded">{{ localText[namePage][userDataSettings.language].up_text_18 }}</p>
            <img v-if="isReferralNeeded" src="./../../assets/img/chevrone_right.svg" alt="money" />
            <p v-if="!isMaxLevel && !isReferralNeeded">{{ localText[namePage][userDataSettings.language].up_text_12 }}</p>
          </button>
        </div>
        <div v-if="!isMaxLevel" class="upgrades_section_skins_item_right_upgrade_summary" :class="{ opacity: isReferralNeeded }">
          <img v-if="skin.skin_upgrade.upgrades_cost_type == 'views'" src="./../../assets/img/eye.svg" alt="views" />
          <img v-if="skin.skin_upgrade.upgrades_cost_type == 'money'" src="./../../assets/img/money.svg" alt="money" />
          <img v-if="skin.skin_upgrade.upgrades_cost_type == 'ton'" src="./../../assets/img/ton.svg" alt="ton" />
          <img v-if="skin.skin_upgrade.upgrades_cost_type == 'stars'" src="./../../assets/img/stars.svg" alt="stars" />
          <p>{{ formatNumber(skin.skin_upgrade.upgrades_cost) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "EQ_UpgradeItem",
  props: {
    skin: {
      type: Object,
      required: true,
    },
    localText: {
      type: Object,
      required: true,
    },
    userDataSettings: {
      type: Object,
      required: true,
    },
    userStorage: {
      type: Object,
      required: true,
    },
    namePage: {
      type: String,
      required: true,
    },
    isEnoughUpgrades: {
      type: Function,
      required: true,
    },
    repostGame: {
      type: Function,
      required: true,
    },
    upgrade: {
      type: Function,
      required: true,
    },
    getImage: {
      type: Function,
      required: true,
    },
    getSkinInfo: {
      type: Function,
      required: true,
    },
    formatNumber: {
      type: Function,
      required: true,
    },
    getUpgradeLine: {
      type: Function,
      required: true,
    },
    upgradeStatus: { // Новый проп для статуса улучшения
      type: Boolean,
      required: true,
    },
  },
  computed: {
    isMaxLevel() {
      return this.skin.skin_upgrade.upgrades_level === Object.keys(this.skin.skin_upgrade.upgrades_paths).length + 1;
    },
    isReferralNeeded() {
      return (
        this.skin.skin_upgrade.upgrades_level == 1 &&
        this.skin.skin_upgrade.upgrades_level_step == 9 &&
        this.userStorage.user.referals < 1
      );
    },
    buttonClass() {
      return {
        disabled: !this.isEnoughUpgrades(
          this.skin.skin_upgrade.upgrades_cost_type,
          this.skin.skin_upgrade.upgrades_cost
        ) || this.isMaxLevel, // Проверяем статус улучшения
        actived: this.isEnoughUpgrades(
          this.skin.skin_upgrade.upgrades_cost_type,
          this.skin.skin_upgrade.upgrades_cost
        ) && !this.isMaxLevel, // Проверяем статус улучшения
        maxlevel: this.isMaxLevel,
        needref: this.isReferralNeeded,
      };
    },
  },
  methods: {
    handleUpgrade() {
      if (this.isReferralNeeded) {
        this.repostGame();
      } else {
        this.upgrade(this.skin);
      }
    },
  }
};
</script>

<style scoped>
@import '@/assets/css/upgrades.css';
@import '@/assets/css/profile.css';
</style>