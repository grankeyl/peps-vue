<template>
  <div class="tutorial">
    <div class="tutorial_inner">
      <swiper
        :slides-per-view="1"
        :pagination="pagination"
        :modules="modules"
        @swiper="onSwiperInit"
      >
        <swiper-slide v-for="slide in tutorialImages">
          <div class="swiper_slide_image" style="margin-left: 7px">
            <img :src="slide['src']" />
          </div>
          <div class="swiper_slide_content">
            <div class="swiper_slide_h4">
              <h4>{{ slide['title'] }}</h4>
            </div>
            <div class="swiper_slide_p">
              <p>{{ slide['description'] }}</p>
            </div>
            <div class="swiper_slide_button">
              <button v-if="slide['button'] == 'Continue'" @click="goToNextSlide">{{ localText[namePage][userDataSettings.language].tu_text_3 }}</button>
              <button v-if="slide['button'] == 'Play game!'" @click="handlePlayGameClick">
                {{ localText[namePage][userDataSettings.language].tu_text_16 }}
              </button>
            </div>
          </div>
        </swiper-slide>
      </swiper>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Pagination } from 'swiper/modules'
import { useRoute } from 'vue-router'

import { TelegramStorage } from '@/stores/telegramStore'
import { localText } from '@/interface'
import { useRouter } from 'vue-router'

export default {
  components: {
    Swiper,
    SwiperSlide
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const referralStatus = ref(route.query.ref)
    
    const namePage = 'tutorial'
    const telegramStorage = TelegramStorage()

    const userDataSettings = computed(() => {
      return {
        language: telegramStorage.getUserLanguage()
      };
    });

    const tutorialImages = ref({
      1: {
        src: '/src/assets/img/tutorial_1.png',
        title: localText[namePage][userDataSettings.value.language].tu_text_1,
        description: localText[namePage][userDataSettings.value.language].tu_text_2,
        button: 'Continue'
      },
      2: {
        src: '/src/assets/img/tutorial_2.png',
        title: localText[namePage][userDataSettings.value.language].tu_text_4,
        description: localText[namePage][userDataSettings.value.language].tu_text_5,
        button: 'Continue'
      },
      3: {
        src: '/src/assets/img/tutorial_3.png',
        title: localText[namePage][userDataSettings.value.language].tu_text_6,
        description: localText[namePage][userDataSettings.value.language].tu_text_7,
        button: 'Continue'
      },
      4: {
        src: '/src/assets/img/tutorial_4.png',
        title: localText[namePage][userDataSettings.value.language].tu_text_8,
        description: localText[namePage][userDataSettings.value.language].tu_text_9,
        button: 'Continue'
      },
      5: {
        src: '/src/assets/img/tutorial_5.png',
        title: localText[namePage][userDataSettings.value.language].tu_text_10,
        description: localText[namePage][userDataSettings.value.language].tu_text_11,
        button: 'Continue'
      },
      6: {
        src: '/src/assets/img/tutorial_6.png',
        title: localText[namePage][userDataSettings.value.language].tu_text_12,
        description: localText[namePage][userDataSettings.value.language].tu_text_13,
        button: 'Continue'
      },
      7: {
        src: '/src/assets/img/tutorial_7.png',
        title: localText[namePage][userDataSettings.value.language].tu_text_14,
        description: localText[namePage][userDataSettings.value.language].tu_text_15,
        button: 'Play game!'
      }
    })

    if (referralStatus.value === 'true') {
      // рефка
    } else {
      // без рефки
      tutorialImages.value['7']['src'] = '/src/assets/img/tutorial_7_1.png'
    }

    const paginationConfig = {
      clickable: true,
      renderBullet(index, className) {
        return `<span class="${className}">${index + 1}</span>`
      }
    }

    const swiperInstance = ref(null)

    const onSwiperInit = (swiper) => {
      swiperInstance.value = swiper
    }

    const goToNextSlide = () => {
      if (swiperInstance.value) {
        swiperInstance.value.slideNext()
      }
    }

    const handlePlayGameClick = () => {
      router.push('/daily')
    }

    return {
      tutorialImages,
      paginationConfig,
      onSwiperInit,
      goToNextSlide,
      handlePlayGameClick,

      namePage,
      userDataSettings,
      localText,

      pagination: {
        clickable: true,
        renderBullet: function (index, className) {
          return '<span class="' + className + '">' + (index + 1) + '</span>'
        }
      },
      modules: [Pagination]
    }
  }
}
</script>

<style>
@import '../assets/css/default.css';

/* Keyframes for fade-in animation */
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
    pointer-events: none;
  }
  100% {
    opacity: 1;
    transform: translateY(0);
    pointer-events: all;
  }
}

/* Apply animation to the images */
.swiper_slide_image img {
  animation: fadeIn 0.8s ease-in-out forwards;
  animation-delay: 0.2s;
}

/* Apply animation to the h4 titles */
.swiper_slide_h4 h4 {
  opacity: 0;
  animation: fadeIn 1s ease-in-out forwards;
  animation-delay: 0.4s;
}

/* Apply animation to the paragraph texts */
.swiper_slide_p p {
  opacity: 0;
  animation: fadeIn 1.2s ease-in-out forwards;
  animation-delay: 0.6s;
}

/* Apply animation to the buttons */
.swiper_slide_button button {
  opacity: 0;
  animation: fadeIn 1.4s ease-in-out forwards;
  animation-delay: 0.8s;
}
</style>
