<template>
  <div class="roulette-container">
    <div class="roulette_detect">
      <img src="./../assets/img/polygon.svg" alt="">
      <div class="roulette_detect_border"></div>
      <img src="./../assets/img/polygon.svg" alt="">
    </div>

    <div v-if="chestItems.length > 0" ref="wheel" class="roulette-wheel" :style="wheelStyle">
      <div
        v-for="(item, index) in infiniteItems"
        :key="index"
        class="roulette-item"
        :style="getItemStyle()"
      >

        <div 
          v-if="item.type == 'skin'"
          class="daily_rewards_item_grided daily_rewards_item_grided_prizes active"
        >
          <div class="daily_rewards_item daily_rewards_item_skin">
              <div 
                class="upgrades_section_skins_item_left_skin"
                :class="item.rare"
              >
                <img src="/src/assets/img/upgrades_effect.png" alt="upgrades_effect" />
                <img :src="getImage(item.prize)" alt="skin" />
                <p v-if="item.baffs.baffs_type == false">Basic</p>
                <p v-else>
                  {{ getRare(item.baffs.baffs_buy_type, item.baffs.baffs_buy_percentage) }}
                </p>
              </div>
          </div>
        </div>
      
        <div 
          v-if="item.type != 'skin'"
          class="daily_rewards_item_grided daily_rewards_item_grided_prizes active"
        >
          <div class="daily_rewards_item">
            <div class="daily_rewards_item_context">
              <div class="daily_rewards_item_context_image">
                <img v-if="item.type == 'views'" src="/src/assets/img/eye.svg" alt="views" />
                <img v-if="item.type == 'money'" src="/src/assets/img/money.svg" alt="money" />
                <img v-if="item.type == 'ton'" src="/src/assets/img/diamond.svg" alt="ton" />
              </div>
              <div class="daily_rewards_item_context_prize">
                <p>{{ item.prize }}</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from "vue";
import { getImage, getRare } from '@/utils/funcs'

export default {
  props: ["chestItems"],
  emits: ["spin-result"],
  setup(props, { emit }) {
    const wheel = ref(null);
    const spinning = ref(false);
    const wheelStyle = ref({});

    const itemCount = computed(() => props.chestItems.length);

    const infiniteItems = computed(() => {
      if (itemCount.value === 0) return [];
      const repeatCount = Math.ceil(100 * itemCount.value);
      return Array(repeatCount).fill(props.chestItems).flat();
    });

    const setInitialStyle = () => {
      if (itemCount.value > 0) {
        wheelStyle.value = {
          transform: `translateX(0%)`,
          transition: "0.6s ease-in-out",
        };
      }
    };

    watch(itemCount, (newCount) => {
      if (newCount > 0 && !spinning.value) {
        setInitialStyle();
      }
    });

    const spin = () => {
      if (spinning.value || itemCount.value === 0) return;

      spinning.value = true;
      const spinDuration = Math.random() * (7434 - 3876) + 3876;
      const spinOffset = Math.floor(Math.random() * itemCount.value);
      const itemWidthPercentage = 1000 / itemCount.value;
      const totalItems = itemCount.value * 20;
      const translateX = -itemWidthPercentage * (spinOffset + totalItems);

      // Запускаем анимацию
      requestAnimationFrame(() => {
        wheelStyle.value = {
          transform: `translateX(${translateX}%)`,
          transition: `transform ${spinDuration / 1000}s cubic-bezier(0.25, 1, 0.5, 1)`,
        };
      });

      setTimeout(() => {
        const finalTranslateX = -itemWidthPercentage * spinOffset;
        wheelStyle.value = {
          transform: `translateX(${finalTranslateX}%)`,
          transition: "transform 0.5s ease-out",
        };
        spinning.value = false;
        emit("spin-result", props.chestItems[spinOffset]);
        setInitialStyle();
      }, spinDuration);
    };

    const getItemStyle = () => ({
      width: `${100 / itemCount.value}%`
    });

    return { 
      wheelStyle, 
      getItemStyle, 
      spin, 
      infiniteItems, 
      getImage, 
      getRare
    };
  },
};
</script>

<style scoped>
@import '../assets/css/daily.css';
@import '../assets/css/upgrades.css';

.roulette-container {
  position: relative;
  width: 100%;
  margin: 0 auto;
  overflow: hidden;
  background-color: #1E274A;
  border-radius: 20px;
  padding: 60px 30px;
}

.roulette-wheel {
  display: flex;
  gap: 12px;
  width: 47%;
  transition: transform 0.3s ease;
}

.roulette-item {
  width: 100px !important;
  max-width: 100px;
  height: 100px;
  text-align: center;
}

.roulette-item .daily_rewards_item_grided {
    width: 100%;
    height: 100%;
}

.roulette-item .daily_rewards_item_grided .daily_rewards_item {
  width: 100px;
  height: 100px;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
}

.roulette_detect {
    width: 100%;
    z-index: 10000;
}

.roulette_detect img:first-child {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
}

.roulette_detect div {
    width: 2px;
    height: 100%;
    position: absolute;
    background: #11A7FF;
    left: 50%;
    top: 50%;
    transform: translateX(-50%) translateY(-50%);
    z-index: 10000;
}

.roulette_detect img:last-child {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%) rotate(180deg);
}

</style>