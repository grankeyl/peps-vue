<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { UserStorage } from '@/stores/userStore'
import { updateGame } from '@/utils/apiRequest'
import { Rive } from '@rive-app/canvas'
import { getPutonSkins } from '@/utils/apiRequest'
import { getImage } from '@/utils/funcs'

const name = 'HomeView'
const skinsPath = window.location.pathname.replace('/home', '')
const userStorage = UserStorage()

const vQ_game_0 = ref<HTMLCanvasElement | null>(null)
const vQ_game_1 = ref<HTMLCanvasElement | null>(null)
const vQ_game_2 = ref<HTMLCanvasElement | null>(null)
const vQ_game_3 = ref<HTMLCanvasElement | null>(null)
const vQ_game_4 = ref<HTMLCanvasElement | null>(null)
const vQ_game_5 = ref<HTMLCanvasElement | null>(null)
const vQ_game_6 = ref<HTMLCanvasElement | null>(null)
const vQ_game_7 = ref<HTMLCanvasElement | null>(null)
const vQ_game_8 = ref<HTMLCanvasElement | null>(null)
const vQ_game_9 = ref<HTMLCanvasElement | null>(null)
const vQ_game_10 = ref<HTMLCanvasElement | null>(null)
const vQ_game_11 = ref<HTMLCanvasElement | null>(null)
const vQ_game_12 = ref<HTMLCanvasElement | null>(null)
const vQ_game_13 = ref<HTMLCanvasElement | null>(null)

const todayIconLoading = ref([])
todayIconLoading.value = ['diamond', 'profile', 'money', 'eye']

function getTodayIcon() {
  return todayIconLoading.value[Math.floor(Math.random() * todayIconLoading.value.length)];
}

const iconSrc = computed(() => {
  return ['/src/assets/img/', getTodayIcon(), '.svg'].join('');
});

const putonSkinsList = ref([])
const putonSkins = ref([])

// const images0 = ref([])

let isFireStarted = ref(false)
let fireClickChecker = ref(true)

const showLoadingStatus = ref(true);
const fadeOut = ref(false);

function startFire(isFireStarted, fireClickChecker, gameBlock) {
  if (isFireStarted.value) {
    return
  }

  isFireStarted.value = true
  fireClickChecker.value = false

  const fireElement = document.createElement('div')
  fireElement.className = 'layer_a fire'
  fireElement.innerHTML = `
    <div style="width: 100%; height: 100%;">
      <canvas class="layer_a layer_i layer_a_5" id="layer_a_5" width="900" height="1950" style="vertical-align: top; margin-top: -30px; width: 420px; height: 955px;"></canvas>
    </div>
  `

  gameBlock.appendChild(fireElement)

  const canvasElement = document.getElementById('layer_a_5') as HTMLCanvasElement
  if (canvasElement) {
    canvasElement.style.opacity = '1'
  }

  let riveFireInstance: rive.Rive

  try {
    riveFireInstance = new Rive({
      src: `${skinsPath}src/assets/animations/fire.riv`,
      canvas: canvasElement,
      autoplay: false,
      onLoad: () => {
        riveFireInstance.play()
      },
      onLoop: () => {
        riveFireInstance.pause()
        if (canvasElement) {
          canvasElement.style.opacity = '0'
        }
      },
      onError: (error: Error) => {
        return
      }
    })
  } catch (error) {
    return
  }

  setTimeout(() => {
    isFireStarted.value = false
    fireClickChecker.value = true

    fireElement.remove()
  }, 3276)
}

function handleTouchStart(event: TouchEvent) {
  event.preventDefault()
  if (event.touches.length === 2) {
    touch(false)
    touch(false)
  } else {
    touch(false)
  }
}

function handleMouseDown(event: MouseEvent) {
  event.preventDefault()
  if (event.detail === 2) {
    touch(false)
    touch(false)
  } else {
    touch(false)
  }
}

function setupCanvas(canvas: HTMLCanvasElement, width: number, height: number) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const dpr = window.devicePixelRatio || 1

  canvas.width = width * dpr
  canvas.height = height * dpr
  ctx.scale(dpr, dpr)

  canvas.style.width = '100%'
  canvas.style.height = height + 'px'

  ctx.imageSmoothingEnabled = true

  return { canvas, ctx }
}

function loadSVG(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    fetch(src)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.statusText}`)
        }
        return response.text()
      })
      .then((svgText) => {
        const img = new Image()
        img.onload = () => {
          resolve(img)
        }
        img.onerror = (err) => {
          return
        }

        img.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svgText)}`
      })
      .catch((err) => {
        return
      })
  })
}

async function combineImages(
  { canvas, ctx }: { canvas: HTMLCanvasElement; ctx: CanvasRenderingContext2D },
  images: { src: string; layer: number }[]
) {
  const loadedImages = await Promise.all(images.map(({ src }) => loadSVG(src)))

  const imagesWithLayers = images.map((imgData, index) => ({
    img: loadedImages[index],
    layer: imgData.layer
  }))

  imagesWithLayers.sort((a, b) => a.layer - b.layer)

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  imagesWithLayers.forEach(({ img }) => {
    const scaleX = canvas.width / img.width / window.devicePixelRatio
    const scaleY = canvas.height / img.height / window.devicePixelRatio
    const scale = Math.min(scaleX, scaleY)

    const x = (canvas.width / window.devicePixelRatio - img.width * scale) / 2
    const y = (canvas.height / window.devicePixelRatio - img.height * scale) / 2

    ctx.drawImage(img, x, y, img.width * scale, img.height * scale)
  })
}

onMounted(() => {
  if (vQ_game_0.value && vQ_game_1.value && vQ_game_2.value && vQ_game_3.value && vQ_game_4.value && vQ_game_5.value && vQ_game_6.value && vQ_game_7.value && vQ_game_8.value && vQ_game_9.value && vQ_game_10.value && vQ_game_11.value && vQ_game_12.value && vQ_game_13.value) {
    const canvas0 = setupCanvas(vQ_game_0.value, 440, 1000)
    const canvas1 = setupCanvas(vQ_game_1.value, 440, 1000)
    const canvas2 = setupCanvas(vQ_game_2.value, 440, 1000)
    const canvas3 = setupCanvas(vQ_game_3.value, 440, 1000)
    const canvas4 = setupCanvas(vQ_game_4.value, 440, 1000)
    const canvas5 = setupCanvas(vQ_game_5.value, 440, 1000)
    const canvas6 = setupCanvas(vQ_game_6.value, 440, 1000)
    const canvas7 = setupCanvas(vQ_game_7.value, 440, 1000)
    const canvas8 = setupCanvas(vQ_game_8.value, 440, 1000)
    const canvas9 = setupCanvas(vQ_game_9.value, 440, 1000)
    const canvas10 = setupCanvas(vQ_game_10.value, 440, 1000)
    const canvas11 = setupCanvas(vQ_game_11.value, 440, 1000)
    const canvas12 = setupCanvas(vQ_game_12.value, 440, 1000)
    const canvas13 = setupCanvas(vQ_game_13.value, 440, 1000)

    // Background Room

    const fetchPutonSkins = async () => {
      const skins = await getPutonSkins(userStorage.user.user_id)

      if (skins.success && skins.skins_list.length !== 0) {
        putonSkinsList.value = skins.skins_list
        putonSkins.value = skins.skins
        setLists()
        clearInterval(interval)
        return skins
      }
    }

    const interval = setInterval(() => {
      fetchPutonSkins()
    }, 600)

    // Not clickable elements
    const images0 = []

    // Not clickable elements (window)
    const images1 = []

    // Clickable elements
    const images2 = []

    // Clickable elements (keyboard)
    const images3 = []

    // Clickable elements (monitor)
    const images4 = []

    // Clickable elements (hands)
    const images5 = []

    // Clickable elements (cable-keyboard)
    const images6 = []

    // Clickable elements (systembox)
    const images7 = []

    // Clickable elements (chair)
    const images8 = []

    // Clickable elements (flower)
    const images9 = []

    // Not clickable elements (window-light)
    const images10 = []

    // Not clickable elements (window-light)
    const images11 = []

    // Not clickable elements (item-window)
    const images12 = []

    // Not clickable elements (item-window)
    const images13 = []

    function setLists() {
      // Not clickable elements
      putonSkins.value.forEach((element) => {
        if (element.clickable == false) {
          if (!element.skin_id.includes('systembox_') && !element.skin_id.includes('flower_') && !element.skin_id.includes('item-table_') && !element.skin_id.includes('item-window_')) {
            images0.push({
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: element.z_index
            })
          }
        }
      })

      // Not clickable elements (window)
      images1.push({
        src: `${skinsPath}src/assets/skins/window_1.svg`,
        layer: 4
      })

      // Clickable elements
      putonSkins.value.forEach((element) => {
        if (element.clickable == true) {
          if (!element.skin_id.includes('keyboard_') && !element.skin_id.includes('monitors_') && !element.skin_id.includes('systembox_') && !element.skin_id.includes('chair_')) {
            if (element.skin_id.includes('tee_')) {
              const id_count = element.skin_id.split('_')[1]
              images2.push({
                src: `${getImage(element.skin_id, '.svg')}`,
                layer: element.z_index
              })
            } else {
              images2.push({
                src: `${getImage(element.skin_id, '.svg')}`,
                layer: element.z_index
              })
            }
          }
        }
      }) 

      // Clickable elements (keyboard)
      putonSkins.value.forEach((element) => {
        if (element.clickable == true) {
          if (element.skin_id.includes('keyboard_')) {
            const id_count = element.skin_id.split('_')[1]
            images3.push({
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: element.z_index
            })
          }
        }
      })

      // Clickable elements (monitor)
      putonSkins.value.forEach((element) => {
        if (element.clickable == true) {
          if (element.skin_id.includes('monitors_')) {
            const id_count = element.skin_id.split('_')[1]
            images4.push({
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: element.z_index
            })
          }
        }
      })

      // Clickable elements (hands)
      putonSkins.value.forEach((element) => {
        if (element.clickable == true) {
          if (element.skin_id.includes('tee_')) {
            const id_count = element.skin_id.split('_')[1]
            images5.push({
              src: `${getImage(`hands_${id_count}`, '.svg')}`,
              layer: element.z_index
            })
          }
        }
      })

      // Clickable elements (cable-keyboard)
      putonSkins.value.forEach((element) => {
        if (element.clickable == true) {
          if (element.skin_id.includes('keyboard_')) {
            const id_count = element.skin_id.split('_')[1]
            images6.push({
              src: `${getImage(`cable-keyboard_${id_count}`, '.svg')}`,
              layer: 8
            })
          }
        }
      })

      // Clickable elements (systembox)
      putonSkins.value.forEach((element) => {
        if (element.clickable == false) {
          if (element.skin_id.includes('systembox_')) {
            const id_count = element.skin_id.split('_')[1]
            images7.push({
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: 1
            })
          }
        }
      })

      // Clickable elements (chair)
      putonSkins.value.forEach((element) => {
        if (element.clickable == true) {
          if (element.skin_id.includes('chair_')) {
            const id_count = element.skin_id.split('_')[1]
            images8.push({
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: 8
            })
          }
        }
      })

      // Clickable elements (flower)
      putonSkins.value.forEach((element) => {
        if (element.clickable == false) {
          if (element.skin_id.includes('flower_')) {
            const id_count = element.skin_id.split('_')[1]
            images9.push({
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: 8
            })
          }
        }
      })

      // Not clickable elements (window-light)
      images10.push({
        src: `${skinsPath}src/assets/skins/light-window_1.svg`,
        layer: 4
      })

      // Not clickable elements (item-table)
      putonSkins.value.forEach((element) => {
        if (element.clickable == false) {
          if (element.skin_id.includes('item-table_')) {
            const id_count = element.skin_id.split('_')[1]
            images11.push({
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: 8
            })
          }
        }
      })

      // Not clickable elements (item-window)
      putonSkins.value.forEach((element) => {
        if (element.clickable == false) {
          if (element.skin_id.includes('item-window_')) {
            const id_count = element.skin_id.split('_')[1]
            images12.push({
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: 8
            })
          }
        }
      })

      // Not clickable elements (item-window)
      putonSkins.value.forEach((element) => {
        if (element.clickable == true) {
          if (element.skin_id.includes('table_2') && element.skin_id.includes('table_3')) {
            const id_count = element.skin_id.split('_')[1]
            images13.push({
              src: `${getImage(`table_${id_count}_right`, '.svg')}`,
              layer: 8
            })
          }
        }
      })

      combineImages(canvas0, images0).catch((err) => {
        return
      })

      combineImages(canvas1, images1).catch((err) => {
        return
      })

      combineImages(canvas2, images2).catch((err) => {
        return
      })

      combineImages(canvas3, images3).catch((err) => {
        return
      })

      combineImages(canvas4, images4).catch((err) => {
        return
      })

      combineImages(canvas5, images5).catch((err) => {
        return
      })

      combineImages(canvas6, images6).catch((err) => {
        return
      })

      combineImages(canvas7, images7).catch((err) => {
        return
      })

      combineImages(canvas8, images8).catch((err) => {
        return
      })

      combineImages(canvas9, images9).catch((err) => {
        return
      })

      combineImages(canvas10, images10).catch((err) => {
        return
      })

      combineImages(canvas11, images11).catch((err) => {
        return
      })

      combineImages(canvas12, images12).catch((err) => {
        return
      })

      combineImages(canvas13, images13).catch((err) => {
        return
      })

      async function processCanvases() {
        try {
          await Promise.all([
            combineImages(canvas1, images1),
            combineImages(canvas2, images2),
            combineImages(canvas3, images3),
            combineImages(canvas4, images4),
            combineImages(canvas5, images5),
            combineImages(canvas6, images6),
            combineImages(canvas7, images7),
            combineImages(canvas8, images8),
            combineImages(canvas9, images9),
            combineImages(canvas10, images10),
            combineImages(canvas11, images11),
            combineImages(canvas12, images12),
            combineImages(canvas13, images13)
          ]);
        } catch (err) {
          return;
        }

        setTimeout(() => {
          showLoadingStatus.value = false;
        }, 0);
      }

      processCanvases();

    }
  }
})

function touchAnimation() {
  if (userStorage.settings.tap_animation) {
    const elements = [vQ_game_2.value, vQ_game_5.value, vQ_game_6.value, vQ_game_4.value, vQ_game_3.value, vQ_game_8.value, vQ_game_13.value];
    elements.forEach((element) => {
      if (element) {
        element.classList.remove('animate');
        void element.offsetWidth; // Trigger reflow
        element.classList.add('animate');
        element.addEventListener(
          'animationend',
          () => {
            element.classList.remove('animate');
          },
          { once: true }
        );
      }
    });
  }
}

let lastClickTimeout

function touchTimeout() {
  clearTimeout(lastClickTimeout)
  lastClickTimeout = setTimeout(async () => {
    updateGame(
      userStorage.user.user_id,
      userStorage.user.balance.views,
      userStorage.user.balance.earn,
      userStorage.user.balance.ton,
      userStorage.costs.stamina_now
    )
  }, 2000)
}

function getPostResult(type, isAuto) {
  let chance
  if (isAuto === true) {
    switch (type) {
      case 'views':
        chance = parseInt(userStorage.costs.auto_views_chance)
        break
      case 'earn':
        chance = parseInt(userStorage.costs.auto_money_chance)
        break
      default:
        chance = parseFloat(userStorage.costs.auto_ton_chance)
    }
  } else {
    switch (type) {
      case 'views':
        chance = parseInt(userStorage.costs.views_chance)
        break
      case 'earn':
        chance = parseInt(userStorage.costs.money_chance)
        break
      default:
        chance = parseFloat(userStorage.costs.ton_chance)
    }
  }

  if (isAuto == true) {
    return Math.random() <= chance / 100 ? true : false
  } else {
    return Math.random() / 2 <= chance / 100 ? true : false
  }
}

function touchPost(type) {
  if (type === 'earn') {
    type = 'money'
  }

  const newDiv = document.createElement('div')
  const uniqueId = `post_${Date.now()}`

  let className = ''
  let headClassName = ''
  let postImage = ''
  let postAmount = ''
  let imageSrc = ''

  if (type === 'views') {
    className = 'gamePost'
    headClassName = 'views'
    postImage = 'default'
    postAmount = `+${userStorage.costs.views_costs}`
    imageSrc = 'eye'
  } else if (type === 'money') {
    className = 'gamePost_green'
    headClassName = 'money'
    postImage = 'money'
    postAmount = `+${userStorage.costs.money_costs}`
    imageSrc = 'money'
  } else {
    className = 'gamePost_ton'
    headClassName = 'ton'
    postImage = 'ton'
    postAmount = `+${userStorage.costs.ton_costs} TON`
    imageSrc = 'diamond'
  }

  newDiv.className = `${className} ${uniqueId}`
  newDiv.innerHTML = `
    <div class="gamePost_head">
        <div class="gamePost_head_number ${headClassName}">
            <p>${postAmount}</p>
        </div>
        <img src="${skinsPath}src/assets/img/${imageSrc}.svg" alt="">
    </div>
    <div class="gamePost_image">
        <img src="${skinsPath}src/assets/img/peps_post_${postImage}.svg" alt="">
    </div>`

  document.getElementById('game_block').appendChild(newDiv)
  newDiv.classList.add(`${className}_animation`)

  const elements = document.querySelectorAll('.gamePost, .gamePost_green, .gamePost_ton')
  elements.forEach((element) => {
    element.addEventListener('animationend', (event) => {
      const parent = event.target.parentElement
      if (parent && parent.children.length > 1) {
        event.target.remove()
      }
    })
  })
}

function touchPostAnimation(type) {
  if (type == 'earn') {
    type = 'money'
  }
  let element = document.getElementById(`header_button_${type}_block`)
  element.classList.add('animate_add_money')
  setTimeout(() => element.classList.remove('animate_add_money'), 600)
}

function touch(isAuto) {
  let stamina = userStorage.costs.stamina_now

  // stamina update
  if (stamina != 0 || isAuto) {
    if (!isAuto) {
      userStorage.costs.stamina_now--
    }

    if (!isAuto) {
      touchTimeout()
    }

    if (!isAuto) {
      touchAnimation()
    }

    let viewsPercents
    let earnPercents
    let tonPercents

    // random reward
    if (isAuto) {
      viewsPercents = userStorage.costs.auto_views_chance
      earnPercents = userStorage.costs.auto_money_chance
      tonPercents = userStorage.costs.auto_ton_chance
    } else {
      viewsPercents = userStorage.costs.views_chance
      earnPercents = userStorage.costs.money_chance
      tonPercents = userStorage.costs.ton_chance
    }

    const totalPercents = viewsPercents + earnPercents + tonPercents
    const random = Math.floor(Math.random() * totalPercents) + 1

    let result

    if (random <= viewsPercents) {
      result = 'views'
    } else if (random <= viewsPercents + earnPercents) {
      result = 'earn'
    } else {
      result = 'ton'
    }

    if (getPostResult(result, isAuto)) {
      touchPostAnimation(result)
      touchPost(result)

      switch (result) {
        case 'views':
          userStorage.user.balance.views += userStorage.costs.views_costs
          break
        case 'earn':
          userStorage.user.balance.earn += userStorage.costs.money_costs
          break
        case 'ton':
          userStorage.user.balance.ton += userStorage.costs.ton_costs
          break
      }
    }
  } else {
    startFire(isFireStarted, fireClickChecker, document.getElementById('game_block'))
  }
}

setInterval(() => {
  if (location.pathname === '/') {
    touch(true)
  }
}, 3300)

setInterval(() => {
  updateGame(
    userStorage.user.user_id,
    userStorage.user.balance.views,
    userStorage.user.balance.earn,
    userStorage.user.balance.ton,
    userStorage.costs.stamina_now
  )
}, 15000)
</script>

<template>
  <div class="game">
    <div class="gameNotifed">
      <div class="gameNotifed_block">
        <div class="gameNotifed_block_text">
          <h4>Season 1 out!</h4>
        </div>
        <div class="gameNotifed_block_button">
          <button onclick="window.open('https://t.me/PepsENG', '_blank')">
            <p>Learn more</p>
          </button>
        </div>
      </div>

      <div class="gameNotifed_block">
        <a href="https://teletype.in/@peperonl/PepsRoadmapRU" style="text-decoration: none">
          <div class="gameNotifed_block_text_roadmap">
            <img src="./../assets/img/diamond.svg" alt="" />
            <h4>Roadmap</h4>
          </div>
        </a>
      </div>
    </div>

    <div class="game_block" id="game_block">
      <canvas
        ref="vQ_game_0"
        class="layer_a layer_i"
        style="position: absolute; z-index: 1; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_1"
        class="layer_a layer_i"
        style="position: absolute; z-index: 2; top: 0px"
      ></canvas>

      <canvas
        @touchstart="handleTouchStart"
        @mousedown="handleMouseDown"
        ref="vQ_game_2"
        class="layer_a layer_i layer_i_true layer_iVq_true"
        style="position: absolute; z-index: 9; top: 0px"
      ></canvas>

      <canvas
        @touchstart="handleTouchStart"
        @mousedown="handleMouseDown"
        ref="vQ_game_3"
        class="layer_a layer_i index_keyboard"
        style="position: absolute; z-index: 9; top: 0px"
      ></canvas>

      <canvas
        @touchstart="handleTouchStart"
        @mousedown="handleMouseDown"
        ref="vQ_game_4"
        class="layer_a layer_i index_monitor layer_iVq_true"
        style="position: absolute; z-index: 11; top: 0px"
      ></canvas>

      <canvas
        @touchstart="handleTouchStart"
        @mousedown="handleMouseDown"
        ref="vQ_game_5"
        class="layer_a layer_i index_hands layer_iVq_true"
        style="position: absolute; z-index: 10; top: 0px"
      ></canvas>

      <canvas
        @touchstart="handleTouchStart"
        @mousedown="handleMouseDown"
        ref="vQ_game_6"
        class="layer_a layer_i index_cable-keyboard layer_iVq_true"
        style="position: absolute; z-index: 9; top: 0px"
      ></canvas>

      <canvas
        @touchstart="handleTouchStart"
        @mousedown="handleMouseDown"
        ref="vQ_game_7"
        class="layer_a layer_i index_pc layer_iVq_true"
        style="position: absolute; z-index: 5; top: 0px"
      ></canvas>

      <canvas
        @touchstart="handleTouchStart"
        @mousedown="handleMouseDown"
        ref="vQ_game_8"
        class="layer_a layer_i index_chair layer_iVq_true"
        style="position: absolute; z-index: 6; top: 0px"
      ></canvas>

      <canvas
        @touchstart="handleTouchStart"
        @mousedown="handleMouseDown"
        ref="vQ_game_9"
        class="layer_a layer_i index_chair layer_iVq_true"
        style="position: absolute; z-index: 4; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_10"
        class="layer_a layer_i"
        style="position: absolute; z-index: 4; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_11"
        class="layer_a layer_i"
        style="position: absolute; z-index: 7; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_12"
        class="layer_a layer_i"
        style="position: absolute; z-index: 7; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_13"
        class="layer_a layer_i"
        style="position: absolute; z-index: 4; top: 0px"
      ></canvas>

    </div>

    <div
      class="game_load_other"
      :class="{ 'fade-out': !showLoadingStatus }"
      v-show="showLoadingStatus || !fadeOut"
    >
      <div class="game_load_other_inner">
        <img
          :src="iconSrc"
          alt=""
          style="max-width: 62px; max-height: 62px; min-width: 62px; min-height: 62px;"
        />
      </div>
    </div>

  </div>
</template>

<style scoped>
@import '../assets/css/gameConsts.css';
@import '../assets/css/medias.css';
</style>