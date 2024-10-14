<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { UserStorage } from '@/stores/userStore'
import { updateGame, getPutonSkins } from '@/utils/apiRequest'
import { Rive } from '@rive-app/canvas'
import { getImage, getSkinInfo, requiredXpForPercents, limitAmount } from '@/utils/funcs'
import { telegramLink, vibrateTelegram } from '@/composables/useTelegramSetup'
import { useRouter } from 'vue-router'

import { TelegramStorage } from '@/stores/telegramStore'
import { localText } from '@/interface'
import { TELEGRAM_BOT } from '@/config'
import { reactive } from 'vue'

const router = useRouter()

const namePage = 'home'
const skinsPath = window.location.pathname.replace('/home', '')
const isLocalStorageAvailable = typeof localStorage['skin_id'] !== 'undefined'

const userStorage = UserStorage()
const telegramStorage = TelegramStorage()

const userStorageReactive = reactive(UserStorage())

const userDataSettings = computed(() => {
  const settings = userStorage.settings || {}
  return {
    ...settings,
    language: settings.language || telegramStorage.getUserLanguage() || 'en'
  }
})

const vQ_game_0 = ref<HTMLCanvasElement | null>(null)
const vQ_game_1 = ref<HTMLCanvasElement | null>(null)
const vQ_game_2 = ref<HTMLCanvasElement | null>(null)
const vQ_game_3 = ref<HTMLCanvasElement | null>(null)
const vQ_game_4 = ref<HTMLCanvasElement | null>(null)
const vQ_game_5 = ref<HTMLCanvasElement | null>(null)
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
  return todayIconLoading.value[Math.floor(Math.random() * todayIconLoading.value.length)]
}

const iconSrc = computed(() => {
  return ['/src/assets/img/', getTodayIcon(), '.svg'].join('')
})

const putonSkinsList = ref([])
const putonSkins = ref([])

let isFireStarted = ref(false)
let fireClickChecker = ref(true)
let riveInstanceConfetti: rive.Rive
let riveFireInstance: rive.Rive

const showLoadingStatus = ref(true)
const showLoadingModalStatus = ref(true)
const canvasConfetti = ref(null)
const fadeOut = ref(false)

const userExperience = userStorage.user.experience

let riveInstanceChest: Rive | null = null

const createGameChest = async () => {
  const GameChestClass = document.getElementById(
    'gameChest_block_canvas'
  ) as HTMLCanvasElement | null
  if (GameChestClass) {
    const dpr = window.devicePixelRatio || 1
    GameChestClass.width = GameChestClass.clientWidth * dpr
    GameChestClass.height = GameChestClass.clientHeight * dpr
    const context = GameChestClass.getContext('2d')
    if (context) {
      riveInstanceChest = new Rive({
        src: `/src/assets/animations/peps_case_icon.riv`,
        canvas: GameChestClass,
        autoplay: false,
        useOffscreenRenderer: true,
        onLoad: () => {
          console.log('Rive loaded successfully')
        },
        onError: (e) => {
          console.error('Rive load error:', e)
        }
      })
      riveInstanceChest.play()
    }
  } else {
    console.error('Canvas element not found')
  }
}

onMounted(() => {
  createGameChest()
})

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
      }
    })
  } catch (error) {
    return
  }

  vibrateTelegram('impact', { impact_style: 'heavy' })

  setTimeout(() => {
    isFireStarted.value = false
    fireClickChecker.value = true

    fireElement.remove()
  }, 3276)
}

function handlePointerDown(event: PointerEvent) {
  event.preventDefault();
  const target = event.target as HTMLElement;

  if (target.classList.contains('gameHitbox')) {
    if (event.pointerType === 'touch') {
      touch(false);
    } else if (event.detail === 2) {
      touch(false);
      touch(false);
    }
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
        if (!response.ok) {}
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

function addUniqueImage(array, image) {
  const exists = array.some((item) => item.src === image.src && item.layer === image.layer)
  if (!exists) {
    array.push(image)
  }
}

onMounted(() => {
  const canvases = [
    vQ_game_0.value,
    vQ_game_1.value,
    vQ_game_2.value,
    vQ_game_3.value,
    vQ_game_4.value,
    vQ_game_5.value,
    vQ_game_7.value,
    vQ_game_8.value,
    vQ_game_9.value,
    vQ_game_10.value,
    vQ_game_11.value,
    vQ_game_12.value,
    vQ_game_13.value
  ]

  if (canvases) {
    const canvas0 = setupCanvas(vQ_game_0.value, 440, 1000)
    const canvas1 = setupCanvas(vQ_game_1.value, 440, 1000)
    const canvas2 = setupCanvas(vQ_game_2.value, 440, 1000)
    const canvas3 = setupCanvas(vQ_game_3.value, 440, 1000)
    const canvas4 = setupCanvas(vQ_game_4.value, 440, 1000)
    const canvas5 = setupCanvas(vQ_game_5.value, 440, 1000)
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
    const images0 = [],
      images1 = [],
      images10 = [],
      images11 = [],
      images12 = [],
      images13 = []

    // Clickable elements
    const images2 = [],
      images3 = [],
      images4 = [],
      images5 = [],
      images7 = [],
      images8 = [],
      images9 = []

    function setLists() {
      var currentDateLocal = new Date()
      var hoursLocal = currentDateLocal.getHours()

      if (hoursLocal >= 7 && hoursLocal < 17) {
        addUniqueImage(images1, {
          src: `${skinsPath}src/assets/skins/window_1.svg`,
          layer: 4
        })
        addUniqueImage(images1, {
          src: `${skinsPath}src/assets/skins/light-window_1.svg`,
          layer: 5
        })
      } else {
        addUniqueImage(images1, {
          src: `${skinsPath}src/assets/skins/window_0.svg`,
          layer: 4
        })
        addUniqueImage(images1, {
          src: `${skinsPath}src/assets/skins/light-window_0.svg`,
          layer: 5
        })
      }

      // Not clickable elements
      putonSkins.value.forEach((element) => {
        if (element.clickable == false) {
          if (
            !element.skin_id.includes('systembox_') &&
            !element.skin_id.includes('flower_') &&
            !element.skin_id.includes('item-table_') &&
            !element.skin_id.includes('item-window_')
          ) {
            addUniqueImage(images0, {
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: element.z_index
            })
          }
        }
      })

      // Clickable elements
      putonSkins.value.forEach((element) => {
        if (element.clickable == true) {
          if (!element.skin_id.includes('monitors_') && !element.skin_id.includes('systembox_')) {
            if (element.skin_id.includes('tee_')) {
              addUniqueImage(images2, {
                src: `${getImage(element.skin_id, '.svg')}`,
                layer: element.z_index
              })
            } else if (element.skin_id.includes('joint_')) {
              addUniqueImage(images2, {
                src: `${getImage(element.skin_id, '.svg')}`,
                layer: 50
              })
              addUniqueImage(images2, {
                src: `${getImage(`smoke`, '.svg')}`,
                layer: 50
              })
            } else if (element.skin_id.includes('chair_4')) {
              addUniqueImage(images2, {
                src: `${getImage(`chair_4_left`, '.svg')}`,
                layer: 6
              })
            } else if (element.skin_id.includes('soplya-mouth_')) {
              addUniqueImage(images2, {
                src: `${getImage(element.skin_id, '.svg')}`,
                layer: 50
              })
            } else if (element.skin_id.includes('chair_')) {
              return
            } else if (element.skin_id.includes('keyboard_')) {
              const id_count = element.skin_id.split('_')[1]
              addUniqueImage(images2, {
                src: `${getImage(`cable-keyboard_${id_count}`, '.svg')}`,
                layer: 8
              })
            } else {
              addUniqueImage(images2, {
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
            addUniqueImage(images3, {
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
            addUniqueImage(images4, {
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
            addUniqueImage(images5, {
              src: `${getImage(`hands_${id_count}`, '.svg')}`,
              layer: element.z_index
            })
          }
        }
      })

      // Clickable elements (systembox)
      putonSkins.value.forEach((element) => {
        if (element.clickable == false) {
          if (element.skin_id.includes('systembox_')) {
            addUniqueImage(images7, {
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
            addUniqueImage(images8, {
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
            addUniqueImage(images9, {
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: 8
            })
          }
        }
      })

      // Not clickable elements (item-table)
      putonSkins.value.forEach((element) => {
        if (element.clickable == false) {
          if (element.skin_id.includes('item-table_')) {
            addUniqueImage(images11, {
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
            addUniqueImage(images12, {
              src: `${getImage(element.skin_id, '.svg')}`,
              layer: 8
            })
          }
        }
      })

      // Not clickable elements (item-window)
      putonSkins.value.forEach((element) => {
        if (element.clickable == true) {
          if (element.skin_id !== 'table_0' && element.skin_id !== 'table_1') {
            if (element.skin_id.includes('table_')) {
              const id_count = element.skin_id.split('_')[1]
              addUniqueImage(images13, {
                src: `${getImage(`table_${id_count}_right`, '.svg')}`,
                layer: 8
              })
            }
          }
        }
      })

      const canvases = [
        canvas0,
        canvas1,
        canvas2,
        canvas3,
        canvas4,
        canvas5,
        canvas7,
        canvas8,
        canvas9,
        canvas10,
        canvas11,
        canvas12,
        canvas13
      ]

      const images = [
        images0,
        images1,
        images2,
        images3,
        images4,
        images5,
        images7,
        images8,
        images9,
        images10,
        images11,
        images12,
        images13
      ]

      async function processCanvases() {
        try {
          const promises = canvases.map((canvas, index) => combineImages(canvas, images[index]))
          await Promise.all(promises)
        } catch (err) {
          return
        }

        showLoadingStatus.value = false
      }

      processCanvases()
    }
  }
})

function touchAnimation() {
  vibrateTelegram('impact', { impact_style: 'soft' })

  if (userStorage.settings.tap_animation) {
    const elements = [
      vQ_game_2.value,
      vQ_game_5.value,
      vQ_game_4.value,
      vQ_game_3.value,
      vQ_game_8.value,
      vQ_game_13.value
    ]
    elements.forEach((element) => {
      if (element) {
        element.classList.remove('animate')
        void element.offsetWidth
        element.classList.add('animate')
        element.addEventListener(
          'animationend',
          () => {
            element.classList.remove('animate')
          },
          { once: true }
        )
      }
    })
  }
}

let lastClickTimeout

function touchTimeout() {
  clearTimeout(lastClickTimeout)
  lastClickTimeout = setTimeout(async () => {
    await updateGame(
      userStorage.user.user_id,
      userStorage.user.balance.views,
      userStorage.user.balance.earn,
      userStorage.user.balance.ton,
      userStorage.costs.stamina_now,
      userStorage.user.experience - userExperience
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
    userStorage.user.experience += 1
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

setInterval(async () => {
  const response = await updateGame(
    userStorage.user.user_id,
    userStorage.user.balance.views,
    userStorage.user.balance.earn,
    userStorage.user.balance.ton,
    userStorage.costs.stamina_now,
    userStorage.user.experience - userExperience
  )

  if (response.success) {
    userStorage.user.balance = response.balances
  }
}, 15000)

function getSkinStorageInfo(type) {
  const skin_id = localStorage.getItem('skin_id')
  const data = getSkinInfo(skin_id)

  if (type === 'description') {
    let canvas_confetti_class = document.getElementById('layer_i_1500')
    let canvasConfettiClass = document.querySelector('.layer_ids_1500')

    const riveInstanceConfetti = new Rive({
      src: `${skinsPath}src/assets/animations/confetti.riv`,
      canvas: canvas_confetti_class,
      autoplay: false,
      onLoad: () => {},
      onError: (e) => {}
    })

    setTimeout(() => {
      canvasConfettiClass.classList.add('active')
      canvas_confetti_class.classList.add('active')
      riveInstanceConfetti?.play()
      vibrateTelegram('impact', { impact_style: 'heavy' })
    }, 430)

    setTimeout(() => {
      canvasConfettiClass.classList.remove('active')
      riveInstanceConfetti?.stop()
      canvas_confetti_class.remove()
    }, 2780)

    localStorage.removeItem('skin_id')
  }

  return data
}

function claimSkin() {
  const modal = document.querySelector('.modal_skin')
  const claimButton = document.querySelector('.modal_claim_button')
  const closeButton = document.querySelector('.modal_close_button')

  closeButton.addEventListener('click', () => {
    modal.classList.remove('active')
  })

  claimButton.addEventListener('click', () => {
    claimButton.classList.remove('actived')
    claimButton.classList.add('disabled')

    setTimeout(() => {
      claimButton.classList.remove('disabled')
      claimButton.classList.add('actived')
      modal.classList.remove('active')
    }, 400)
  })
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

watch(
  () => userStorage.user.experience,
  async (newValue) => {
    if (newValue >= userStorage.user.experience_need) {
      const response = await updateGame(
        userStorage.user.user_id,
        userStorage.user.balance.views,
        userStorage.user.balance.earn,
        userStorage.user.balance.ton,
        userStorage.costs.stamina_now,
        userStorage.user.experience - userExperience
      )

      console.log(response)

      if (response.success) {
        location.reload()
      }
    }
  }
)

window.addEventListener('pointerdown', handlePointerDown)
</script>

<template>
  <div class="game">

    <div class="gameChest">
      <RouterLink to="/chestDev">
        <div class="gameChest_block">
          <div class="gameChest_block_notify"></div>
          <div class="gameChest_block_canvas">
            <canvas id="gameChest_block_canvas" width="880" height="360"></canvas>
          </div>
        </div>
      </RouterLink>
    </div>

    <div class="gameNotifed">
      <div class="gameNotifed_block">
        <div
          class="gameNotifed_block_text"
          :style="{
            width:
              requiredXpForPercents(userStorageReactive.user.experience, userStorageReactive.user.experience_need) +
              '%'
          }"
        >
          <h4>
            {{ userStorageReactive.user.level }}
            {{ localText[namePage][userDataSettings.language].ho_text_1 }}
            {{ limitAmount(userStorageReactive.user.experience, userStorageReactive.user.experience_need) }}/{{ userStorageReactive.user.experience_need }}
          </h4>
        </div>
      </div>

      <div class="gameNotifed_block">
        <RouterLink to="/referals">
          <div class="gameNotifed_block_text_roadmap">
            <img src="./../assets/img/friens.svg" alt="" />
            <h4>{{ localText[namePage][userDataSettings.language].ho_text_2 }}</h4>
          </div>
        </RouterLink>
      </div>

      <div @click="repostGame" class="gameNotifed_repost">
        <img src="./../assets/img/repost.svg" alt="" />
      </div>
    </div>

    <div class="game_block" id="game_block">
      <div class="gameHitbox layer_i layer_i_true" id="gameHitbox_Click"></div>

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
        ref="vQ_game_2"
        class="layer_a layer_i layer_i_true layer_iVq_true"
        style="position: absolute; z-index: 9; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_3"
        class="layer_a layer_i index_keyboard"
        style="position: absolute; z-index: 9; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_4"
        class="layer_a layer_i index_monitor layer_iVq_true"
        style="position: absolute; z-index: 11; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_5"
        class="layer_a layer_i index_hands layer_iVq_true"
        style="position: absolute; z-index: 10; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_7"
        class="layer_a layer_i index_pc layer_iVq_true"
        style="position: absolute; z-index: 5; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_8"
        class="layer_a layer_i index_chair layer_iVq_true"
        style="position: absolute; z-index: 6; top: 0px"
      ></canvas>

      <canvas
        ref="vQ_game_9"
        class="layer_a"
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
        <div class="game_load_other_inner_img"
            style="margin: auto; max-height: 35px; min-width: 35px; min-height: 35px">
          <img
            :src="iconSrc"
            alt=""
            style="transform: scale(0.60); object-fit:contain; max-height: 100%; min-width: 100%; min-height: 100%"
          />
        </div>
      </div>
    </div>
  </div>

  <div
    class="layer_a layer_ids_1500"
    style="z-index: 10000; top: 70px; left: 50%; right: 50%; transform: translateX(-50%)"
  >
    <div class="" style="width: 100%; height: 100%">
      <canvas
        id="layer_i_1500"
        width="900"
        height="1950"
        style="vertical-align: top; width: 450px; height: 975px"
      ></canvas>
    </div>
  </div>

  <div v-if="!showLoadingStatus">
    <div v-if="isLocalStorageAvailable" class="modal modal_skin modal_task active">
      <div class="modal_inner">
        <div class="modal_close_button">
          <svg
            @click="claimSkin"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              opacity="0.5"
              d="M13.985 15.3767L4.25067 5.80729L5.87457 4.15541L15.6089 13.7248L13.985 15.3767ZM5.97102 15.4452L4.31913 13.8213L13.8886 4.08695L15.5404 5.71085L5.97102 15.4452Z"
              fill="white"
            />
          </svg>
        </div>

        <div class="modal_content">
          <div class="modal_content_image">
            <img :src="getImage(getSkinStorageInfo('uuid_name').uuid_name)" alt="skin" />
          </div>
          <div class="modal_content_reward">
            <h4>{{ getSkinStorageInfo('name').name }}</h4>
          </div>
          <div class="modal_content_description">
            <p v-if="userDataSettings.language == 'en'">
              {{ getSkinStorageInfo('description').description }}
            </p>
            <p v-if="userDataSettings.language == 'ru'">
              {{ getSkinStorageInfo('description').description_ru }}
            </p>
          </div>
        </div>

        <div class="modal_claim_button actived">
          <button @click="claimSkin" id="modal_claim_button">
            <img
              class="button_loading_img"
              src="./../assets/img/button_loading.svg"
              alt="loading"
            />
            <p>{{ localText['root'][userDataSettings.language].root_text_15 }}</p>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '../assets/css/gameConsts.css';
@import '../assets/css/medias.css';
@import '../assets/css/modals.css';
</style>
