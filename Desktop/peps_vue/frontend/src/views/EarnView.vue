<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue'
import '../../node_modules/flowbite-vue/dist/index.css'
import { getUserTasks, getTask, endTask, checkSubscribe, taskNextStep } from '@/utils/apiRequest'
import { UserStorage } from '@/stores/userStore'
import { TelegramStorage } from '@/stores/telegramStore'
import { shareStory, telegramLink, telegramDefaultLink } from '@/composables/useTelegramSetup'

import { localText } from '@/interface'
import { TELEGRAM_BOT } from '@/config'
import { RouterLink } from 'vue-router'

export default defineComponent({
  setup() {
    // toasts
    const showToastTaskExists = ref(false)
    const showToast2 = ref(false)
    // toasts

    const namePage = 'earn'

    const useUserStore = UserStorage()
    const useTelegramStore = TelegramStorage()

    const userData = computed(() => useUserStore.user || {})
    const userSettings = computed(() => useUserStore.settings || {})

    const userDataSettings = computed(() => {
      const settings = useUserStore.settings || {}
      return {
        ...settings,
        language: settings.language || useTelegramStore.getUserLanguage() || 'en'
      }
    })

    const loaderStatusPage = ref(true)

    const tasks = ref([])
    const storyTask = ref(false)

    let interval = setInterval(async () => {
      if ('user_id' in userData.value) {
        const response = await getUserTasks(userData.value.user_id)

        if (response.success) {
          filterTasks(response.tasks)
          loaderStatusPage.value = false
          clearInterval(interval)
        }
      }
    }, 500)

    const filterTasks = (response_tasks) => {
      response_tasks.forEach((task) => {
        if (task.id == 'story') {
          storyTask.value = task.completed
        } else {
          tasks.value.push(task)
        }
      })
    }

    const startTaskClick = async (task) => {
      if (task.task_redirect.startsWith('https://t.me/')) {
        const checkTaskStatusResponse = checkTaskStatus(task.id)

        if (checkTaskStatusResponse == 'completed') {
          // выдача приза
          if (task.task_gift_type == 'views') {
            userData.value.balance.views += parseInt(task.task_gift)
          } else if (task.task_gift_type == 'money') {
            userData.value.balance.earn += parseInt(task.task_gift)
          } else {
            userData.value.balance.ton += parseInt(task.task_gift)
          }

          const response = await endTask(
            task.id,
            userData.value.user_id,
            userData.value.balance.views,
            userData.value.balance.earn,
            userData.value.balance.ton
          )

          if (response.success) {
            // location.reload()
          }
        } else {
          const channelLink = task.task_redirect.split('@')[0]
          const channelId = task.task_redirect.split('@')[1]

          await getTask(task.id, userData.value.user_id)

          // telegram tasks

          telegramLink(channelLink)

          // начинается цикл проверки на завершение таска

          const responseTelegramTask = await checkSubscribe(userData.value.user_id, channelId)

          let intervalTelegramTask

          intervalTelegramTask = setInterval(async () => {
            if (responseTelegramTask.success) {
              if (responseTelegramTask.isSubscribed) {
                // подписан на канал
                clearInterval(intervalTelegramTask)
                const responseTelegramTaskNextStep = await taskNextStep(
                  task.id,
                  userData.value.user_id
                )
                if (responseTelegramTaskNextStep.success) {
                  // location.reload()
                }
              } else {
                // не подписан на канал
                console.log('Не подписан на канал')
              }
            }
          }, 1000)
        }
      } else if (task.task_redirect.startsWith('https://x.com/')) {
        const checkTaskStatusResponse = checkTaskStatus(task.id)

        if (checkTaskStatusResponse == 'completed') {
          if (task.task_gift_type == 'views') {
            userData.value.balance.views += parseInt(task.task_gift)
          } else if (task.task_gift_type == 'money') {
            userData.value.balance.earn += parseInt(task.task_gift)
          } else {
            userData.value.balance.ton += parseInt(task.task_gift)
          }

          const response = await endTask(
            task.id,
            userData.value.user_id,
            userData.value.balance.views,
            userData.value.balance.earn,
            userData.value.balance.ton
          )

          if (response.success) {
            location.reload()
          }
        } else {
          const channelLink = task.task_redirect

          await getTask(task.id, userData.value.user_id)

          telegramDefaultLink(channelLink)

          await taskNextStep(task.id, userData.value.user_id)

          location.reload()
        }
      } else if (task.task_redirect.startsWith('https://instagram.com/')) {
        const checkTaskStatusResponse = checkTaskStatus(task.id)

        if (checkTaskStatusResponse == 'completed') {
          if (task.task_gift_type == 'views') {
            userData.value.balance.views += parseInt(task.task_gift)
          } else if (task.task_gift_type == 'money') {
            userData.value.balance.earn += parseInt(task.task_gift)
          } else {
            userData.value.balance.ton += parseInt(task.task_gift)
          }

          const response = await endTask(
            task.id,
            userData.value.user_id,
            userData.value.balance.views,
            userData.value.balance.earn,
            userData.value.balance.ton
          )

          if (response.success) {
            location.reload()
          }
        } else {
          const channelLink = task.task_redirect

          await getTask(task.id, userData.value.user_id)

          telegramDefaultLink(channelLink)

          await taskNextStep(task.id, userData.value.user_id)

          location.reload()
        }
      } else {
        const checkTaskStatusResponse = checkTaskStatus(task.id)

        if (checkTaskStatusResponse == 'completed') {
          // выдача приза
          if (task.task_gift_type == 'views') {
            userData.value.balance.views += parseInt(task.task_gift)
          } else if (task.task_gift_type == 'money') {
            userData.value.balance.earn += parseInt(task.task_gift)
          } else {
            userData.value.balance.ton += parseInt(task.task_gift)
          }

          const response = await endTask(
            task.id,
            userData.value.user_id,
            userData.value.balance.views,
            userData.value.balance.earn,
            userData.value.balance.ton
          )

          if (response.success) {
            location.reload()
          } else {
            console.log(response)
          }
        } else if (checkTaskStatusResponse == 'in_progress') {
          location.href = task.task_redirect + '?task=' + task.id
        } else if (checkTaskStatusResponse == 'success') {
          // выполнено
          return
        } else {
          const taskProgress = userData.value.tasks_progress

          if (taskProgress && Object.keys(taskProgress).length > 0) {
            if (Array.isArray(tasks.value)) {
              // Найдем таск того же типа, который не текущий и не завершен
              const matchingTask = tasks.value.find(
                (task2) =>
                  task2.id !== task.id &&
                  task2.task_type === task.task_type &&
                  !taskProgress[task2.id]
              )

              // Если найден такой таск, проверяем его статус
              if (matchingTask) {
                const status = checkTaskStatus(matchingTask.id)

                if (status === 'completed' || status === 'success') {
                  const response = await getTask(task.id, userData.value.user_id)
                  if (response.success) {
                    window.location.href = task.task_redirect + '?task=' + task.id
                  }
                } else {
                  showToastTaskExists.value = true
                  console.log('Уже есть активный таск с таким типом')
                }
              } else {
                // Если подходящего таска нет, просто продолжаем выполнение задания
                const response = await getTask(task.id, userData.value.user_id)
                if (response.success) {
                  window.location.href = task.task_redirect + '?task=' + task.id
                }
              }
            }
          } else {
            const response = await getTask(task.id, userData.value.user_id)
            if (response.success) {
              window.location.href = task.task_redirect + '?task=' + task.id
            }
          }

          // const response = await getTask(task.id, userData.value.user_id)
          // if (response.success) {
          // window.location.href = task.task_redirect + '?task=' + task.id
          // }
        }
      }
    }

    const checkTaskStatus = (taskId: string) => {
      const taskInfo = tasks.value.find((task) => task.id === taskId)

      if (!taskInfo || !taskInfo.task_progress) {
        return 'false'
      }

      const { task_progress, task_steps } = taskInfo

      if (task_progress === false) {
        return 'false'
      } else if (task_progress.current_step >= task_steps) {
        if (taskInfo.completed) {
          return 'success'
        } else {
          return 'completed'
        }
      } else {
        return 'in_progress'
      }
    }

    const storyTaskClick = async () => {
      const story_task_button = document.querySelector('.story_task_button')
      story_task_button.classList.add('active')

      if (useTelegramStore.getUserIsPremium()) {
        shareStory(userData.value.referal_key, userSettings.value.language)

        if (!storyTask.value) {
          const response = await endTask(
            'story',
            userData.value.user_id,
            parseInt(userData.value.balance.views),
            parseInt(userData.value.balance.earn) + 15000,
            parseInt(userData.value.balance.ton)
          )

          if (response.success) {
            setTimeout(() => {
              story_task_button.classList.remove('active')
              story_task_button.classList.add('closed')
              userData.value.balance.earn = parseInt(userData.value.balance.earn) + 15000
              storyTask.value = true
            }, 3500)
          }
        } else {
          setTimeout(() => {
            story_task_button.classList.remove('active')
            story_task_button.classList.add('closed')
          }, 3500)
        }
      } else {
        shareStory(userData.value.referal_key, userSettings.value.language)

        const response = await endTask(
          'story',
          userData.value.user_id,
          parseInt(userData.value.balance.views),
          parseInt(userData.value.balance.earn),
          parseInt(userData.value.balance.ton)
        )

        if (response.success) {
          setTimeout(() => {
            story_task_button.classList.remove('active')
            story_task_button.classList.add('closed')
          }, 3500)
        }
      }
    }

    function repostGame() {
      let text_lg = ''

      if (userSettings.value.language === 'ru') {
        text_lg =
          '🐸 Лягушонок Пепе стал игрой! Прокачивай оборудование чтобы получить новые предметы и $PEPS. 🎁 Бери свою приветственную награду 2,500 $PEPS и лимитированный скин!'
      } else {
        text_lg =
          '🐸 Pepe the frog becomes a game! Upgrade your setup to get new items and $PEPS. 🎁 Claim your welcome gift, 2,500 $PEPS and limited skin'
      }

      const baseUrl = 'https://t.me/share/url?url='
      const appUrl = `https://t.me/${TELEGRAM_BOT}/app?startapp=${userData.value.referal_key}`
      const fullUrl = `${baseUrl}${encodeURIComponent(appUrl)}&text=${encodeURIComponent(text_lg)}`

      telegramLink(fullUrl)
    }

    function copyRepostGame() {
      let text_lg = ''

      if (userDataSettings.value.language === 'ru') {
        text_lg =
          '🐸 Лягушонок Пепе стал игрой! Прокачивай оборудование чтобы получить новые предметы и $PEPS. 🎁 Бери свою приветственную награду 2,500 $PEPS и лимитированный скин!'
      } else {
        text_lg =
          '🐸 Pepe the frog becomes a game! Upgrade your setup to get new items and $PEPS. 🎁 Claim your welcome gift, 2,500 $PEPS and limited skin'
      }

      const appUrl = `https://t.me/${TELEGRAM_BOT}/app?startapp=${userData.value.referal_key}`
      const fullUrl = `${appUrl}\n\n${text_lg}`

      const tempInput = document.createElement('input')
      tempInput.value = fullUrl
      document.body.appendChild(tempInput)
      tempInput.select()
      document.execCommand('copy')
      document.body.removeChild(tempInput)

      showToast2.value = true
      setTimeout(() => {
        showToast2.value = false
      }, 2000)
    }

    return {
      tasks,
      startTaskClick,
      loaderStatusPage,
      userData,
      checkTaskStatus,
      storyTaskClick,
      storyTask,
      showToastTaskExists,
      showToast2,
      repostGame,
      copyRepostGame,

      namePage,
      userDataSettings,
      localText
    }
  }
})
</script>

<template>
  <div id="toast_1" :class="showToastTaskExists ? 'show' : ''" class="toast">
    {{ localText['root'][userDataSettings.language].root_text_7 }}
  </div>
  <div id="toast_2" :class="showToast2 ? 'show' : ''" class="toast">
    {{ localText['root'][userDataSettings.language].root_text_14 }}
  </div>

  <div class="earn">
    <div class="earn_inner">
      <div class="upgrades_section earn_limited">
        <div class="upgrades_section_title special_sp">
          <div class="skeleton text">
            <h4>{{ localText[namePage][userDataSettings.language].ea_text_1 }}</h4>
          </div>
        </div>

        <div class="upgrades_section_content">
          <div
            @click="repostGame"
            class="earn_limited_task upgrades_section_skins_item skeleton block"
            id="invite_frien_limited_js"
          >
            <div
              style="overflow: initial"
              class="special_spanner upgrades_section_skins_item_left_info_title"
            >
              <span style="border-radius: 6px" id="limited_task_time">6d 2h</span>
            </div>

            <div class="upgrades_section_skins_item_left">
              <div class="upgrades_section_skins_item_left_skin rare">
                <img src="./../assets/img/pepsi.svg" alt="money" />
              </div>

              <div class="upgrades_section_skins_item_left_info">
                <div class="upgrades_section_skins_item_left_info_title">
                  <h4>{{ localText[namePage][userDataSettings.language].ea_text_2 }}</h4>
                </div>
                <div
                  class="upgrades_section_skins_item_left_info_earn upgrades_section_skins_item_left_info_earn_d"
                >
                  <p>{{ localText[namePage][userDataSettings.language].ea_text_3 }} 2,500 $PEPS</p>
                </div>
              </div>

              <div v-if="userData.referals >= 1" class="upgrades_section_skins_item_right_upgrade">
                <svg
                  style="margin-left: -40px"
                  width="22"
                  height="22"
                  viewBox="0 0 22 22"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M7.75 11L9.91667 13.1667L14.25 8.83333M1.25 11C1.25 12.2804 1.50219 13.5482 1.99217 14.7312C2.48216 15.9141 3.20034 16.9889 4.10571 17.8943C5.01108 18.7997 6.08591 19.5178 7.26884 20.0078C8.45176 20.4978 9.71961 20.75 11 20.75C12.2804 20.75 13.5482 20.4978 14.7312 20.0078C15.9141 19.5178 16.9889 18.7997 17.8943 17.8943C18.7997 16.9889 19.5178 15.9141 20.0078 14.7312C20.4978 13.5482 20.75 12.2804 20.75 11C20.75 9.71961 20.4978 8.45176 20.0078 7.26884C19.5178 6.08591 18.7997 5.01108 17.8943 4.10571C16.9889 3.20034 15.9141 2.48216 14.7312 1.99217C13.5482 1.50219 12.2804 1.25 11 1.25C9.71961 1.25 8.45176 1.50219 7.26884 1.99217C6.08591 2.48216 5.01108 3.20034 4.10571 4.10571C3.20034 5.01108 2.48216 6.08591 1.99217 7.26884C1.50219 8.45176 1.25 9.71961 1.25 11Z"
                    stroke="#65E262"
                    stroke-width="1.52941"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </div>

              <div v-else class="upgrades_section_skins_item_right_upgrade">
                <img src="./../assets/img/chevrone_right.svg" alt="" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="upgrades_section earn_limited">
        <div class="upgrades_section_title skeleton text">
          <h4>{{ localText[namePage][userDataSettings.language].ea_text_5 }}</h4>
        </div>

        <div class="earn_challenges_block skeleton block">
          <div class="earn_challenges_block_inner">
            <div class="earn_challenges_block_top">
              <div class="earn_challenges_block_top_block">
                <img src="./../assets/img/money_four.svg" alt="money" />
              </div>
              <div class="earn_challenges_block_top_texts">
                <div class="earn_challenges_block_top_texts_title">
                  <h4
                    v-if="userData.referals >= 10"
                    style="
                      white-space: nowrap;
                      overflow: hidden;
                      text-overflow: ellipsis;
                      max-width: 122px;
                    "
                  >
                    {{ localText[namePage][userDataSettings.language].ea_text_17 }}
                  </h4>
                  <h4
                    v-else
                    style="
                      white-space: nowrap;
                      overflow: hidden;
                      text-overflow: ellipsis;
                      max-width: 122px;
                    "
                  >
                    {{ localText[namePage][userDataSettings.language].ea_text_6 }}
                  </h4>
                </div>
                <div class="earn_challenges_block_top_texts_description">
                  <p v-if="userData.referals >= 10">{{ localText[namePage][userDataSettings.language].ea_text_7 }} 1,000 $PEPS</p>
                  <p v-else>{{ localText[namePage][userDataSettings.language].ea_text_7 }} 20,000 $PEPS</p>
                </div>
                <div class="earn_challenges_block_top_texts_counts">
                  <span v-if="userData.referals < 10">{{ userData.referals }}/10</span>
                </div>
              </div>
              <div class="earn_challenges_block_top_spanner">
                <img src="./../assets/img/money.svg" alt="money" />
                <p v-if="userData.referals >= 10">1,000</p>
                <p v-else>20,000</p>
              </div>
            </div>
            <div class="earn_challenges_block_footer">
              <div class="earn_challenges_block_footer_button">
                <div
                  @click="repostGame"
                  class="upgrades_section_skins_item_right_upgrade_btn actived"
                >
                  <button id="invite_frien_nolimited_js">
                    <img
                      class="button_loading_img"
                      src="./../assets/img/button_loading.svg"
                      alt="loading"
                    />
                    <p>{{ localText[namePage][userDataSettings.language].ea_text_9 }}</p>
                  </button>
                </div>

                <div v-if="userData.referals >= 10" class="referals_block_link_noactive">
                  <span @click="copyRepostGame">
                    <img src="./../assets/img/copy.svg" alt="copy" />
                  </span>
                </div>

              </div>
            </div>
          </div>
        </div>

        <RouterLink to="/referals">
          <div class="earn_friends_invited">
            <div class="earn_friends_invited_inner">
              <div class="earn_friends_invited_inner_text">
                <p>{{ userData.referals }} {{ localText[namePage][userDataSettings.language].ea_text_18 }}</p>
              </div>
              <div class="earn_friends_invited_inner_photo">
                <img src="./../assets/img/chevrone_earn.svg" alt="">
              </div>
            </div>
          </div>
        </RouterLink>

      </div>

      <div class="upgrades_section earn_limited earn_tasks">
        <div class="upgrades_section_title skeleton text">
          <h4>{{ localText[namePage][userDataSettings.language].ea_text_10 }}</h4>
        </div>

        <div
          v-if="loaderStatusPage"
          style="margin: auto; text-align: center; align-items: center; padding: 60px 0px"
        >
          <div class="jumping-dots-loader"><span></span> <span></span> <span></span></div>
        </div>

        <div :style="!loaderStatusPage ? '' : 'opacity: 0'" class="story_task_block">
          <div class="story_task">
            <div class="story_task_h4">
              <h4>{{ localText[namePage][userDataSettings.language].ea_text_12 }}</h4>
            </div>
            <div class="story_task_p">
              <p>{{ localText[namePage][userDataSettings.language].ea_text_13 }}</p>
            </div>
            <div class="story_task_span">
              <span>+15,000 $PEPS</span>
            </div>
          </div>

          <div
            @click="storyTaskClick()"
            :class="storyTask ? 'closed' : ''"
            class="story_task_button"
          >
            <button>
              <img
                class="button_loading_img"
                src="./../assets/img/button_loading.svg"
                alt="loading"
              />
              <p>{{ localText[namePage][userDataSettings.language].ea_text_14 }}</p>
              <img src="./../assets/img/story.svg" alt="story" />
            </button>
          </div>

          <div class="story_tasks_line"></div>
        </div>

        <div class="earn_tasks_block skeleton block">
          <div v-for="task in tasks" class="earn_tasks_block_item">
            <div class="earn_tasks_block_item_left">
              <div class="earn_tasks_block_item_left_image">
                <img :src="task.task_photo" alt="money" />
              </div>
              <div class="earn_tasks_block_item_left_info">
                <div class="earn_tasks_block_item_left_info_title">
                  <h4>{{ task.task_name }}</h4>
                </div>
                <div class="earn_tasks_block_item_left_info_earn">
                  <p v-if="task.task_gift_type == 'views'">
                    +{{ task.task_gift }}
                    {{ localText['root'][userDataSettings.language].root_text_1 }}
                  </p>
                  <p v-else-if="task.task_gift_type == 'money'">+{{ task.task_gift }} $PEPS</p>
                  <p v-else-if="task.task_gift_type == 'ton'">
                    +{{ task.task_gift }}
                    {{ localText['root'][userDataSettings.language].root_text_5 }}
                  </p>
                  <p v-else>{{ localText[namePage][userDataSettings.language].ea_text_16 }}</p>
                </div>
              </div>
            </div>
            <div class="earn_tasks_block_item_right">
              <button
                @click="startTaskClick(task)"
                :class="checkTaskStatus(task.id)"
                class="earn_tasks_block_item_right_button"
              >
                <img
                  class="button_loading_img"
                  src="./../assets/img/button_loading.svg"
                  alt="loading"
                />
                <svg
                  width="17"
                  height="17"
                  viewBox="0 0 17 17"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M6 8.5L7.66667 10.1667L11 6.83333M1 8.5C1 9.48491 1.19399 10.4602 1.5709 11.3701C1.94781 12.2801 2.50026 13.1069 3.1967 13.8033C3.89314 14.4997 4.71993 15.0522 5.62987 15.4291C6.53982 15.806 7.51509 16 8.5 16C9.48491 16 10.4602 15.806 11.3701 15.4291C12.2801 15.0522 13.1069 14.4997 13.8033 13.8033C14.4997 13.1069 15.0522 12.2801 15.4291 11.3701C15.806 10.4602 16 9.48491 16 8.5C16 7.51509 15.806 6.53982 15.4291 5.62987C15.0522 4.71993 14.4997 3.89314 13.8033 3.1967C13.1069 2.50026 12.2801 1.94781 11.3701 1.5709C10.4602 1.19399 9.48491 1 8.5 1C7.51509 1 6.53982 1.19399 5.62987 1.5709C4.71993 1.94781 3.89314 2.50026 3.1967 3.1967C2.50026 3.89314 1.94781 4.71993 1.5709 5.62987C1.19399 6.53982 1 7.51509 1 8.5Z"
                    stroke="#65E262"
                    stroke-width="1.17647"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
                <p v-if="checkTaskStatus(task.id) == 'completed'">
                  {{ localText[namePage][userDataSettings.language].ea_text_15 }}
                </p>
                <p v-if="checkTaskStatus(task.id) == 'in_progress'">
                  {{ userData.tasks_progress[task.id].current_step }} / {{ task.task_steps }}
                </p>
                <p v-if="checkTaskStatus(task.id) == 'false'">
                  {{ localText[namePage][userDataSettings.language].ea_text_11 }}
                </p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '../assets/css/earn.css';
@import '../assets/css/upgrades.css';
@import '../assets/css/shop.css';
@import '../assets/css/profile.css';
@import '../assets/css/referals.css';

.story_task {
  width: 100%;
  min-height: 86px;
  background: url('./../assets/img/task_story_background.png') no-repeat;
  background-size: cover;
  border-radius: 17px;
  padding: 13px 18px;
  text-align: left;
}

.story_task_h4 h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--h);
  margin-bottom: 5px;
}

.story_task_p p {
  font-size: 14px;
  font-weight: 500;
  color: #75c8f2;
  margin-bottom: 5px;
}

.story_task_span span {
  font-size: 14px;
  font-weight: 500;
  color: #6182a6;
}
</style>
