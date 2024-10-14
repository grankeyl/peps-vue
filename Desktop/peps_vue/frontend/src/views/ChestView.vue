<script lang="ts">
import { ref, onMounted } from "vue";
import RouletteWheel from "./../components/RouletteWheel.vue";
import { getChests } from '@/utils/apiRequest'
import { getSkinJson } from '@/utils/funcs'

export default {
  components: {
    RouletteWheel,
  },
  setup() {

    const chests = ref([])
    const chestItems = ref([]);
    
    const getChestsValue = async () => {
      const response = await getChests()
      if (response.success) {
        chests.value = response.data
        
        const case1Chests = chests.value['case_1'].chest_prizes
        case1Chests.forEach(element => {
          const prize = element
          const prize_type = prize['prize'].split(':')[0]
          const prize_value = element.split(':')[1]
          if (prize_type == 'skin') {
            chestItems.value.push({ type: prize_type, prize: prize_value, rare: getSkinJson(prize_value).rare, baffs: getSkinJson(prize_value).baffs })
          } else {
            chestItems.value.push({ type: prize_type, prize: prize_value })
          }
        })
        console.log(chestItems.value)
      }
    }

    getChestsValue()

    const result = ref(null);
    const rouletteWheel = ref(null);

    const handleResult = (item) => {
      result.value = item;
    };

    const spin = () => {
      if (rouletteWheel.value) {
        rouletteWheel.value.spin(); // Call spin through ref once component is mounted
      }
    };

    // Ensure the rouletteWheel is set up after the component is mounted
    onMounted(() => {
      if (rouletteWheel.value) {
        rouletteWheel.value.spin = rouletteWheel.value.spin; // Make sure the spin function is accessible
      }
    });

    return { 
      chestItems, 
      result, 
      spin, 
      handleResult, 
      rouletteWheel,
      chests,
      getSkinJson
    };
  },
}
</script>

<template>
  <div class="chest">
    <div class="chest_inner">
      <div class="chest_content">
        <div class="chest_image">
          <img src="./../assets/img/money_center.svg" alt="chest" />
        </div>
        <div class="chest_h">
          <h3>{{ chests['case_1']?.chest_name || 'Loading...' }}</h3>
        </div>
        <div class="chest_p">
          <p>{{ chests['case_1']?.chest_description || 'Loading...' }}</p>
        </div>
      </div>
      <div class="chest_free">
        <RouletteWheel ref="rouletteWheel" :chestItems="chestItems" @spin-result="handleResult" />
        <div v-if="result" class="result">
          <h2>Вы выиграли:</h2>
          <p>{{ result.name }}</p>
        </div>
      </div>
      <div class="chest_free">
        <div 
        @click="spin"
        class="chest_spin"
        >
            <div class="chest_spin_button">
                <div class="chest_spin_button_text">
                    <p>Spin</p>
                </div>
                <div class="chest_spin_button_stars">
                  <div class="chest_spin_button_stars_image">
                      <img v-if="chests['case_1']?.chest_buy_type === 'stars'" src="/src/assets/img/stars.svg" alt="money" />
                      <img v-if="chests['case_1']?.chest_buy_type === 'views'" src="/src/assets/img/eye.svg" alt="money" />
                      <img v-if="chests['case_1']?.chest_buy_type === 'money'" src="/src/assets/img/money.svg" alt="money" />
                      <img v-if="chests['case_1']?.chest_buy_type === 'ton'" src="/src/assets/img/diamond.svg" alt="money" />
                  </div>
                  <div class="chest_spin_button_stars_amount">
                      <p>{{ chests['case_1']?.chest_buy_amount || 'Loading...' }}</p>
                  </div>
              </div>
            </div>
        </div>
      </div>
      <div class="chest_free">
        <div class="chest_free_block">
          <div class="chest_free_text">
            <div class="chest_h">
              <h4>Возможные награды</h4>
            </div>
          </div>
          <div class="chest_arrow">
            <img src="/src/assets/img/chevrone_right.svg" alt="money" />
          </div>
        </div>
        <div class="chest_free_block">
          <div class="chest_free_text">
            <div class="chest_h">
              <h4>Получи фри-спин</h4>
            </div>
            <div class="chest_p last_p">
              <p>За каждого пятого приглашенного друга</p>
            </div>
          </div>
          <div class="chest_arrow">
            <img src="/src/assets/img/chevrone_right.svg" alt="money" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '../assets/css/chest.css';
@import '../assets/css/daily.css';
</style>
